---
name: bubbly-pondering-lampson
description: Medical Diagnosis Expert System Mini-Project refactor plan
---

# Context
The user requires a complete, professional, and academically compliant "Medical Diagnosis Expert System" Mini-Project demonstrating Forward and Backward Chaining rule-based inference in Python Flask. It must satisfy academic viva/demo requirements:
1. Real Python implementations of Forward Chaining (with multi-step passes and intermediate fact derivation) and Backward Chaining (recursive subgoal evaluation). No hardcoded mock animations or fake front-end logic!
2. Premium Medical Intelligence Dashboard frontend with Dark Premium Theme (slate/navy theme, glassmorphism, responsive visual timeline for reasoning trace, interactive preset test suites, and academic viva demo buttons).
3. Thorough tests for AI engine logic and Flask API.
4. Clean directory structure with separated concerns (inference engines, knowledge bases, static and template folders).
5. No LLM or external medical APIs; works fully offline.

# Proposed Architecture

```
Project/ (AI_Mini_Project/)
├── app.py                      # Main Flask application with API endpoints
├── requirements.txt            # Project dependencies (Flask, etc.)
├── inference/
│   ├── __init__.py
│   ├── forward_chaining.py     # Genuine Forward Chaining Engine
│   └── backward_chaining.py    # Genuine Recursive Backward Chaining Engine
├── knowledge/
│   ├── __init__.py
│   ├── knowledge_base.py       # Knowledge base loaded from JSON containing rules
│   └── rules.json              # Structured list of 12 rules (symptoms & intermediate/final diagnoses)
├── tests/
│   ├── test_forward.py         # Unit tests for Forward chaining
│   ├── test_backward.py        # Unit tests for Backward chaining
│   └── test_rules.py           # Unit tests for knowledge base
├── templates/
│   └── index.html              # Premium Medical Dashboard Single-page App
├── static/
│   ├── css/
│   │   └── style.css           # Premium Tailwind/Custom Dashboard Styles (Dark)
│   ├── js/
│   │   └── app.js              # Elegant reactive app state management (vanilla JS/Alpine)
│   └── images/
│       ├── medical-ai-hero.png
│       ├── medical-ai-dashboard.png
│       └── medical-ai-process.png
└── README.md                   # Professional academic documentation
```

# Verification Plan
1. Run local pytest/unittest to make sure inference engine logic passes all checks.
2. Run `python app.py` and open the local web interface to manually check:
   - Selection of symptoms and executing Forward Chaining.
   - Run interactive preset test cases from the Testing Center.
   - Switch to Backward Chaining, select a goal disease, verify against symptoms, and inspect the vertical timeline timeline-based reasoning trace.
   - Launch Viva Mode to test quick demos for the examiner.
3. Verify that zero external API requests or online dependencies are used.
