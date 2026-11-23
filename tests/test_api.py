def test_health(client):
    assert client.get("/health").json()["outreach_enabled"] is False

def test_auth(client):
    assert client.get("/api/v1/leads").status_code == 401

def test_lead_and_qualification(client):
    headers = {"x-api-key": "test-secret"}
    result = client.post("/api/v1/leads", headers=headers, json={"company_name": "Example LLC"})
    assert result.status_code == 201, result.text
    lead_id = result.json()["id"]
    qualification = client.patch(f"/api/v1/leads/{lead_id}/qualification", headers=headers, json={
        "need_confirmed": True, "purchase_within_90d": True, "budget_known": False,
        "decision_contact_known": True, "wants_quote_or_call": True})
    assert qualification.status_code == 200
    assert qualification.json()["score"] == 85
    assert client.patch(f"/api/v1/leads/{lead_id}/status", headers=headers,
                        json={"status": "HANDOFF", "reason": "too early"}).status_code == 409

def test_ownership_gate(client):
    headers = {"x-api-key": "test-secret"}
    lead_id = client.post("/api/v1/leads", headers=headers, json={"company_name": "Demo Corp"}).json()["id"]
    assert client.patch(f"/api/v1/leads/{lead_id}/status", headers=headers,
                        json={"status": "RESEARCHED", "reason": "public evidence"}).status_code == 200
    assert client.patch(f"/api/v1/leads/{lead_id}/status", headers=headers,
                        json={"status": "CONTACT_ELIGIBLE", "reason": "test"}).status_code == 409
