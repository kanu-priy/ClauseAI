from llm_config import llm

def simplify_clauses(contract_text: str) -> str:
    prompt = f"""You are a plain-language legal translator.

For each of the 8-12 most important clauses in this contract:

---
**Clause**: [clause name or topic]
**What it says**: [quote first ~20 words]
**What it means**: [plain English, 1-2 sentences]
**Impact**: [✅ helps you / ❌ hurts you / ➖ neutral] — [one sentence reason]
---

Skip boilerplate. Focus on clauses affecting money, rights, obligations, or risk.

After all clauses add a **Plain English Summary** paragraph (3-4 sentences).

Contract:
{contract_text[:5000]}"""
    return llm.invoke(prompt).content