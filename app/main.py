import secrets
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.base import Base, engine, get_db
from app.db.models import Lead, LeadEvent, Requirement, OwnershipCheck
from app.api.schemas import LeadCreate, LeadQualify, LeadStatusUpdate, LeadRead, RequirementUpsert, OwnershipReview, InnUpdate
from app.leads.scoring import calculate_score
from app.leads.gaps import QUESTIONS, next_questions
from app.leads.inn import valid_inn
from app.leads.workflow import assert_transition, TRANSITIONS

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)  # Prototype only: use Alembic in production.
    yield

app = FastAPI(title="Servermall AI Sales 100", version="0.2.0", lifespan=lifespan)

def admin(x_api_key: str | None = Header(default=None)):
    expected = get_settings().admin_api_key
    if expected == "replace-with-a-long-random-secret" or not x_api_key or not secrets.compare_digest(expected, x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/health")
def health():
    return {"status": "ok", "outreach_enabled": False, "llm_enabled": False}

@app.post("/api/v1/leads", response_model=LeadRead, status_code=201, dependencies=[Depends(admin)])
def create_lead(body: LeadCreate, db: Session = Depends(get_db)):
    if body.inn and not valid_inn(body.inn):
        raise HTTPException(422, "Invalid INN checksum")
    if body.inn and db.scalar(select(Lead).where(Lead.inn == body.inn)):
        raise HTTPException(409, "Duplicate INN")
    lead = Lead(company_name=body.company_name, inn=body.inn, source_url=str(body.source_url) if body.source_url else None, source_evidence=body.source_evidence)
    db.add(lead)
    db.flush()
    db.add(LeadEvent(lead_id=lead.id, action="CREATED", payload={"source_url": lead.source_url}))
    db.commit()
    db.refresh(lead)
    return lead

@app.get("/api/v1/leads", response_model=list[LeadRead], dependencies=[Depends(admin)])
def list_leads(limit: int = 50, db: Session = Depends(get_db)):
    if not 1 <= limit <= 100:
        raise HTTPException(422, "limit must be 1..100")
    return db.scalars(select(Lead).order_by(Lead.id.desc()).limit(limit)).all()

@app.get("/api/v1/leads/{lead_id}", response_model=LeadRead, dependencies=[Depends(admin)])
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    return lead

@app.patch("/api/v1/leads/{lead_id}/qualification", response_model=LeadRead, dependencies=[Depends(admin)])
def qualify(lead_id: int, body: LeadQualify, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    for field, value in body.model_dump().items():
        setattr(lead, field, value)
    lead.score = calculate_score(lead)
    db.add(LeadEvent(lead_id=lead_id, action="QUALIFICATION_UPDATED", payload={"score": lead.score}))
    db.commit()
    db.refresh(lead)
    return lead

@app.patch("/api/v1/leads/{lead_id}/status", response_model=LeadRead, dependencies=[Depends(admin)])
def status(lead_id: int, body: LeadStatusUpdate, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    if body.status not in TRANSITIONS:
        raise HTTPException(422, "Unknown status")
    try:
        assert_transition(lead.status, body.status)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    if body.status == "CONTACT_ELIGIBLE" and (not lead.contact_permission or not lead.consent_evidence):
        raise HTTPException(409, "Documented contact permission required")
    if body.status == "HANDOFF":
        review = db.scalar(select(OwnershipCheck).where(OwnershipCheck.lead_id == lead.id).order_by(OwnershipCheck.id.desc()))
        if not review or review.result not in ("AVAILABLE", "ASSIGNED_SELF"):
            raise HTTPException(409, "Ownership review required")
    if body.status == "QUALIFIED" and lead.score < 70:
        raise HTTPException(409, "Score below threshold")
    old = lead.status
    lead.status = body.status
    db.add(LeadEvent(lead_id=lead_id, action="STATUS_CHANGED", payload={"from": old, "to": body.status, "reason": body.reason}))
    db.commit()
    db.refresh(lead)
    return lead

@app.put("/api/v1/leads/{lead_id}/requirements/{field}", dependencies=[Depends(admin)])
def put_requirement(lead_id: int, field: str, body: RequirementUpsert, db: Session = Depends(get_db)):
    if not db.get(Lead, lead_id):
        raise HTTPException(404, "Lead not found")
    if field not in {name for name, _ in QUESTIONS}:
        raise HTTPException(422, "Unknown requirement")
    if body.status == "CONFIRMED" and not body.value:
        raise HTTPException(422, "Confirmed requirement needs value")
    if body.status != "CONFIRMED" and body.value is not None:
        raise HTTPException(422, "Only confirmed requirements may have value")
    existing = db.scalar(select(Requirement).where(Requirement.lead_id == lead_id, Requirement.field == field))
    if existing is None:
        existing = Requirement(lead_id=lead_id, field=field)
        db.add(existing)
    existing.status, existing.value, existing.source, existing.evidence = body.status, body.value, body.source, body.evidence
    db.add(LeadEvent(lead_id=lead_id, action="REQUIREMENT_UPDATED", payload={"field": field, "status": body.status}))
    db.commit()
    return {"field": field, **body.model_dump()}

@app.get("/api/v1/leads/{lead_id}/requirements", dependencies=[Depends(admin)])
def get_requirements(lead_id: int, db: Session = Depends(get_db)):
    if not db.get(Lead, lead_id):
        raise HTTPException(404, "Lead not found")
    rows = db.scalars(select(Requirement).where(Requirement.lead_id == lead_id)).all()
    recorded = {r.field: {"status": r.status, "value": r.value, "source": r.source, "evidence": r.evidence} for r in rows}
    return {"requirements": {name: recorded.get(name, {"status": "NOT_SPECIFIED", "value": None}) for name, _ in QUESTIONS}, "next_questions": next_questions(recorded)}

@app.patch("/api/v1/leads/{lead_id}/inn", dependencies=[Depends(admin)])
def update_inn(lead_id: int, body: InnUpdate, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    if not valid_inn(body.inn):
        raise HTTPException(422, "Invalid INN checksum")
    duplicate = db.scalar(select(Lead).where(Lead.inn == body.inn, Lead.id != lead_id))
    if duplicate:
        raise HTTPException(409, "Duplicate INN")
    if lead.inn != body.inn:
        db.query(OwnershipCheck).filter(OwnershipCheck.lead_id == lead_id).delete()
    lead.inn = body.inn
    db.add(LeadEvent(lead_id=lead_id, action="INN_UPDATED", payload={"inn_last4": body.inn[-4:]}))
    db.commit()
    return {"lead_id": lead_id, "inn": body.inn, "ownership_status": "OWNERSHIP_UNKNOWN"}

@app.post("/api/v1/leads/{lead_id}/ownership-review", dependencies=[Depends(admin)])
def ownership_review(lead_id: int, body: OwnershipReview, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    if not lead.inn:
        raise HTTPException(409, "INN required")
    db.add(OwnershipCheck(lead_id=lead_id, **body.model_dump()))
    db.add(LeadEvent(lead_id=lead_id, action="OWNERSHIP_REVIEWED", payload={"result": body.result, "checked_by": body.checked_by}))
    db.commit()
    return {"lead_id": lead_id, "result": body.result, "handoff_allowed": body.result in ("AVAILABLE", "ASSIGNED_SELF")}

@app.get("/api/v1/leads/{lead_id}/handoff-preview", dependencies=[Depends(admin)])
def handoff_preview(lead_id: int, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    review = db.scalar(select(OwnershipCheck).where(OwnershipCheck.lead_id == lead_id).order_by(OwnershipCheck.id.desc()))
    rows = db.scalars(select(Requirement).where(Requirement.lead_id == lead_id)).all()
    requirements = {r.field: {"status": r.status, "value": r.value, "source": r.source} for r in rows}
    return {"lead_id": lead_id, "company_name": lead.company_name, "inn": lead.inn, "score": lead.score,
            "ownership": review.result if review else "OWNERSHIP_UNKNOWN",
            "handoff_allowed": bool(review and review.result in ("AVAILABLE", "ASSIGNED_SELF") and lead.score >= 70),
            "requirements": {field: requirements.get(field, {"status": "NOT_SPECIFIED", "value": None}) for field, _ in QUESTIONS},
            "missing_questions": next_questions(requirements), "documents": [], "documents_note": "Document intake not yet implemented"}
