# QuickNotes — Документация проекта

## 1. Описание системы
**QuickNotes** — веб-приложение для создания, просмотра, поиска, редактирования и удаления текстовых заметок по категориям («Учёба», «Идеи», «Личное»).

## 2. Проектирование интерфейсов (Figma)
Интерактивный дизайн-макет экранных форм (`Notes_Main`, `Note_Create`, `Note_Edit`):
- 👉 [Открыть макет QuickNotes в Figma] https://www.figma.com/design/qg3dRFjF1l3aCUusfXN02F/Untitled?node-id=0-1&t=buYc3WBtHHovD1gn-1

## 3. Архитектура (UML)
- **Представление:** `NotesWebView` (HTML/CSS веб-интерфейс)
- **Логика приложения:** `QuickNotesServer`, `NoteService` (Python / Flask)
- **Хранение данных:** `NoteStorage`, сущность `Note`
