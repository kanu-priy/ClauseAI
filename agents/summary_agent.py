from llm_config import llm

def generate_summary(contract_text: str) -> str:
    prompt = f"""You are a Senior Contract Advisor writing an executive briefing for a busy CEO.
No jargon. No fluff. Under 450 words total.

## Contract Overview
- Contract type, parties and their roles
- Duration, effective date
- Total value or pricing structure

## Key Terms at a Glance
3-5 bullet points in plain English.

## ⚠️ Top 3 Things to Know Before Signing
Be blunt. What must this person understand before signing?

## 🔴 What I Would Negotiate
3 specific clauses to push back on. Name each clause, state the risk, propose what to demand instead.

## ✅ Overall Assessment
One honest paragraph. Rate it: Fair / Slightly Unfair / Unfair / Very Unfair — and explain why.

Contract:
{contract_text[:5000]}"""
    return llm.invoke(prompt).content