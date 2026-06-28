from llm_config import llm

def analyze_compliance(contract_text: str) -> str:
    prompt = f"""You are a Compliance & Regulatory Expert.

Analyse this contract for compliance risks:

## 1. Data Privacy & Protection (GDPR / DPDP / CCPA)
- Personal data processing? DPA in place?
- Data retention, deletion policy, breach notification timelines?
- Sub-processors and cross-border transfers?

## 2. Industry-Specific Regulations
- Sector regulation violations (finance, healthcare, telecom, employment)?
- Required licences or regulatory approvals?

## 3. Anti-Corruption & Trade Compliance
- FCPA / UK Bribery Act red flags?
- Export controls or sanctions?

## 4. Labour & Employment Compliance
- Contractor vs employee misclassification risk?
- Non-compete enforceability in governing jurisdiction?

## 5. Missing Mandatory Disclosures
- What legally required disclosures or notices are absent?

## 6. Overall Compliance Verdict
Rate each area: ✅ Compliant | ⚠️ Needs Attention | ❌ Non-Compliant

Contract:
{contract_text[:5000]}"""
    return llm.invoke(prompt).content