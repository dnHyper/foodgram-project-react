[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org) [![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org) [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org) [![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com) [![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org) [![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)  [![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)](https://www.figma.com/file/HHEJ68zF1bCa7Dx8ZsGxFh/Продуктовый-помощник-(Final)) [![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)](https://github.com) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)

# Яндекс.Практикум. Спринт 17

#### Название: praktikum_new_diplom
#### Папка: foodgram-project-react
#### Группа: когорта 25
#### Когда: 2022 год
#### Кто: Алексей Ерёменко ( https://github.com/dnHyper/ )
#### Версия: 1.0ß

# Описание

Исходный код фронт/бэкенда для онлайн-сервиса «Продуктовый помощник».

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

В данный момент проект запущен на сервере и работает по адресу: http://margdoof.ru
Посмотреть документацию можно по адресу: http://margdoof.ru/api/docs/redoc.html

# Подготовка и запуск проекта локально

Склонировать репозиторий на локальную машину:
```s
git clone git@github.com:dnHyper/foodgram-project-react.git
```
Перейти в папку с проектом
```s
cd папка_куда_склонировали/foodgram-project-react
```
Создать виртуальное окружение и обновить pip
```s
python -m venv venv
source venv/Scripts/activate
pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:

```s
pip install -r backend/foodgram_project/requirements.txt
```

Из папки backend/foodgram_project/ выполнить миграции:

```s
python manage.py migrate
```
После этого вы можете работать с api локально обращаясь по адресу: http://127.0.0.1:8000/api/

# Запуск проекта локально в контейнере:

Для этого вам необходимо установить и запустить docket  https://www.docker.com/get-started/

После этого, из консоли, перейти в папку infra и выполнить команду:
```s
docker-compose up -d
```
Запустится рабочий образ сайта по локальным адресам:
- к фронтенду: http://127.0.0.1/
- к документации: http://127.0.0.1/api/docs/redoc.html
- к API: http://127.0.0.1/api/

# Примечания:
В папке backend/media/data/ содержатся тестовые данные в формате json для начального наполнения сайта. При загрузке через git actions на сервер эти данные автоматически загружаются в БД, после чего папка удаляется.

Если вы планируете разворачивать данный проект на сервере, то рекомендую загрузить в первую очередь папку docs - для доступа к справке по строению проекта, а так-же содержимое папки server, в которой содержится:
docker-composer.yml - конфиг для запуска контейнеров
ndinx.conf - конфиг для работы nginx

# Изменения версий:
(0.1)
- Добавлены модели:
+ User
+ Recipe
- Добавлены сериализаторы для моделей
- Добавлена логика для:
+ Recipe
+ Ingridient
- Добавлены пути

(0.2)
- Небольшие исправления настроек
- Небольшие исправления сериализаторов
- Добавлена возможность скачивать PDF-файл ингридиентов рецептов
- Добавлена админка
- Внесены изменения в docker-composer и nginx config для работы админки
- Небольшие правки в пользовательском сериализаторе
- Изменение работы сохранения изображений (теперь сохраняются на сервере а не в БД)

(0.3)
- Небольшие изменения в админке (добавлено отображение количества избранных рецептов)
- Изменения настроек в setup.cfg
- Правки импортов в соответствии с PEP8
- Добавлен workflows для тестирования на стороне GIT и загрузки на Docker
- Добавлена возможность подписываться на пользователей
- Вынесение фильтрации в отдельный файл (filter.py)
- Добавление фильтрации по избранным и добавленному в корзину
- Незначительные изменения по коду

(0.5)
- Изменения в workflows: добавлена загрузка на Yandex

(0.6) - Правки после первого ревью

(0.7) - Правки после второго ревью
- Добавлена команда import_to_db для импорта в БД ингредиентов и тэгов

(0.8) - Правки после третьего ревью
- Исправлена ошибка: отписка от пользователя работала некорректно
- Исправлена ошибка: изменение рецептов завершалось с ошибкой 500
- Исправлена проверка количества ингридиента
- Небольшие изменения в модели рецептов
- Произведен сброс миграций
- Небольшие изменения в импортах
- Исправлен nginx.conf
- Добавлен docker-composer-server.yml для работы на сервере
- Добавлена версия в docker-compose.yml
