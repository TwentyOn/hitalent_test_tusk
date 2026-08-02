# Тестовое задание

## Структура проекта
- task1 - директория задания 1
  - docs - файлы аннотаций
- task2 - директория задания 2
  - docs - файлы аннотаций, изображений, выходных
  - output - директория для выходных файлов

## Функционал
Весь функционал проекта выполнен встроенными модулями python

- Задание 1
  - script1.py - результаты выводятся в консоль
  - script2.py - результаты выводятся в консоль
  - script3.py - результаты выводятся в консоль
  - script4.py - результирующие файлы записываются в task1/docs/
- Задание 2
  - script1
    - updated_annotations.json записывается по пути task2/output/annotations/updated_annotations.json
    - изображения по классам записываются по пути task2/output/images/
  - script2.py
    - результаты выводятся в консоль
    - файл dataset_report.json записывается по пути 
    task2/output/dataset_report.json
  - script3.py - YOLO-аннотации записываются в дирректорию: 
  task2/output/yolo_dataset/

## Необходимые компоненты
- Среда python

## Запуск
1. Клонование репозитория:
```commandline
git clone https://github.com/TwentyOn/test_tasks.git -b datalight_task && cd test_tasks
```
2. Запуск скриптов

Каждый скрипт запускается отдельно по команде:
```commandline
python -m task#.script#
```
где знак # номер задания и скрипта

Например:
```commandline
python -m task1.script1
```
