# tests/test_todos.py
import json
from app import app

def test_get_todos():
    client = app.test_client()
    r = client.get("/todos")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_post_and_get():
    client = app.test_client()
    new = {"task": "Write CI test"}
    r = client.post("/todos", data=json.dumps(new), content_type="application/json")
    assert r.status_code == 201
    created = r.get_json()
    assert created["task"] == new["task"]
    r = client.get("/todos")
    assert any(t["task"] == new["task"] for t in r.get_json())
