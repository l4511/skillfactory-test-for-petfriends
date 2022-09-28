# skillfactory-test-for-petfriends

Сборник тестов для тестирования сайта petfriends.skillfactory.ru.
Все тестовые задачи можно выполнять по отдельности , при соблюдении необходимых условий для каждого из них.
Предпочтительнее запускать все тесты разом, тогда все работает корректно и правильно.

В директории /tests располагается файл с тестами.
В директории /tests/images лежат картинки для теста добавления питомца и теста добавления картинки.
В корневой директории лежит файл settings.py - содержит информацию о валидном логине и пароле.
В корневой директории лежит файл api.py, который является библиотекой к REST api сервису веб приложения Pet Friends.
Библиотека api написана в классе, что соответствует принципам ООП и позволяет удобно пользоваться её методами. При инициализации библиотеки объявляется переменная base_url которая используется при формировании url для запроса.
