"""
QuickNotes — веб-сервис быстрых учебных заметок.
Автор: Дыбин Фёдор Александрович (гр. ИС.1-23-2, ИрГУПС)
"""

from datetime import datetime
from flask import Flask, jsonify, request, abort, render_template_string, redirect, url_for

app = Flask(__name__)

notes = [
    {
        "id": 1,
        "title": "Конспект по ИСИС",
        "category": "Учёба",
        "content": "Изучить модель ветвления GitFlow, UML-диаграммы и настройку GitHub Actions.",
        "created_at": "26.11.2026 12:30",
    },
    {
        "id": 2,
        "title": "Идея для курсовой",
        "category": "Идеи",
        "content": "Сделать веб-сервис для обмена учебными конспектами между студентами группы.",
        "created_at": "26.11.2026 12:45",
    },
]
_next_id = 3


def reset_notes():
    global notes, _next_id
    notes = []
    _next_id = 1


MAIN_HTML = """
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>QuickNotes — Быстрые заметки</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; margin: 0; padding: 28px 48px; color: #0f172a; }
    .topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .brand { font-size: 24px; font-weight: 700; color: #1e3a8a; }
    .btn { padding: 9px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; border: none; cursor: pointer; font-size: 14px; display: inline-block; }
    .btn-primary { background: #2563eb; color: #fff; }
    .btn-light { background: #e2e8f0; color: #1e293b; }
    .btn-danger { background: #fee2e2; color: #991b1b; }
    .toolbar { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 22px; }
    .search-input { padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; width: 260px; font-size: 14px; }
    .pill { padding: 6px 14px; border-radius: 999px; border: 1px solid #cbd5e1; background: #fff; color: #334155; text-decoration: none; font-size: 13px; }
    .pill.active { background: #2563eb; color: #fff; border-color: #2563eb; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
    .card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; box-shadow: 0 2px 6px rgba(15,23,42,.04); display: flex; flex-direction: column; justify-content: space-between; }
    .badge { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; background: #dbeafe; color: #1e40af; margin-bottom: 8px; }
    .card h3 { margin: 4px 0 8px; font-size: 17px; }
    .card p { margin: 0 0 14px; color: #475569; font-size: 14px; line-height: 1.45; }
    .card-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 10px; font-size: 12px; color: #64748b; }
  </style>
</head>
<body>
  <div class="topbar">
    <div class="brand">QuickNotes</div>
    <a href="/create" class="btn btn-primary">+ Новая заметка</a>
  </div>
  <form class="toolbar" method="get" action="/">
    <input class="search-input" type="text" name="q" value="{{ q }}" placeholder="Поиск по заголовку или тексту...">
    <input type="hidden" name="category" value="{{ category }}">
    <button class="btn btn-light" type="submit">Найти</button>
    {% for cat in ['Все', 'Учёба', 'Идеи', 'Личное'] %}
      <a href="/?category={{ cat }}&q={{ q }}" class="pill {{ 'active' if category == cat else '' }}">{{ cat }}</a>
    {% endfor %}
  </form>
  {% if items %}
    <div class="grid">
      {% for n in items %}
        <div class="card">
          <div>
            <span class="badge">{{ n.category }}</span>
            <h3>{{ n.title }}</h3>
            <p>{{ n.content }}</p>
          </div>
          <div class="card-footer">
            <span>{{ n.created_at }}</span>
            <div style="display:flex; gap:6px;">
              <a href="/edit/{{ n.id }}" class="btn btn-light" style="padding:5px 10px; font-size:12px;">Изменить</a>
              <form action="/delete/{{ n.id }}" method="post" style="margin:0;">
                <button type="submit" class="btn btn-danger" style="padding:5px 10px; font-size:12px;">Удалить</button>
              </form>
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <p style="text-align:center; color:#64748b; margin-top:60px;">Заметок не найдено. Нажмите «+ Новая заметка», чтобы добавить первую.</p>
  {% endif %}
</body>
</html>
"""

FORM_HTML = """
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{{ page_title }} — QuickNotes</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .card { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 28px; width: 440px; box-shadow: 0 4px 16px rgba(15,23,42,.06); }
    h2 { margin-top: 0; }
    label { display: block; font-size: 14px; font-weight: 600; margin: 12px 0 4px; color: #334155; }
    input, select, textarea { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; box-sizing: border-box; font-family: inherit; font-size: 14px; }
    .actions { display: flex; gap: 10px; margin-top: 18px; }
    .btn { flex: 1; padding: 10px; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; text-align: center; text-decoration: none; font-size: 14px; }
    .btn-cancel { background: #e2e8f0; color: #1e293b; }
    .btn-save { background: #2563eb; color: #fff; }
  </style>
</head>
<body>
  <div class="card">
    <h2>{{ page_title }}</h2>
    <form method="post">
      <label>Заголовок заметки *</label>
      <input type="text" name="title" value="{{ note.title if note else '' }}" placeholder="Например: Подготовка к защите ЛР" required>
      <label>Категория</label>
      <select name="category">
        {% for cat in ['Учёба', 'Идеи', 'Личное'] %}
          <option value="{{ cat }}" {{ 'selected' if note and note.category == cat else '' }}>{{ cat }}</option>
        {% endfor %}
      </select>
      <label>Текст заметки</label>
      <textarea name="content" rows="5" placeholder="Введите содержание заметки...">{{ note.content if note else '' }}</textarea>
      <div class="actions">
        <a href="/" class="btn btn-cancel">Отмена</a>
        <button type="submit" class="btn btn-save">{{ submit_label }}</button>
      </div>
    </form>
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    category = request.args.get("category", "Все")
    q = request.args.get("q", "").strip()
    items = notes
    if category and category != "Все":
        items = [n for n in items if n["category"] == category]
    if q:
        items = [n for n in items if q.lower() in n["title"].lower() or q.lower() in n["content"].lower()]
    return render_template_string(MAIN_HTML, items=items, category=category, q=q)


@app.route("/create", methods=["GET", "POST"])
def create_page():
    global _next_id
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        if title:
            notes.append({
                "id": _next_id,
                "title": title,
                "category": (request.form.get("category") or "Учёба").strip(),
                "content": (request.form.get("content") or "").strip(),
                "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
            })
            _next_id += 1
        return redirect(url_for("index"))
    return render_template_string(FORM_HTML, page_title="Новая заметка", submit_label="Сохранить заметку", note=None)


@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit_page(note_id):
    target = next((n for n in notes if n["id"] == note_id), None)
    if not target:
        abort(404)
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        if title:
            target["title"] = title
        target["category"] = (request.form.get("category") or target["category"]).strip()
        target["content"] = (request.form.get("content") or "").strip()
        return redirect(url_for("index"))
    return render_template_string(FORM_HTML, page_title="Редактирование заметки", submit_label="Сохранить изменения", note=target)


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_page(note_id):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return redirect(url_for("index"))


# --- REST API для заметок ---
@app.route("/notes", methods=["GET"])
def api_get_notes():
    category = request.args.get("category", "").strip()
    query = request.args.get("q", "").strip().lower()
    result = notes
    if category and category != "Все":
        result = [n for n in result if n["category"] == category]
    if query:
        result = [n for n in result if query in n["title"].lower() or query in n["content"].lower()]
    return jsonify(result), 200


@app.route("/notes", methods=["POST"])
def api_create_note():
    global _next_id
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        abort(400, description="Note title is required")
    note = {
        "id": _next_id,
        "title": title,
        "category": (data.get("category") or "Учёба").strip(),
        "content": (data.get("content") or "").strip(),
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    notes.append(note)
    _next_id += 1
    return jsonify(note), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
def api_update_note(note_id):
    data = request.get_json(silent=True) or {}
    for note in notes:
        if note["id"] == note_id:
            if "title" in data and data["title"].strip():
                note["title"] = data["title"].strip()
            if "category" in data and data["category"].strip():
                note["category"] = data["category"].strip()
            if "content" in data:
                note["content"] = data["content"].strip()
            return jsonify(note), 200
    abort(404, description="Note not found")


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def api_delete_note(note_id):
    global notes
    for note in notes:
        if note["id"] == note_id:
            notes = [n for n in notes if n["id"] != note_id]
            return jsonify({"deleted": note_id}), 200
    abort(404, description="Note not found")


if __name__ == "__main__":
    print("QuickNotes server starting at http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
