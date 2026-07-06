# NeuroTest

Бекенд для сервиса по прохождению тестов с использованием LLM.

## Описание

NeuroTest — это веб-приложение для загрузки тестов в формате .docx, которые автоматически преобразуются в структурированный JSON с помощью LLM. Затем система находит правильные ответы на вопросы. Пользователь также может вручную добавлять, редактировать или удалять тесты, вопросы и ответы через Swagger UI (бэкенд-документацию).

Проект реализован на FastAPI (бэкенд) с интеграцией OpenRouter и Cerebras для работы с моделями, а также Tavily для поисковых запросов.

## Технологии

- **Python 3.11+**
- **FastAPI** — веб-фреймворк
- **LangChain** — интеграция с LLM (Cerebras, OpenRouter)
- **Pydantic Settings** — управление конфигурацией
- **Uvicorn** — ASGI-сервер
- **Docker** — контейнеризация
- **aiofiles** — асинхронная работа с файлами
- **docx2txt** — извлечение текста из `.docx`

## Структура проекта

```text
NeuroTest/
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── routers/          # Эндпоинты API
│   │           ├── __init__.py
│   │           ├── answer.py     # Работа с ответами
│   │           ├── neurotest.py  # Основные эндпоинты (файлы, генерация)
│   │           ├── question.py   # Работа с вопросами
│   │           └── test.py       # Управление тестами
│   ├── core/
│   │   └── settings.py           # Настройки и переменные окружения
│   ├── files/                    # Директория для хранения загруженных файлов
│   ├── infrastructure/           # Вспомогательные утилиты и инфраструктура
│   ├── repositories/             # Работа с хранилищем данных
│   ├── schemas/
│   │   └── test_output.py        # Pydantic-схемы для выходных данных тестов
│   ├── services/                 # Бизнес-логика
│   │   ├── answer.py             # Сервис для работы с ответами
│   │   ├── file.py               # Загрузка, чтение, сохранение файлов
│   │   ├── json2answer.py        # Генерация правильных ответов через LLM
│   │   ├── question.py           # Сервис для работы с вопросами
│   │   ├── test.py               # Сервис для работы с тестами
│   │   └── text2json.py          # Парсинг текста теста в структурированный JSON
│   ├── .dockerignore
│   ├── CHANGELOG.md
│   ├── Dockerfile                # Инструкция для сборки образа
│   ├── main.py                   # Точка входа FastAPI
│   ├── pyproject.toml            # Зависимости и метаданные проекта
│   ├── test_docx2txt.py          # Тесты для парсинга DOCX
│   ├── test_feat.py              # Функциональные тесты
│   └── uv.lock                   # Зафиксированные версии зависимостей
└── frontend/
    └── index.html                # Простой интерфейс для выбора теста и режима
````

## API Эндпоинты

Все эндпоинты имеют префикс `/api/v1`.

### 📁 Файлы и тесты с использованием llm
| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/` | Проверка работы сервиса (возвращает `"Hello from NeuroTest!"`) |
| `POST` | `/files` | Загрузка файла с тестом (`.docx`) |
| `POST` | `/files/json_text` | Создание JSON-файла с вопросами без ответов |
| `POST` | `/files/json_answer` | Создание JSON-файла с вопросами и правильными ответами |
| `GET` | `/files` | Получение списка файлов по типу (`docx`, `text`, `answer`) |

### 📝 Тесты
| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/tests/all` | Получение списка всех тестов |
| `POST` | `/tests/file` | Создание теста из загруженного файла |
| `PUT` | `/tests/file` | Обновление теста из файла |
| `POST` | `/tests/` | Создание нового теста из JSON |
| `GET` | `/tests/{test_id}` | Получение теста по ID |
| `PUT` | `/tests/{test_id}` | Обновление теста по ID |
| `DELETE` | `/tests/{test_id}` | Удаление теста по ID |

### ❓ Вопросы
| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/tests/{test_id}/questions/` | Создание вопроса для указанного теста |
| `GET` | `/tests/{test_id}/questions/` | Получение вопроса по ID (или списка) |
| `PUT` | `/tests/{test_id}/questions/` | Обновление вопроса |
| `DELETE` | `/tests/{test_id}/questions/` | Удаление вопроса |

### ✅ Ответы
| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/tests/{test_id}/answers/` | Добавление ответа на вопрос |
| `GET` | `/tests/{test_id}/answers/` | Получение ответа на вопрос |
| `PUT` | `/tests/{test_id}/answers/` | Обновление ответа |
| `DELETE` | `/tests/{test_id}/answers/` | Удаление ответа |

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/TigranAko/NeuroTest.git
   cd NeuroTest/backend
   ```

2. Создайте файл `.env` в корневой директории (рядом с `backend/`) со следующими переменными:
   ```env
   TAVILY_API_KEY=your_tavily_key
   CEREBRAS_API_KEY=your_cerebras_key
   OPENROUTER_API_KEY=your_openrouter_key
   ```

3. Установите зависимости (рекомендуется использовать `uv`):
   ```bash
   uv sync
   ```

4. Запустите сервер:
   ```bash
   python main.py
   ```
   Сервер будет доступен по адресу `http://localhost:8000`.

### Запуск в Docker

1. Соберите образ:
   ```bash
   docker build -t neurotest-backend ./backend
   ```

2. Запустите контейнер:
   ```bash
   docker run -p 8000:8000 --env-file .env neurotest-backend
   ```

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `TAVILY_API_KEY` | API-ключ для Tavily Search (поиск информации для проверки ответов) |
| `CEREBRAS_API_KEY` | API-ключ для Cerebras (генерация ответов) |
| `OPENROUTER_API_KEY` | API-ключ для OpenRouter (парсинг текста теста) |

## Лицензия

MIT License. Подробнее см. в файле [LICENSE](https://github.com/TigranAko/NeuroTest/blob/main/LICENSE).

## Авторы

- [TigranAko](https://github.com/TigranAko)
- [Maksimushkamolnia2001](https://github.com/Maksimushkamolnia2001)
