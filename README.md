# ReadMe
## python_dev_Malay_Alexandr
Приложения на DRF для создания 2 датасетов из 2 баз данных

# Установка проекта
## Скачайте свой проект zip архивом, либо склонируйте репозиторий при помощи git clone
```
git clone https://github.com/SavageGinny/python_dev_Malay_Alexandr.git
```
## Установка библиотек и виртуального окружение
### Перейдите в папку проекта:
```
cd python_dev_Malay_Alexandr
```
### Запустите виртуальное окружение:
```
python -m venv venv
```
### Обновите pip до последней версии
```
python.exe -m pip install --upgrade pip
```
### Установите все необходимые библиотеки
```
pip install django djangorestframework django-crispy-forms crispy-bootstrap5 django-select2
```
## Запуск проекта
### Проведите миграции
```
python manage.py makemigrations
```
```
python manage.py migrate
```
### По желанию, создайте суперпользователя
```
python manage.py createsuperuser
```
### Запустите приложение
```
python manage.py runserver
```

# Инструкция пользователя
## Главная страница
После перехода по ссылке `http://127.0.0.1:8000/` на главной странице вы увидете поле ввода|выбора. После того, как вы выберите логин юзера, на которого вы хотите получить датасеты, нажимайте "Показать данные". После этого на этой же странице появятся таблицы и кнопки "Скачать датасет" под ними. При нажатии на них, вы сможете скачать необходимый датасет в csv формате.

## API
### API запросы проделанны в таком виде:
```
GET http://127.0.0.1:8000/api/comments?login=<userloggin>
```
```
GET http://127.0.0.1:8000/api/general?login=<userloggin>
```
где `<userloggin>` - логин юзера, на которого собираются данные. Например:
```
GET http://127.0.0.1:8000/api/comments?login=user1
```
```
GET http://127.0.0.1:8000/api/general?login=user1
```
### Так же можно просмотреть данные и в браузере в виде JSON, только с интефейсом от DRF. Для этого нужно ввести тоже самое, только без GET:
```
http://127.0.0.1:8000/api/comments?login=<userloggin>
```
```
http://127.0.0.1:8000/api/general?login=<userloggin>
```
# Условие задачи:
## 1. Создать две sqlite базы данных (sqlite - опционально, также возможны mysql, postrges) - схемы приложены к заданию.
## 2. В одной бд (db1_scheme.png) создать три таблицы - post, author и blog.
- В первой должна содержаться информация о посте (id, header, text, author_id, blog_id).
- Во второй информация об авторе (id, login, email).
- В третьей информация о блоге (id, owner_id, name, description).
- таблица post связана через внешние ключи с таблицами user (author_id) и blog (blog_id),
- таблица blog связана через внешний ключ с таблицей user (owner_id)
![db1_scheme](https://github.com/user-attachments/assets/e9e50a99-78d7-4e5d-9494-f83f703352a7)

## 3. Во второй бд (db2_scheme.png) создать три таблицы - logs, space_type и event_type.
### В первой таблице будут содержаться действия пользователя (id, datetime,user_id, space_type_id (внешний ключ для связи с таблицей space_type), event_type_id (внешний ключ для связи с таблицей event_type), space_id (id пространства, в котором было совершено действие) user_id может содержать идентификаторы пользователи из разных БД, предполагается что в том числе и из нашей первой созданной
### space_type содержит типы пространств где пользователь может совершать действия, пространства могут быть такими:

- global
- blog
- post

### event_type содержит типы действий:

- login
- comment
- create_post
- delete_post
- logout

### Предполагается, что действия типа login, logout выполняются в пространстве global, действия типа create_post, delete_post выполняются в пространстве blog, действие comment выполняется в пространстве post 

![db2_scheme](https://github.com/user-attachments/assets/f9acc7f9-197b-44e3-9dab-2c400721b36c)

## 4. На языке python с использованием любых библиотек необходимо реализовать функционал подключения к двум базам данных и формирования по логину пользователя двух датасетов - comments и general

### Первый содержит следующую информацию (ниже перечислены колонки итоговой таблицы):

- логин пользователя,
- заголовок поста (header) к которому он оставлял комментарии
- логин автора поста
- кол-во комментариев

### Второй содержит общую информацию о действиях пользователя (ниже перечислены колонки итоговой таблицы):

- дата
- кол-во входов на сайт
- кол-вы выходов с сайта
- кол-во действий внутри блога

## 5. Датасеты должны формироваться и отдаваться по api, необходимо поднять веб сервер и реализовать два ендпоинта:

- api/comments
- api/general

### Логин пользователя передавать необходимо через get-параметр
## 6. По результатам задания должен быть предоставлен репозиторий с артефактами работы, названный по паттерну python_dev_<фамилия>_<имя> - передать можно или ссылку на гитхаб/гитлаб, или архив
### P.S. Если вы нашли в задании какие-то нестыковки/несоответствия, исправьте их так как считаете правильным и в readme.md файле опишите то что сделали.
# О правках в условии
## Дополнительное поле в таблице logs
В данную таблицу было добавлено поле - space_id, в котором хранится id пространства, в котором происходили действия: если в global - space_id = None, blog - id блога, post - id поста

## Почему выбранно такое решение:
Изначально, была идея в первой БД создать таблицу comment, в которой бы хранились данные о комментариях. В процессе стало ясно, что одно из заданий с данной таблицой решается без использования таблицы logs во второй БД. Основная задача - сбор данных при помощи коннекта двух таблиц, поэтому было решено создать поле space_id, по которому приложение достаёт название поста и его автора.

# О выбранном инструментарии
- Django - мощный фреймворк для создания веб приложений. Он надёжный, масштабируемый и легок в изучении, благодаря большому количеству информации по нему в интернете, начиная с основной документации, заканчивая статьями на Habr и ответам на StackOverfow. Но основной причиной было то, что у него есть встроенная ORM система, что помогает легко работать с базами данных.

- Django Rest Framework - дополнение к Django, необходимый для создания API.

Остальные библиотеки (django-crispy-forms, crispy-bootstrap5, django-select2) использовались для создания формы ввода|выбора логина юзера на главной странице
