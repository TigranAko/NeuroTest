import logging
from typing import Annotated
from uuid import UUID

from core.database import get_db
from core.settings import settings
from fastapi import Depends
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field
from repositories.answer import AnswerRepository
from repositories.question import QuestionRepository
from repositories.test import TestRepository
from schemas.answer import AnswerCreate
from schemas.question import QuestionCreate
from schemas.test import TestCreate
from services.file import FileService
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class Answer(BaseModel):
    text: str = Field(description="Текст варианта ответа")


class Question(BaseModel):
    question: str = Field(description="Текст вопроса")
    answers: list[Answer] = Field(
        description="Список  возможных ответов (без указания правильных)"
    )


class Test(BaseModel):
    questions: list[Question] = Field(description="Список всех вопросов теста")


def get_llm_chat():
    if settings.USE_LOCAL_LLM:
        return ChatOpenAI(
            api_key="No api key",
            base_url=settings.LOCAL_LLM_BASE_URL,
            model=settings.LOCAL_LLM_MODEL,
            temperature=0.1,
            max_retries=3,
        )
    return ChatOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        model="openrouter/free",
        temperature=0.1,
        max_retries=3,
        timeout=2 * 60 * 1000,  # две минуты
    )


llm = get_llm_chat()

structured_llm = llm.with_structured_output(Test)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Ты - строгий парсер тестов. "
            "Твоя задача - находить вопросы и варианты ответов. ",
        ),
        (
            "human",
            "Последний вопрос из предыдущего чанка:\n{first_question}\n"
            "Хвост предыдущего чанка:\n{previous_tail}\n\n"
            "Текущий фрмагмент\n{current_chunk}",
        ),
    ]
)

chain = prompt | structured_llm


class TextToJsonService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.test = TestRepository(db)
        self.question = QuestionRepository(db)
        self.answer = AnswerRepository(db)

    def _split_text(
        self,
        text: str,
    ) -> list[str]:
        spliter = RecursiveCharacterTextSplitter(
            chunk_size=settings.SPLIT_CHUNK_SIZE,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = spliter.split_text(text)
        logger.debug(
            "Text split into chunks",
            extra={
                "meta": {
                    "count_chunks": len(chunks),
                },
            },
        )
        return chunks

    def _try_parse_chunk(
        self,
        chunk_text: str,
        tail: str,
        last_question_last_chunk: str | None,
    ) -> list[Question]:
        chunk_test = None
        for retry_count in range(3):
            logger.debug(
                "Parsing chunk attempt",
                extra={
                    "meta": {
                        "attempt": retry_count + 1,
                    },
                },
            )
            chunk_test = self.parse_chunk(
                chunk_text,
                tail,
                last_question_last_chunk,
            )  # TODO: Тут используется модель
            if chunk_test is not None:
                logger.debug(
                    "Chunk parsed successfully",
                    extra={
                        "meta": {
                            "count_questions": len(chunk_test),
                        },
                    },
                )
                return chunk_test
        logger.warning(
            "Failed to parse chunk after 3 attempts",
            extra={
                "meta": {
                    "chunk_length": len(chunk_text),
                },
            },
        )

    def _delete_dublicate(self, all_questions, new_questions) -> None:
        logger.debug(
            "Try to find duplicate question",
            extra={
                "meta": {
                    "last_question_length": len(all_questions),
                    "new_questions_length": len(new_questions),
                },
            },
        )
        if (
            all_questions != []
            and all_questions[-1].question == new_questions[0].question
        ):
            logger.debug(
                "Deleting duplicate question",
                extra={
                    "meta": {
                        "duplicate_question_text": new_questions[0].question,
                    },
                },
            )
            all_questions.pop()

    def parse_test(self, raw_text: str) -> Test:
        logger.debug(
            "Starting parse test",
            extra={
                "meta": {
                    "text_length": len(raw_text),
                },
            },
        )
        chunks = self._split_text(raw_text)
        all_questions = []
        tail = ""
        last_question = ""
        for i, chunk in enumerate(chunks, 1):
            chunk = chunk.replace("\n\n", "\n")

            chunk_test = self._try_parse_chunk(chunk, tail, last_question)
            new_questions = chunk_test.questions
            self._delete_dublicate(
                all_questions, new_questions
            )  # all_questions is mutable (delete dublicate last question)
            all_questions.extend(new_questions)

            chunk_lines = chunk.split("\n")
            tail = chunk_lines[-1]
            last_question = all_questions[-1].model_dump_json()
            logger.debug(
                "Chunk fully processed",
                extra={
                    "meta": {
                        "chunk_length": len(chunk),
                        "current_chunk": i,
                        "count_chunks": len(chunks),
                        "count_new_questions": len(new_questions),
                    },
                },
            )
        logger.debug(
            "Test parsed successfully",
            extra={
                "meta": {
                    "count_all_questions": len(all_questions),
                },
            },
        )
        test = Test(questions=all_questions)
        return test

    def parse_chunk(
        self,
        chunk_text: str,
        tail: str,
        last_question_last_chunk: str | None,
    ) -> list[Question]:
        logger.debug(
            "Starting LLM call",
            extra={
                "meta": {
                    "last_question": last_question_last_chunk,
                    "tail": tail,
                    "chunk_text": chunk_text,
                },
            },
        )
        result = chain.invoke(
            {
                "first_question": last_question_last_chunk,
                "previous_tail": tail,
                "current_chunk": chunk_text,
            }
        )
        usage = getattr(result, "usage_metadata", {})
        logger.debug(
            "LLM called",
            extra={
                "meta": {
                    "last_question": last_question_last_chunk,
                    "tail": tail,
                    "chunk_text": chunk_text,
                    "input_tokens": usage.get("input_tokens"),
                    "output_tokens": usage.get("output_tokens"),
                },
            },
        )
        return result

    async def create_json_without_answers(
        self,
        file_title: str,
        file: FileService,
        user_id: UUID,
    ) -> UUID:
        logger.info(
            "Creating test by docx file without answers",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "file_title": file_title,
                },
            },
        )
        text = await file.get_text_docx(file_title)
        questions_without_answers: Test = self.parse_test(text)
        test_id = await self._save_test(questions_without_answers, user_id, file_title)
        logger.info(
            "Test created by docx file without answers",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "test_id": str(test_id),
                },
            },
        )
        return test_id

    async def _save_test(
        self,
        test: Test,
        author_id: UUID,
        title: str,
    ):
        logger.debug(
            "Starting save test",
            extra={
                "meta": {
                    "author_id": str(author_id),
                    "title": title,
                },
            },
        )
        data = test.model_dump()
        questions = data.pop("questions")
        data["title"] = title
        tc = TestCreate(**data)
        test_id = await self.test.add_one(tc, author_id)
        for q in questions:
            answers = q.pop("answers")
            qc = QuestionCreate(
                text=q.get("question"),
            )
            question_id = await self.question.add_one(test_id, qc)
            for a in answers:
                ac = AnswerCreate(
                    text=a["text"],
                    isCorrect=False,
                )
                await self.answer.add_one(question_id, ac)
        await self.db.commit()
        logger.debug(
            "Test saved successfully",
            extra={
                "meta": {
                    "author_id": str(author_id),
                    "title": title,
                    "test_id": str(test_id),
                },
            },
        )
        return test_id


def get_text2json_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return TextToJsonService(db)
