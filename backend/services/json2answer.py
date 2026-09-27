from time import sleep
from typing import Annotated, Literal
from uuid import UUID

from core.database import get_db
from core.settings import settings
from fastapi import Depends
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from repositories.answer import AnswerRepository
from repositories.question import QuestionRepository
from repositories.test import TestRepository
from schemas.answer import AnswerCreate
from schemas.question import QuestionCreate
from schemas.test import TestCreate
from schemas.test_output import QuestionOutput, TestOutput
from sqlalchemy.ext.asyncio import AsyncSession

# ---------- Инструменты ----------
search = TavilySearch(
    max_results=2,
    search_depth="basic",
    tavily_api_key=settings.TAVILY_API_KEY.get_secret_value(),
)


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
        base_url="https://api.cerebras.ai/v1/",
        api_key=settings.CEREBRAS_API_KEY,
        model="gpt-oss-120b",  # Add other models
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
        timeout=180,
    )


llm = get_llm_chat()

parser = PydanticOutputParser(pydantic_object=QuestionOutput)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Ты — эксперт, определяющий правильные ответы на вопросы.
Используй ТОЛЬКО результаты поиска, приведённые ниже. Если информации недостаточно, отвечай на основе общеизвестных фактов, но не выдумывай.
Верни JSON с ответом строго по инструкции.

{format_instructions}

Вопрос:
{question}

Варианты ответа:
{answers}""",
        ),
        (
            "user",
            "Результаты поиска:\n{search_results}\n\nОпредели правильные варианты. Если их несколько, отметь все.",
        ),
    ]
)


class JsonToAnswerService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.test = TestRepository(db)
        self.question = QuestionRepository(db)
        self.answer = AnswerRepository(db)

    def process_single_questions(
        self,
        question_text: str,
        answers: list[dict[Literal["text"], str]],
    ) -> QuestionOutput:
        formatted_answers = "\n".join(
            f"{i}) {a.get('text')}" for i, a in enumerate(answers, 1)
        )
        search_results = search.invoke(question_text)
        print(search_results, type(search_results))
        search_text = "\n".join(r["content"] for r in search_results.get("results"))

        chain = prompt | llm | parser
        result = chain.invoke(
            {
                "question": question_text,
                "answers": formatted_answers,
                "search_results": search_text,
                "format_instructions": parser.get_format_instructions(),
            }
        )
        return result

    def process_test(self, input: dict, author_id: UUID) -> TestOutput:
        questions_data = input["questions"]
        output_questions = []
        for idx, q in enumerate(questions_data):
            print(f"Вопрос {idx + 1}/{len(questions_data)}...")
            sleep(2)
            result = self.process_single_questions(q["question"], q["answers"])
            print(result, type(result))
            output_questions.append(result)
        return TestOutput(questions=output_questions, author_id=author_id)

    async def create_json_answers(
        self,
        test_id: UUID,
        author_id: UUID,
    ) -> UUID:
        # data = await file.reed_json(file_title + "_text")
        # READ TEST , need optimize
        data = {"questions": []}
        questions = list(await self.question.get_by_test(test_id))
        for question in questions:
            new_question = {
                "question": question.text,
                "answers": [],
            }
            answers = list(await self.answer.get_by_question(question.id))
            for answer in answers:
                new_question["answers"].append({"text": answer.text})
            data["questions"].append(new_question)

        answers: TestOutput = self.process_test(data, author_id=author_id)
        # answers_str = answers.model_dump_json(indent=4)
        test_id = await self._save_test(answers, author_id)
        # await file.create_json(file_title + "_answers", answers)
        return test_id

    async def _save_test(
        self,
        test: TestOutput,
        author_id: UUID,
    ):
        data = test.model_dump()
        questions = data.pop("questions")
        tc = TestCreate(**data)
        # TODO: update test and no recreate dublicate test
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
                    isCorrect=a["isCorrect"],
                )
                await self.answer.add_one(question_id, ac)
        await self.db.commit()
        return test_id


def get_json2answer_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return JsonToAnswerService(db)
