# Тестовое задание 

## О проекте
Поисковик по текстам документов (Python, FastAPI, PostgreSQL, ElasticSearch)

## Функционал
Функционал проекта представлен в виде двух конечных точек:
- http://localhost:8000/documents - конечная точка для отправки текстового
поискового запроса и получения ответа
- http://localhost:8000/documents/{id}/ - конечная точка для удаления документа из 
БД и индекса эластики
- Реализованы базовые тесты конечных точек с помощью pytest. Для тестов создаётся 
тестовая БД (SQLite), тестовый индекс в эластике.


## Структура проекта
- backend - функционал работы с базами данных
- models - модели SQLAlchemy
- routers - определение конечных точек API
- scripts - вспомогательные скрипты для заполнения данными базы данных
- tests - директория с тестами
- main.py - точка входа
- schemas.py - модели pydantic
- settings.py - модуль конфигурации

## Необходимые компоненты
- Docker
- Docker Compose

## Требования к переменным окружения
С переменными окружения можно ознакомится в параметрах конфигурации 
[docker-compose.yaml](docker-compose.yaml)

Особое внимание требуется уделить переменным ELASTIC_HOST, ELASTIC_API_KEY - здесь
 должны быть ваши параметры от ElasticSearch

## Запуск
1. клонирование репозитория
```commandline
git clone https://github.com/TwentyOn/test_tasks.git -b analytical_sol_task && cd test_tasks
```
1. запуск docker-compose
```commandline
docker compose up -d
```
2. создание миграции БД
```commandline
docker compose exec backend alembic revision --autogenerate -m 'initial'
```
3. применение миграций
```commandline
docker compose exec backend alembic upgrade head
```
4. заполнение данных
```commandline
docker compose exec backend python -m scripts.startup
```

5. тесты
```commandline
docker compose exec backend pytest
```

После выполнения вышеуказанных инструкции с API можно работать по адресу:
http://localhost:8000/docs

Остановка docker-compose: 
```commandline
docker compose stop
```