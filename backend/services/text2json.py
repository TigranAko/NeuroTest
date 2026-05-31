import docx2txt
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenrouterConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    openrouter_api_key: SecretStr


class Answer(BaseModel):
    text: str = Field(description="Текст варианта ответа")


class Question(BaseModel):
    question: str = Field(description="Текст вопроса")
    answers: list[Answer] = Field(
        description="Список  возможных ответов (без указания правильных)"
    )


class Test(BaseModel):
    questions: list[Question] = Field(description="Список всех вопросов теста")


config = OpenrouterConfig()

llm = ChatOpenRouter(
    api_key=config.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/free",
    temperature=0.1,
    max_retries=3,
    timeout=2 * 60 * 1000,  # две минуты
)

structured_llm = llm.with_structured_output(Test)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Ты - строгий парсер тестов. "
            "Твоя задача - находить вопросы и варианты ответов. "
            "Игнорируй последний вопрос в фрагменте",
        ),
        (
            "human",
            "Хвост предыдущего чанка:\n{previous_tail}\n\n"
            "Текущий фрмагмент\n{current_chunk}",
        ),
    ]
)

chain = prompt | structured_llm


class TextToJsonService:
    def parse_test(self, raw_text: str) -> Test:
        spliter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = spliter.split_text(raw_text)
        all_questions = []
        tail = ""
        for i, chunk in enumerate(chunks, 1):
            chunk = chunk.replace("\n\n", "\n")
            print(f"Чанк: {i}/{len(chunks)}\nДлина чанка {len(chunk)} символов")
            chunk_test = self.parse_chunk(chunk, tail)  # TODO: Тут используется модель
            new_questions = chunk_test.questions
            print("Новые вопросы", new_questions)
            all_questions.extend(new_questions)
            print(f"Добавлено {len(new_questions)} вопросов")
            chunk_lines = chunk.split("\n")
            tail = (
                "\n".join(chunk_lines[-5:])
                if len(chunk_lines) > 5
                else "\n".join(chunk_lines)
            )
            print("Обрезанный конец", tail)
            # TODO: нужно выбрать последний вопрос предыдущего чанка
        # TODO: нужо обрабатыввать последний вопрос
        print()
        print(all_questions)
        test = Test(questions=all_questions)
        return test

    def parse_chunk(self, chunk_text: str, tail: str) -> list[Question]:
        result = chain.invoke(
            {
                "previous_tail": tail,
                "current_chunk": chunk_text,
            }
        )
        return result


def get_text2json_service():
    return TextToJsonService()
