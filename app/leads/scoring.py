WEIGHTS = {
    "need_confirmed": 30,
    "purchase_within_90d": 25,
    "budget_known": 15,
    "decision_contact_known": 15,
    "wants_quote_or_call": 15,
}
def calculate_score(lead) -> int:
    return sum(weight for field, weight in WEIGHTS.items() if getattr(lead, field, False))
def score_band(score: int) -> str:
    return "hot" if score >= 70 else "warm" if score >= 40 else "cold"
