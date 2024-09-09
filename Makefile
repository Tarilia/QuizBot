lint: # запуск линтера
	poetry run flake8 disease-prediction

install: # установка пакета после клонирования репозитория или удаления зависимостей
	poetry install
