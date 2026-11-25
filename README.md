# Trige Support

Система обработки клиентских обращений

## Стек

- **Backend:** Python 3.13, FastAPI, Pydantic Settings, structlog
- **База данных:** PostgreSQL 17, SQLAlchemy 2 + Alembic
- **Очередь:** Redis 7, Celery/Taskiq
- **Почта (dev):** Mailpit
- **Frontend:** Vue 3 + Pinia + Vite (план)

## Требования

- Docker и Docker Compose
- [uv](https://docs.astral.sh/uv/) — управление Python-окружением и зависимостями

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

