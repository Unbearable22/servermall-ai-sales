from app.leads.gaps import next_questions
from app.leads.inn import valid_inn

def test_questions_skip_unknown():
    records = {"purpose": {"status": "UNKNOWN"}, "server_quantity": {"status": "CONFIRMED", "value": "2"}}
    result = next_questions(records)
    assert result[0]["field"] == "cpu_count"
    assert len(result) == 2

def test_inn():
    assert valid_inn("7707083893")
    assert not valid_inn("7707083894")

def test_requirement_api(client):
    h = {"x-api-key": "test-secret"}
    lead_id = client.post("/api/v1/leads", headers=h, json={"company_name": "Example"}).json()["id"]
    r = client.put(f"/api/v1/leads/{lead_id}/requirements/cpu_cores", headers=h,
                   json={"status": "UNKNOWN", "source": "client_message"})
    assert r.status_code == 200
    details = client.get(f"/api/v1/leads/{lead_id}/requirements", headers=h).json()
    assert details["requirements"]["cpu_cores"]["status"] == "UNKNOWN"
