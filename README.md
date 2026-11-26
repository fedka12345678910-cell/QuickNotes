# QuickNotes

Веб-сервис быстрых учебных заметок (дисциплина «Инструментальные средства информационных систем», ФГБОУ ВО ИрГУПС).

**Автор:** Дыбин Фёдор Александрович, гр. ИС.1-23-2

## Состав проекта
- `app.py` — веб-приложение на Flask (HTML-интерфейс и REST API)
- `requirements.txt` — зависимости Python (`flask`, `pytest`)
- `tests/test_simple.py` — базовые модульные тесты (деление на ноль, чёт/нечёт, валидация)
- `tests/test_notes.py` — тесты REST API заметок (создание, фильтрация, редактирование, удаление)
- `setup/install.bat` — установочный пакет для Windows
- `.github/workflows/tests.yml` — конфигурация CI в GitHub Actions
- `docs/uml/` — UML-диаграммы архитектуры системы

## Запуск приложения
```bash
pip install -r requirements.txt
python app.py
```
Открыть в браузере: `http://127.0.0.1:5000`

## Запуск тестов
```bash
pytest -v
```
