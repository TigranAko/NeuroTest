import time

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from langchain_tavily import TavilySearch
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class TavilyConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
    )
    TAVILY_API_KEY: SecretStr
    openrouter_api_key: SecretStr


config = TavilyConfig()


# ---------- Модели ----------
class Answer(BaseModel):
    text: str
    isCorrect: bool


class QuestionOutput(BaseModel):
    question: str
    answers: list[Answer]


class TestOutput(BaseModel):
    questions: list[QuestionOutput]


# ---------- Инструменты ----------
search = TavilySearch(
    max_results=2,
    search_depth="basic",
    tavily_api_key=config.TAVILY_API_KEY.get_secret_value(),
)

llm = ChatOpenRouter(
    api_key=config.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/free",
    temperature=0,
    model_kwargs={"response_format": {"type": "json_object"}},
)

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


def format_answers(answers: list[Answer]) -> str:
    return "\n".join(f"{i}. {a.text}" for i, a in enumerate(answers, 1))


# chain = (
#     RunnablePassthrough.assign(search_results=lambda x: search.invoke(x["question"]))
#     | RunnablePassthrough.assign(
#         formatted_answers=lambda x: format_answers(x["answers"]),
#         search_results_text=lambda x: "\n".join(
#             r["content"] for r in x["search_results"]
#         ),
#     )
#     | RunnablePassthrough.assign(
#         result=lambda x: (
#             prompt.partial(format_instructions=parser.get_format_instructions())
#             | llm
#             | parser
#         ).invoke(
#             {
#                 "question": x["question"],
#                 "answers": x["formatted_answers"],
#                 "search_results": x["search_results_text"],
#             }
#         )
#     )
#     | RunnableLambda(lambda x: x["result"])
# )
# chain = RunnableLambda(process_single_questions)


def process_single_questions(question_text: str, answers: list[str]) -> QuestionOutput:
    search_results = search.invoke(question_text)
    print(search_results, type(search_results))
    search_text = "\n".join(r["content"] for r in search_results.get("results"))

    formatted_answers = "\n".join(f"{i}) {a}" for i, a in enumerate(answers, 1))
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


def process_test(input: dict, max_requests_per_day=50) -> TestOutput:
    questions_data = input["questions"]
    output_questions = []
    requests_today = 0
    for idx, q in enumerate(questions_data):
        if requests_today >= max_requests_per_day:
            print(
                f"Достигнут дневной лимит ({max_requests_per_day}). Продолжите завтра."
            )
            break
        print(f"Вопрос {idx + 1}/{len(questions_data)}...")

        result = process_single_questions(q["question"], q["answers"])
        output_questions.append(result)
        requests_today += 1
        time.sleep(1)
    return TestOutput(questions=output_questions)


# ---------- Использование ----------
if __name__ == "__main__":
    # Пример исходного JSON (как в вопросе)
    input_json = {
        "questions": [
            {
                "question": "1. Матрица, размером (1х5) называется..........",
                "answers": [
                    {"text": "матрица-столбец"},
                    {"text": "единичная"},
                    {"text": "матрица-строка"},
                ],
            },
            {
                "question": "2. Матрица (1 0 0 0 5 0 0 0 9) называется...",
                "answers": [
                    {"text": "Единичная"},
                    {"text": "Нулевая"},
                    {"text": "Диагональная"},
                    {"text": "Симметричная"},
                ],
            },
        ]
    }

    test_in = input_json  # TestInput(**input_json)
    test_out = process_test(test_in)
    print(test_out.model_dump_json(indent=2))
    with open("./files/test_answer.json", "w", encoding="utf-8") as file:
        file.write(test_out.model_dump_json(indent=4))
