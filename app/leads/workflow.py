TRANSITIONS = {
    "DISCOVERED": {"RESEARCHED", "NEEDS_REVIEW", "DUPLICATE"},
    "RESEARCHED": {"CONTACT_ELIGIBLE", "NEEDS_REVIEW", "DUPLICATE"},
    "CONTACT_ELIGIBLE": {"CONTACTED", "ENGAGED", "NEEDS_REVIEW", "OPTED_OUT"},
    "CONTACTED": {"ENGAGED", "NO_RESPONSE", "OPTED_OUT", "NEEDS_REVIEW"},
    "ENGAGED": {"QUALIFIED", "NO_RESPONSE", "OPTED_OUT", "NEEDS_REVIEW"},
    "QUALIFIED": {"HANDOFF", "ENGAGED", "OPTED_OUT", "NEEDS_REVIEW"},
    "HANDOFF": {"WON", "LOST", "ENGAGED", "OPTED_OUT"},
    "NEEDS_REVIEW": {"RESEARCHED", "CONTACT_ELIGIBLE", "OPTED_OUT", "DUPLICATE"},
    "NO_RESPONSE": {"ENGAGED", "OPTED_OUT"},
    "WON": set(), "LOST": set(), "OPTED_OUT": set(), "DUPLICATE": set(),
}
def assert_transition(current: str, target: str):
    if target not in TRANSITIONS.get(current, set()):
        raise ValueError(f"Invalid transition: {current} -> {target}")
