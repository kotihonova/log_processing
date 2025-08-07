Перед запуском скрипта необходимо установить использующиеся в проекте зависимости с помощью команды

`pip install -r requirements.txt`

Если вы не хотите их устанавливать глобально на свой компьютер, рекомендую сначала создать и активировать виртуальное окружение, только потом их устанавливать

`python3 -m venv test_env`

`source test_env/bin/activate  # Linux/macOS
.\test_env\Scripts\activate   # Windows`

Запустить скрипт можно из корневой директории с помощью команды, можно ввести несколько имен файлов, только одну дату в формате YYYY-MM-DD, название отчета -- 'average'. Все аргументы вводятся **без кавычек**.

`python3 src/logparser.py --filename example2.log -r average -d 2025-06-22`

Перед запуском тестирования необходимо выполнить команду в корневой директории проекта:

`export PYTHONPATH=. # Linux/macOS
$env:PYTHONPATH = "." # Windows PowerShell
set PYTHONPATH=. # Windows cmd`

Запустить тесты с помощью команды

`pytest --cov=src tests/`

Примеры `example1.log` и `example2.log` взяты из тестового задания, хранятся в корневой директории проекта.