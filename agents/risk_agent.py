from llm_config import llm
import re, json

def analyze_risk(contract_text: str) -> dict:
    """Returns dict: { scores, narrative, raw }. scores has keys:
       overall, legal, financial, operational, compliance (each 1-10),
       risk_factors (list[str]), positives (list[str])."""
    prompt = f"""You are a Contract Risk Scoring Expert.

Respond with EXACTLY this JSON first (no text before it), then write your narrative after:

{{
  "overall": <1-10>,
  "legal": <1-10>,
  "financial": <1-10>,
  "operational": <1-10>,
  "compliance": <1-10>,
  "risk_factors": ["<risk 1>","<risk 2>","<risk 3>","<risk 4>","<risk 5>"],
  "positives": ["<positive 1>","<positive 2>","<positive 3>"]
}}

SCORING: 1-3=Low risk, 4-6=Medium, 7-8=High, 9-10=Critical (higher=more risk).

After the JSON write a 200-word plain-English narrative. No markdown headers, flowing paragraphs only.

Contract:
{contract_text[:5000]}"""

    response = llm.invoke(prompt)
    raw = response.content

    scores = {"overall":5,"legal":5,"financial":5,"operational":5,"compliance":5,
              "risk_factors":[],"positives":[]}
    narrative = raw

    try:
        match = re.search(r'\{[\s\S]*?\}', raw)
        if match:
            parsed = json.loads(match.group())
            scores.update(parsed)
            narrative = raw[match.end():].strip() or "Risk analysis complete. Review scores above."
    except Exception:
        pass

    return {"scores": scores, "narrative": narrative, "raw": raw}