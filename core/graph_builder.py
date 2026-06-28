"""
ClauseAI — Graph Builder & Parallel Runner
LangGraph sequential workflow + ThreadPoolExecutor parallel runner.
"""
from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END
from concurrent.futures import ThreadPoolExecutor, as_completed

from agents.legal_agent import analyze_legal
from agents.compliance_agent import analyze_compliance
from agents.finance_agent import analyze_finance
from agents.operations_agent import analyze_operations
from agents.risk_agent import analyze_risk
from agents.summary_agent import generate_summary
from agents.simplifier_agent import simplify_clauses
from utils.helpers import build_full_report
from core.state import ContractState


# ── LangGraph node functions ──────────────────────────────────

def node_legal(state):
    try:    return {"legal_analysis": analyze_legal(state["contract_text"])}
    except Exception as e: return {"legal_analysis": f"⚠️ Error: {e}"}

def node_compliance(state):
    try:    return {"compliance_analysis": analyze_compliance(state["contract_text"])}
    except Exception as e: return {"compliance_analysis": f"⚠️ Error: {e}"}

def node_finance(state):
    try:    return {"finance_analysis": analyze_finance(state["contract_text"])}
    except Exception as e: return {"finance_analysis": f"⚠️ Error: {e}"}

def node_operations(state):
    try:    return {"operations_analysis": analyze_operations(state["contract_text"])}
    except Exception as e: return {"operations_analysis": f"⚠️ Error: {e}"}

def node_risk(state):
    try:    return {"risk_result": analyze_risk(state["contract_text"])}
    except Exception as e:
        return {"risk_result": {"scores":{"overall":5,"legal":5,"financial":5,"operational":5,"compliance":5,"risk_factors":[],"positives":[]},
                                "narrative": f"⚠️ Error: {e}", "raw": ""}}

def node_summary(state):
    try:    return {"summary": generate_summary(state["contract_text"])}
    except Exception as e: return {"summary": f"⚠️ Error: {e}"}

def node_simplifier(state):
    try:    return {"simplified_clauses": simplify_clauses(state["contract_text"])}
    except Exception as e: return {"simplified_clauses": f"⚠️ Error: {e}"}

def node_generate_report(state):
    results = {}
    if state.get("summary"):             results["summary"]    = state["summary"]
    if state.get("risk_result",{}).get("narrative"): results["risk"] = state["risk_result"]["narrative"]
    if state.get("legal_analysis"):      results["legal"]      = state["legal_analysis"]
    if state.get("compliance_analysis"): results["compliance"] = state["compliance_analysis"]
    if state.get("finance_analysis"):    results["finance"]    = state["finance_analysis"]
    if state.get("operations_analysis"): results["operations"] = state["operations_analysis"]
    if state.get("simplified_clauses"):  results["simplifier"] = state["simplified_clauses"]
    return {"final_report": build_full_report(results, state.get("filename","contract"))}


# ── LangGraph sequential build ────────────────────────────────

def build_graph():
    """Sequential LangGraph workflow (use run_analysis_parallel for true parallelism)."""
    g = StateGraph(ContractState)
    g.add_node("legal",      node_legal)
    g.add_node("compliance", node_compliance)
    g.add_node("finance",    node_finance)
    g.add_node("operations", node_operations)
    g.add_node("risk",       node_risk)
    g.add_node("summary",    node_summary)
    g.add_node("simplifier", node_simplifier)
    g.add_node("report",     node_generate_report)
    g.set_entry_point("legal")
    g.add_edge("legal","compliance"); g.add_edge("compliance","finance")
    g.add_edge("finance","operations"); g.add_edge("operations","risk")
    g.add_edge("risk","summary"); g.add_edge("summary","simplifier")
    g.add_edge("simplifier","report"); g.add_edge("report", END)
    return g.compile()


# ── Agent map (text-returning agents only) ────────────────────

AGENT_MAP = {
    "legal":      analyze_legal,
    "compliance": analyze_compliance,
    "finance":    analyze_finance,
    "operations": analyze_operations,
    "summary":    generate_summary,
    "simplifier": simplify_clauses,
    # "risk" is NOT here — it returns dict, handled separately
}


# ── Parallel runner ───────────────────────────────────────────

def run_analysis_parallel(
    contract_text: str,
    enabled_agents: List[str],       # must be List[str]
    progress_callback=None
) -> tuple:
    """
    Run enabled agents in parallel with ThreadPoolExecutor.

    Args:
        contract_text:   Full text of the contract.
        enabled_agents:  List of agent names, e.g. ["legal","risk","summary"].
        progress_callback: Optional callable(name, status) for live updates.

    Returns:
        (results: Dict[str, str], risk_result: dict | None)
        results contains only text-agent outputs (str values).
        risk_result is the structured dict from risk_agent (separate return).
    """
    results: Dict[str, Any] = {}
    risk_result = None

    run_risk   = "risk" in enabled_agents
    text_agents = [a for a in enabled_agents if a != "risk" and a in AGENT_MAP]

    if not text_agents and not run_risk:
        return results, risk_result

    def run_text(name, fn):
        try:
            if progress_callback: progress_callback(name, "running")
            out = fn(contract_text)
            if progress_callback: progress_callback(name, "done")
            return name, out
        except Exception as e:
            if progress_callback: progress_callback(name, "error")
            return name, f"⚠️ {name} agent error: {e}"

    def run_risk_fn():
        try:
            if progress_callback: progress_callback("risk", "running")
            out = analyze_risk(contract_text)
            if progress_callback: progress_callback("risk", "done")
            return "risk", out
        except Exception as e:
            if progress_callback: progress_callback("risk", "error")
            return "risk", {"scores":{"overall":5,"legal":5,"financial":5,"operational":5,"compliance":5,
                                      "risk_factors":[],"positives":[]},
                            "narrative": f"⚠️ Risk error: {e}", "raw": ""}

    workers = min(len(text_agents) + (1 if run_risk else 0), 8)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(run_text, n, AGENT_MAP[n]): n for n in text_agents}
        if run_risk:
            rf = ex.submit(run_risk_fn); futures[rf] = "risk"

        for fut in as_completed(futures):
            name, result = fut.result()
            if name == "risk":
                risk_result = result   # dict — kept separate, NOT merged into results
            else:
                results[name] = result  # str

    return results, risk_result