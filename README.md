
Программка для автоматической регистрации в вайфай-сети Южно-Уральского государственного университета.

## Назначение

Сеть SUSU_EDU при подключении к ней редиректит со всех страниц на страницу авторизации для ввода логина и пароля,
а затем требует повторной авторизации каждые полчаса.
Этот скрипт спрашивает логин и пароль при первом запуске и регулярно пытается авторизоваться в сети, чтобы избавить пользователя от необходимости делать это.
Его можно легко настроить для работы с другими сетями, использующими Cisco Web Authentication.

## Использование

Если есть питон, то запустить можно просто командой `python autoregistrator.py`. Если его нет, то можно взять exe-файл [здесь](https://github.com/igor-shevchenko/autologin/releases).

## Зависимости

* [requests](http://python-requests.org)
* [py2exe](http://www.py2exe.org/)

## Лицензия

MIT

## Автор

Игорь Шевченко, mail@igorshevchenko.ru