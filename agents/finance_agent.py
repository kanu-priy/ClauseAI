from llm_config import llm

def analyze_finance(contract_text: str) -> str:
    prompt = f"""You are a Financial Risk Analyst specialising in contract review.

Analyse the financial aspects of this contract:

## 1. Payment Terms
- Payment schedules, milestones, Net-30/60/upfront?
- Cash flow impact? Late payment interest charges?

## 2. Pricing Risks
- Fixed vs variable pricing? Price escalation clauses (CPI-linked)?
- Scope creep protection?

## 3. Hidden Costs & Fees
- Setup, maintenance, licensing, travel, pass-through costs?
- Uncapped pass-through costs?

## 4. Penalties & Liquidated Damages
- Financial penalties for delay or breach? Are they capped and proportionate?

## 5. Financial Obligations & Exposure
- Total potential exposure (best/worst case)?
- Unlimited financial obligations? Insurance requirements?

## 6. Currency & Tax
- Currency risk? Who bears GST/VAT/TDS/withholding tax?

## 7. Financial Red Flags
Top risks in order of severity.

Contract:
{contract_text[:5000]}"""
    return llm.invoke(prompt).content