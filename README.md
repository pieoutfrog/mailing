Mailing list management, administration and statistics collection service
Описание

Чтобы удержать текущих клиентов, часто используют вспомогательные, или «прогревающие», рассылки для информирования и привлечения клиентов. В связи с этим был разработан сервис управления рассылками, администрирования и получения статистики.
Установка

    Скачайте проект в домашнюю директорию и установите зависимости командой pip install -r requirements.txt


Перед первым запуском программы:

    Создайте Базу данных (в данной работе используется PostgreSQL) и перейдите в файл .env.sample и пропишите переменные окружения в формате(все данные после "=" в виде примера):

SECRET_KEY='django-secret-key'
DEBUG=True/False

DATABASE_NAME='name_of_db'
DATABASE_USER='db_user'
DATABASE_PASSWORD='your_password'
DATABASE_HOST='127.0.0.1'
DATABASE_PORT=5432

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=email.host.com
EMAIL_PORT=465
EMAIL_HOST_USER=ur_mail@gmail.com/ru
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True/False
EMAIL_USE_SSL=True/False

CACHE_ENABLED=True/False
CACHE_LOCATION=cashe_location://127.0.0.0:6477

    Установите Redis

Выполните миграции


Запустите сервер
python manage.py runserver

    Команда для запуска apscheduler(в другом окне терминала): python manage.py runapscheduler

Работа кода

Для обычного пользователя:

При запуске сервера будет открыта гланая страница со статистикой сайта, а также статьями, связаные с данным сервисом. Перед использованием возможностей сервиса, придется зарегестрироваться, а также пройти верификацию почты. После верификации почты будут доступны такие возможности как создание/просмотр/редактирование/удаление своих клиентов, сообщений и рассылок, и также просмотр логгов по отправке рассылки.

Для суперюзера/менеджера(группа-managers):

Та же главная страница, также возможность управлять активность пользователя сервера и статусом рассылки
Для завершения работы

В терминале, где запущен сервер, прожать Ctrl + C
