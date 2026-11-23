# Product requirements — public edition

## Goal
Hybrid B2B Dell server lead discovery and inbound Telegram consultation for Russia. A human manager approves outbound contacts and checks company ownership.

## Personas
- Buyer: asks for server recommendations and may send a technical specification.
- Sales manager: validates company INN/ownership, approves quotes, receives qualified leads.
- Administrator: configures permitted sources, secrets and compliance controls.

## Business flow
Discover public procurement signals → research company → determine permitted contact path → consult buyer → collect technical requirements → request INN for real project registration → manager checks company assignment → qualify → handoff with original documents.

## Presales
Collect purpose, quantity, CPU sockets/cores/frequency, RAM, storage types/count/capacity, RAID, network ports/speed, redundant PSU, iDRAC, warranty, delivery city, budget and purchase deadline. Every field is CONFIRMED, UNKNOWN, NOT_SPECIFIED or NOT_APPLICABLE. Do not guess missing fields; ask up to two relevant questions per turn. Client-provided values must remain distinct from AI suggestions.

## Handoff
Send company name, INN, Telegram contact, procurement timeline, itemized server configuration, unknown parameters, contradictions, original PDF/DOCX/XLSX attachments, conversation summary and ownership status. Block sales handoff if company belongs to another manager or status is unknown.

## Acceptance
No unsolicited messaging; no fabricated prices or availability; explicit company ownership approval; every recommendation traceable to verified documentation; human override and audit events.
