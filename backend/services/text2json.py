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
            chunk_size=4000,
            separators=["\n\n", "\n", " ", ""],
        )
        return spliter.split_text(text)

    def _try_parse_chunk(
        self,
        chunk_text: str,
        tail: str,
        last_question_last_chunk: str | None,
    ) -> list[Question]:
        chunk_test = None
        for retry_count in range(3):
            print(f"\nОтправляется запрос {retry_count + 1}\n")
            chunk_test = self.parse_chunk(
                chunk_text,
                tail,
                last_question_last_chunk,
            )  # TODO: Тут используется модель
            if chunk_test is not None:
                return chunk_test
        print("ERROR: Не получилось обработать чанк\n\n", chunk_text)

    def _delete_dublicate(self, all_questions, new_questions) -> None:
        if (
            all_questions != []
            and all_questions[-1].question == new_questions[0].question
        ):
            print("\nУдаление дубликата вопроса при соединении чанков")
            print(all_questions[-1], "\n", new_questions[0])
            all_questions.pop()

    def parse_test(self, raw_text: str) -> Test:
        chunks = self._split_text(raw_text)
        all_questions = []
        tail = ""
        last_question = ""
        for i, chunk in enumerate(chunks, 1):
            chunk = chunk.replace("\n\n", "\n")
            print(f"Чанк: {i}/{len(chunks)}\nДлина чанка {len(chunk)} символов")

            chunk_test = self._try_parse_chunk(chunk, tail, last_question)
            new_questions = chunk_test.questions
            print("Новые вопросы", new_questions)
            self._delete_dublicate(
                all_questions, new_questions
            )  # all_questions is mutable (delete dublicate last question)
            all_questions.extend(new_questions)

            print(f"Добавлено {len(new_questions)} вопросов")
            chunk_lines = chunk.split("\n")
            tail = chunk_lines[-1]
            print("Последния  строка", tail)
            last_question = all_questions[-1].model_dump_json()
            print("Последний  вопрос", last_question)
        print()
        print(all_questions)
        test = Test(questions=all_questions)
        return test

    def parse_chunk(
        self,
        chunk_text: str,
        tail: str,
        last_question_last_chunk: str | None,
    ) -> list[Question]:
        result = chain.invoke(
            {
                "first_question": last_question_last_chunk,
                "previous_tail": tail,
                "current_chunk": chunk_text,
            }
        )
        return result

    async def create_json_without_answers(
        self,
        file_title: str,
        file: FileService,
        user_id: UUID,
    ) -> UUID:
        text = await file.get_text_docx(file_title)
        questions_without_answers: Test = self.parse_test(text)
        test_id = await self._save_test(questions_without_answers, user_id)
        return test_id

    async def _save_test(
        self,
        test: Test,
        author_id: UUID,
    ):
        data = test.model_dump()
        questions = data.pop("questions")
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
        return test_id


def get_text2json_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return TextToJsonService(db)
