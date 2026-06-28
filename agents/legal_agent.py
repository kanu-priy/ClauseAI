from llm_config import llm

def analyze_legal(contract_text: str) -> str:
    prompt = f"""You are a Senior Legal Analyst with 20+ years of contract law experience.

Review this contract thoroughly:

## 1. Risky or One-Sided Clauses
List each risky clause, explain WHY it is risky, and who it disadvantages.

## 2. Liability & Indemnification
- Are liability caps reasonable and mutual?
- Are indemnification obligations balanced?
- Are there unlimited liability traps?

## 3. Missing Legal Protections
What standard clauses are absent that the signing party should demand?

## 4. Termination Conditions
- What triggers termination?
- Is termination for convenience allowed? For whom?
- What are post-termination obligations and survival clauses?

## 5. Ambiguous or Vague Language
Flag any wording that is undefined, vague, or open to multiple interpretations.

## 6. Governing Law & Dispute Resolution
- Is the jurisdiction fair?
- Is arbitration mandatory? Class action waivers?

## 7. Legal Risk Summary
Top 3 legal risks in order of severity.

Contract:
{contract_text[:5000]}"""
    return llm.invoke(prompt).content