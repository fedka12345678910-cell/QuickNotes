from app import app, reset_notes


def test_create_and_filter_notes():
    reset_notes()
    client = app.test_client()
    r1 = client.post("/notes", json={"title": "Лабораторная №7", "category": "Учёба", "content": "Сделать прототип"})
    assert r1.status_code == 201
    r2 = client.get("/notes?category=Учёба")
    assert r2.status_code == 200
    assert len(r2.get_json()) == 1


def test_update_note():
    reset_notes()
    client = app.test_client()
    created = client.post("/notes", json={"title": "Идея проекта", "category": "Идеи", "content": "Черновик"}).get_json()
    nid = created["id"]
    upd = client.put(f"/notes/{nid}", json={"content": "Обновлённый текст заметки"})
    assert upd.status_code == 200
    assert upd.get_json()["content"] == "Обновлённый текст заметки"


def test_delete_note():
    reset_notes()
    client = app.test_client()
    created = client.post("/notes", json={"title": "Временная запись"}).get_json()
    nid = created["id"]
    res = client.delete(f"/notes/{nid}")
    assert res.status_code == 200
    assert client.get("/notes").get_json() == []
