lint: # запуск линтера
	poetry run flake8 quiz_bot

install: # установка пакета после клонирования репозитория или удаления зависимостей
	poetry install

run: # запуск
	poetry run python quiz_bot/main.py
