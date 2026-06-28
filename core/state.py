from typing import TypedDict, List

class ContractState(TypedDict):
    contract_text: str
    filename: str
    legal_analysis: str
    compliance_analysis: str
    finance_analysis: str
    operations_analysis: str
    summary: str
    simplified_clauses: str
    risk_result: dict
    enabled_agents: List[str]
    final_report: str
    error: str