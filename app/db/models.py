from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

def utcnow():
    return datetime.now(timezone.utc)

class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    inn: Mapped[str | None] = mapped_column(String(12), unique=True, index=True)
    source_url: Mapped[str | None] = mapped_column(Text)
    source_evidence: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="DISCOVERED")
    need_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    purchase_within_90d: Mapped[bool] = mapped_column(Boolean, default=False)
    budget_known: Mapped[bool] = mapped_column(Boolean, default=False)
    decision_contact_known: Mapped[bool] = mapped_column(Boolean, default=False)
    wants_quote_or_call: Mapped[bool] = mapped_column(Boolean, default=False)
    contact_permission: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_evidence: Mapped[str | None] = mapped_column(Text)
    score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class LeadEvent(Base):
    __tablename__ = "lead_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), index=True)
    action: Mapped[str] = mapped_column(String(60))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class Requirement(Base):
    __tablename__ = "lead_requirements"
    __table_args__ = (UniqueConstraint("lead_id", "field"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), index=True)
    field: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(24), default="NOT_SPECIFIED")
    value: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(32), default="client_message")
    evidence: Mapped[str | None] = mapped_column(Text)

class OwnershipCheck(Base):
    __tablename__ = "ownership_checks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), index=True)
    result: Mapped[str] = mapped_column(String(32))
    checked_by: Mapped[str] = mapped_column(String(80))
    note: Mapped[str | None] = mapped_column(Text)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
