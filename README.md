# Pitchford Support

Система обработки клиентских обращений из нескольких каналов (Viber, Telegram, Email)
с единым интерфейсом оператора в виде PWA.

Проект находится в активной разработке. Реализован каркас бэкенда и инфраструктура
для локальной разработки; приём сообщений из каналов и операторский интерфейс — следующие шаги.

## Стек

- **Backend:** Python 3.13, FastAPI, Pydantic Settings, structlog
- **База данных:** PostgreSQL 17 (план: SQLAlchemy 2 + Alembic)
- **Очередь:** Redis 7 (план: Celery)
- **Почта (dev):** Mailpit
- **Frontend:** Vue 3 + Pinia + Vite (план)

## Требования

- Docker и Docker Compose
- [uv](https://docs.astral.sh/uv/) — управление Python-окружением и зависимостями

Python отдельно устанавливать не нужно: версия закреплена в `backend/.python-version`,
`uv` скачает её автоматически при первом запуске.

## Быстрый старт

### 1. Настройки окружения

```bash
cp .env.example .env
```

Для реального окружения замените `SECRET_KEY` на случайное значение:

```bash
openssl rand -hex 32
```

`.env` в git не попадает. Все доступные переменные описаны в `.env.example`.

### 2. Инфраструктура

```bash
docker compose --env-file .env -f infra/docker-compose.yml up -d
docker compose --env-file .env -f infra/docker-compose.yml ps
```

Поднимаются:

| Сервис | Адрес | Назначение |
|---|---|---|
| PostgreSQL | `localhost:5432` | база данных |
| Redis | `localhost:6379` | очередь и real-time (в следующих шагах) |
| Mailpit SMTP | `localhost:1025` | приём писем в разработке |
| Mailpit UI | http://localhost:8025 | просмотр писем |

### 3. Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

### 4. Проверка

```bash
curl -s http://localhost:8000/healthz
# {"status":"ok"}
```

Swagger UI: http://localhost:8000/docs

## Полезные команды

```bash
# из backend/
uv run pytest -q          # тесты
uv run ruff check .      # линтер
uv run ruff format .     # форматирование

# из корня репозитория
docker compose --env-file .env -f infra/docker-compose.yml logs -f db
docker compose --env-file .env -f infra/docker-compose.yml down
```

Остановка с удалением данных БД и Redis (осторожно, dev-only):

```bash
docker compose --env-file .env -f infra/docker-compose.yml down -v
```

## Структура проекта

```
backend/
  app/
    core/          # конфигурация, логирование
    main.py        # создание приложения, health-эндпоинты
  tests/           # тесты
  alembic/         # миграции (следующий шаг)
infra/
  docker-compose.yml  # PostgreSQL, Redis, Mailpit
frontend/          # PWA-интерфейс (следующие шаги)
```

## Конфигурация

- Единственный источник настроек — переменные окружения и `.env` в корне репозитория.
- Локальные переопределения — через переменные окружения (они имеют приоритет над `.env`).
- Секреты не коммитятся. `SECRET_KEY` должен быть случайным и достаточно длинным.
- Compose подставляет значения из `.env` при разборе `infra/docker-compose.yml`.
  Без `.env` обязательные переменные вызовут ошибку на старте — это ожидаемое
  поведение (fail-fast).

## Статус

- [x] Каркас FastAPI, конфигурация, структурные логи
- [x] Dev-инфраструктура (PostgreSQL, Redis, Mailpit)
- [x] Health-check и smoke-тест
- [ ] Подключение к БД, модели `User`/`Team`, миграции
- [ ] Аутентификация и роли
- [ ] Тикеты, сообщения, внутренние заметки
- [ ] Каналы: Viber, Telegram, Email
- [ ] Real-time и SLA
- [ ] PWA-интерфейс оператора

## Диагностика

**`ValidationError: ... field required` при старте** — не создан `.env` или в нём
не хватает переменных. Выполните `cp .env.example .env`.

**`port is already allocated`** — порт занят другим процессом. Измените порт
в `.env` (`POSTGRES_PORT`, `REDIS_PORT`, `MAILPIT_SMTP_PORT`, `MAILPIT_UI_PORT`).

**Postgres не принимает новый пароль** — переменные `POSTGRES_*` применяются только
при инициализации пустого volume. Для сброса: `docker compose ... down -v`.
