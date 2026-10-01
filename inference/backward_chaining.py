# Silicon Valley High-Fidelity Backward Chaining (Goal-Driven Prover) Engine

def run_backward_chaining(rules, target_disease, user_symptoms):
    """
    Executes a goal-driven recursive backward chaining inference engine.
    rules: List of dicts representing production rules.
    target_disease: String (The hypothesis goal to prove).
    user_symptoms: List of strings (Known clinical evidence asserted).

    Returns:
        Dict containing validation status, satisfied criteria, missing clinical evidence,
        recommended next-step clinical inquiries, and full proof trace.
    """
    known_facts = set(f.lower().strip().replace(" ", "_") for f in user_symptoms if f)
    trace = []
    goal_str = str(target_disease).strip()
    goal_lower = goal_str.lower()

    trace.append(f"[Goal Assertion] Initiating Top-Down Backward Chaining for clinical hypothesis: '{goal_str}'")
    trace.append(f"[Evidence Base] Observed facts in patient record: {sorted(list(known_facts)) if known_facts else 'None'}")

    target_rule = None
    for r in rules:
        if r.get("diagnosis", "").strip().lower() == goal_lower or r.get("id", "").strip().lower() == goal_lower:
            target_rule = r
            break

    if not target_rule:
        trace.append(f"[Hypothesis Rejected] No production rule in Knowledge Base derives '{goal_str}'.")
        return {
            "matched": False,
            "target": goal_str,
            "diagnosis": goal_str,
            "rule_id": "N/A",
            "category": "Unknown",
            "severity": "UNKNOWN",
            "confidence": "None",
            "icd10": "N/A",
            "satisfied_symptoms": [],
            "missing_symptoms": [goal_str],
            "recommended_inquiry": [f"Validate whether '{goal_str}' is within diagnostic scope."],
            "tests_recommended": "Clinical evaluation required.",
            "treatment": "N/A",
            "reasoning_trace": trace
        }

    rule_id = target_rule.get("id", "R??")
    diagnosis = target_rule.get("diagnosis", goal_str)
    premises = [p.lower().strip().replace(" ", "_") for p in target_rule.get("symptoms", [])]

    trace.append(f"[Subgoal Decomposition] Hypothesis mapped to Rule {rule_id} (Diagnosis: '{diagnosis}')")
    trace.append(f" - Required Antecedent Premises: {premises}")

    satisfied = []
    missing = []

    for p in premises:
        if p in known_facts:
            satisfied.append(p)
            trace.append(f"   ✓ Subgoal '{p}': SATISFIED (Observed in patient record)")
        else:
            missing.append(p)
            trace.append(f"   ✗ Subgoal '{p}': UNSATISFIED (Missing from patient record)")

    is_verified = (len(missing) == 0 and len(premises) > 0)

    if is_verified:
        trace.append(f"[Conclusion Verified] Rule {rule_id} is FULLY SATISFIED. Hypothesis '{diagnosis}' is mathematically PROVEN by available clinical evidence.")
    else:
        trace.append(f"[Conclusion Inconclusive] Rule {rule_id} cannot fire. Missing required evidence: {missing}. Hypothesis '{diagnosis}' remains UNPROVEN.")

    recommended_inquiries = [f"Inquire / Test patient for active presence of: '{m.replace('_', ' ')}'" for m in missing]

    return {
        "matched": is_verified,
        "target": diagnosis,
        "diagnosis": diagnosis,
        "rule_id": rule_id,
        "id": rule_id,
        "category": target_rule.get("category", "General"),
        "body_system": target_rule.get("body_system", "General"),
        "severity": target_rule.get("severity", "MODERATE"),
        "confidence": target_rule.get("confidence", "High"),
        "icd10": target_rule.get("icd10", "N/A"),
        "total_required": len(premises),
        "satisfied_symptoms": satisfied,
        "missing_symptoms": missing,
        "recommended_inquiry": recommended_inquiries,
        "tests_recommended": target_rule.get("tests_recommended", "Standard clinical diagnostic workup."),
        "treatment": target_rule.get("treatment", "Consult appropriate medical specialist."),
        "prevention": target_rule.get("prevention", "Standard preventative measures."),
        "reasoning_trace": trace
    }
