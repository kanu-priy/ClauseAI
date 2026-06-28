def classify_contract(contract_text: str) -> str:
    t = contract_text.lower()
    if "lease" in t or "tenant" in t or "landlord" in t: return "Lease Agreement"
    if "employment" in t or "employee" in t or "employer" in t: return "Employment Contract"
    if "non-disclosure" in t or "nda" in t: return "Non-Disclosure Agreement"
    if "saas" in t or "software" in t or "subscription" in t: return "SaaS / Software Agreement"
    if "vendor" in t or "supplier" in t or "procurement" in t: return "Vendor Agreement"
    if "service" in t or "statement of work" in t or "sow" in t: return "Service Agreement"
    if "partnership" in t or "joint venture" in t: return "Partnership Agreement"
    if "purchase" in t or "acquisition" in t: return "Purchase / Sale Agreement"
    return "General Contract"