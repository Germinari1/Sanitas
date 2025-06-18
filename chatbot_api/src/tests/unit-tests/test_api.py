from fastapi.testclient import TestClient
import pytest
import main

# replace the real agent call with a dummy
async def fake_agent(q): 
    return {"input": q, "output": "ok", "intermediate_steps": []}

main.invoke_agent_with_retry = fake_agent  # patch in place
client = TestClient(main.app)

def test_get_status():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"status": "running"}

def test_post_agent():
    body = {"text": "ping"}
    r = client.post("/hospital-rag-agent", json=body)
    assert r.status_code == 200
    j = r.json()
    assert set(j.keys()) == {"input", "output", "intermediate_steps"}
    assert j["output"] == "ok"
