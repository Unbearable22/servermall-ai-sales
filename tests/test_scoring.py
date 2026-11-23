from types import SimpleNamespace
from app.leads.scoring import calculate_score, score_band

def test_score():
    lead = SimpleNamespace(need_confirmed=True, purchase_within_90d=True, budget_known=False,
                           decision_contact_known=True, wants_quote_or_call=True)
    assert calculate_score(lead) == 85
    assert score_band(85) == "hot"
    assert score_band(45) == "warm"
    assert score_band(0) == "cold"
