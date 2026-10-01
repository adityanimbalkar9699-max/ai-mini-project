# Silicon Valley High-Fidelity Forward Chaining Inference Engine

def run_forward_chaining(rules, initial_facts):
    """
    Executes a multi-pass forward chaining symbolic inference cycle.
    rules: List of dicts loaded from knowledge base (rules.json).
    initial_facts: List of raw strings representing observed clinical symptoms.

    Returns:
        List of ranked diagnoses, including full matches, partial differential matches,
        evidence satisfaction breakdowns, laboratory test recommendations, and an audit trace.
    """
    normalized_input = [f.lower().strip().replace(" ", "_") for f in initial_facts if f]
    facts = set(normalized_input)
    trace = []
    fired_rules = []

    trace.append(f"[Step 01] Initialized Working Memory with {len(facts)} active clinical evidence signal(s): {sorted(list(facts)) if facts else 'None'}")

    if not facts:
        trace.append("[Step 02] Inference Halted: No active symptoms asserted in Working Memory.")
        return []

    changed = True
    cycle = 1

    # Multi-pass forward reasoning loop
    while changed:
        changed = False
        trace.append(f"[Step 02.{cycle}] Commencing Inference Cycle {cycle} across {len(rules)} production rules...")

        for rule in rules:
            rule_id = rule.get("id", "R??")
            if rule_id in fired_rules:
                continue

            premises = [p.lower().strip().replace(" ", "_") for p in rule.get("symptoms", [])]
            consequent = rule.get("diagnosis", "").strip()

            satisfied_premises = [p for p in premises if p in facts]
            missing_premises = [p for p in premises if p not in facts]

            if len(satisfied_premises) > 0 and len(satisfied_premises) < len(premises):
                trace.append(
                    f" - Rule {rule_id} ({consequent}): Partial premise match [{len(satisfied_premises)}/{len(premises)} satisfied]. "
                    f"Missing criteria: {missing_premises}"
                )

            # Rule firing condition: ALL premises must be verified in Working Memory
            if len(satisfied_premises) == len(premises) and len(premises) > 0:
                facts.add(consequent.lower())
                fired_rules.append(rule_id)
                changed = True
                trace.append(
                    f" - [RULE FIRED] Rule {rule_id} triggered! All {len(premises)} premises {premises} satisfied. "
                    f"Derived new clinical fact: '{consequent}' added to Working Memory."
                )

        cycle += 1
        if cycle > 10:
            trace.append("[Warning] Maximum inference recursion depth reached; cycle terminated.")
            break

    # Compile differential diagnosis list
    diagnoses_results = []
    for rule in rules:
        rule_id = rule.get("id")
        consequent = rule.get("diagnosis", "")
        consequent_lower = consequent.lower()

        premises = [p.lower().strip().replace(" ", "_") for p in rule.get("symptoms", [])]
        matched = [p for p in premises if p in facts]
        missing = [p for p in premises if p not in facts]
        total_required = len(premises) if premises else 1
        match_ratio = len(matched) / total_required

        if len(matched) > 0:
            is_full = (rule_id in fired_rules) or (consequent_lower in facts) or (len(matched) == total_required)
            diagnoses_results.append({
                "rule_id": rule_id,
                "id": rule_id,  # Dual-key compatibility for frontend
                "diagnosis": consequent,
                "category": rule.get("category", "General"),
                "body_system": rule.get("body_system", "General"),
                "severity": rule.get("severity", "MODERATE"),
                "confidence": rule.get("confidence", "High"),
                "icd10": rule.get("icd10", "N/A"),
                "match_count": len(matched),
                "total_required": total_required,
                "match_ratio": round(match_ratio * 100, 1),
                "is_full_match": is_full,
                "satisfied_symptoms": matched,
                "missing_symptoms": missing,
                "symptoms": premises, # for UI convenience
                "tests_recommended": rule.get("tests_recommended", "Standard clinical blood work & examination."),
                "treatment": rule.get("treatment", "Consult medical practitioner for clinical management."),
                "prevention": rule.get("prevention", "Routine preventative hygiene and primary care checkups."),
                "reasoning_trace": trace
            })

    # Sort results: Full matches first, then by match_ratio descending
    diagnoses_results.sort(key=lambda x: (x["is_full_match"], x["match_ratio"]), reverse=True)
    return diagnoses_results
