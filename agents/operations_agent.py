from llm_config import llm

def analyze_operations(contract_text: str) -> str:
    prompt = f"""You are an Operations Risk Specialist.

Analyse this contract for operational risks:

## 1. Deliverables & Timelines
- What must be delivered and by when? Are timelines realistic?
- Consequences of missed deadlines?

## 2. Roles & Responsibilities
- Map each party's obligations. Ambiguous ownership areas?

## 3. Service Level Agreements (SLAs)
- Performance metrics defined? SLA breach consequences?

## 4. Resource Requirements
- Personnel, infrastructure, tooling? Key-person dependencies?

## 5. Change Management
- Formal change request process? Who approves and at what cost?

## 6. Operational Risks
- Subcontractor risks? Business continuity obligations? Cybersecurity?

## 7. Exit & Transition
- Knowledge transfer obligations? Data portability? Lock-in risks?

## 8. Operational Risk Summary
Top 3-5 operational risks in priority order.

Contract:
{contract_text[:5000]}"""
    return llm.invoke(prompt).content