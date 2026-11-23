from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class LeadCreate(BaseModel):
    company_name: str = Field(min_length=2, max_length=255)
    inn: str | None = Field(default=None, pattern=r"^\d{10}(\d{2})?$")
    source_url: HttpUrl | None = None
    source_evidence: str | None = Field(default=None, max_length=4000)

class LeadQualify(BaseModel):
    need_confirmed: bool
    purchase_within_90d: bool
    budget_known: bool
    decision_contact_known: bool
    wants_quote_or_call: bool

class LeadStatusUpdate(BaseModel):
    status: str
    reason: str = Field(min_length=3, max_length=1000)

class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company_name: str
    inn: str | None
    status: str
    score: int
    contact_permission: bool
    created_at: datetime

class RequirementUpsert(BaseModel):
    status: Literal["CONFIRMED", "UNKNOWN", "NOT_SPECIFIED", "NOT_APPLICABLE"]
    value: str | None = Field(default=None, max_length=2000)
    source: Literal["client_message", "client_document", "manager"] = "client_message"
    evidence: str | None = Field(default=None, max_length=2000)

class OwnershipReview(BaseModel):
    result: Literal["AVAILABLE", "ASSIGNED_SELF", "ASSIGNED_OTHER", "OWNERSHIP_UNKNOWN"]
    checked_by: str = Field(min_length=2, max_length=80)
    note: str | None = Field(default=None, max_length=1000)

class InnUpdate(BaseModel):
    inn: str
