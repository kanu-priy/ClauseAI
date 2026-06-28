from llm_config import llm

def ask_contract(question: str, contract_text: str, analysis_context: dict = None) -> str:
    """
    Answer a user question about the contract.
    analysis_context: dict of {agent_name: str} — all values must be strings.
    Use safe_ctx() in app.py before passing here.
    """
    ctx_block = ""
    if analysis_context:
        ctx_block = "\n\n### Prior Analysis:\n"
        for name, text in analysis_context.items():
            ctx_block += f"\n**{name.title()}:** {str(text)[:600]}\n"

    prompt = f"""You are a contract advisor with deep legal and business expertise.
Answer the user's question clearly and concisely.
- Reference specific contract language if relevant
- If the answer is not in the contract, say so clearly
- State risk level (high/medium/low) when relevant
- 3-6 sentences unless more detail is genuinely needed
{ctx_block}

### Contract:
{contract_text[:4000]}

### Question:
{question}"""
    return llm.invoke(prompt).content