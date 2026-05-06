# Тестовое задание 

## О проекте
Репозиторий для выполнения [тестового задания](docs%2FTZ.docx)

## Функционал
Функционал проекта проекта исполнен в соответствии с тестовым заданием

После запуска проекта:
 - OpenAPI-схема доступна по адресу:
http://localhost:8000/api/schema/swagger-ui/
 - фронтенд доступен по адресу: http://localhost:3000

К БД можно подключиться с порта 5433, параметры подключения можно найти
в параметрах окружения
[docker-compose.yaml](docker-compose.yaml)


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
docker compose stop
```

## Запуск настольного приложения
### Способ 1 (только windows)
1. Запустить исполняемый файл [main.exe](desktop%2Fbuild%2Fexe.win-amd64-3.14%2Fmain.exe)
по пути desktop/build/exe.win-amd64-3.14
### Способ 2
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

## Демонстрация работы
1. Окно регистрации ![register.png](docs%2Fregister.png)
2. Форма входа ![login.png](docs%2Flogin.png)
3. Интерфейс личного кабинета ![profile_view.png](docs%2Fprofile_view.png)
4. главное окно настольного приложения 

![desktop.png](docs%2Fdesktop.png)
5. окно подключения настолько приложения

![desktop.png](docs%2Fdesktop.png)