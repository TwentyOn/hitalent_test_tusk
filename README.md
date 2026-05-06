# Тестовое задание 

## О проекте
Репозиторий для выполнения [тестового задания](docs%2FTZ.docx)

## Функционал
Функционал проекта проекта исполнен в соответствии с тестовым заданием

После запуска проекта:
 - OpenAPI-схема доступна по адресу:
http://localhost:8000/api/schema/swagger-ui/
 - фронтенд доступен по адресу: http://localhost:3000

Более детальная информация доступна в [docker-compose.yaml](docker-compose.yaml)


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

## Запуск веб приложения

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

## Запуск настольного приложения
1. перейти в директорию приложения
```commandline
cd desktop
```
2. создать и активировать вирутальное окружение
```commandline
python -m venv .venv && .venv\Scripts\activate
```
3. установить зависимости
```commandline
pip install -r requirements.txt
```
4. запустить приложение
```commandline
python main.py
```
5. деативация окружения
```commandline
deativate
```