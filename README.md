# Тестовое задание 

## О проекте
Репозиторий для выполнения [тестового задания](docs%2FTZ.docx)

## Функционал
Функционал проекта проекта исполнен в соответствии с тестовым заданием

С конечными точками API можно ознакомится после запуска проекта
в OpenAPI-схеме по адресу:
http://localhost:8000/api/schema/swagger-ui/


## Структура проекта
- backend - серверная часть приложения
- desctop - настольное приложение
- frontend - веб-интерфейс

## Используемые компоненты
- Django, DRF - серверная часть веб приложения
- Vue.js, Vuetify - клиенская часть веб приложения
- PyQt6 - настольное приложение

## Требования к переменным окружения
Со структурой переменных коружения можно ознакомиться в файле [docker-compose.yaml](docker-compose.yaml)

## Запуск

1. клонирование репозитория
```commandline
git clone https://github.com/TwentyOn/test_tasks.git -b citadel_task && cd test_tasks
```

2. запуск docker-compose

```commandline
docker compose up -d
```

3. запуск тестов (опционально)
```commandline
docker compose exec -it backend python manage.py test
```
4. Остановка docker-compose
```commandline
python main.py
```