# AuraMed Clinical AI // Clinical Decision Support Expert System

> **High-Fidelity Symbolic Artificial Intelligence Platform for Deterministic Medical Inference & Clinical Triage**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.0-green.svg)](https://flask.palletsprojects.com/)
[![Inference Engine](https://img.shields.io/badge/AI%20Core-Forward%20%26%20Backward%20Chaining-emerald.svg)]()
[![Cloud Ready](https://img.shields.io/badge/Deployment-Docker%20%2F%20Render%20%2F%20GCP-cyan.svg)]()
[![Status](https://img.shields.io/badge/Reliability-100%25%20Verified-brightgreen.svg)]()

---

## 1. Executive Overview & Problem Statement
In clinical medicine, diagnostic precision demands rigorous, transparent, and deterministic evidence evaluation. Traditional machine learning and generative AI architectures struggle in high-stakes healthcare environments due to unexplainable "black-box" heuristics, stochastic unpredictability, and severe hallucination risks.

**AuraMed Clinical AI** is an enterprise-grade **Symbolic AI Expert System (Clinical Decision Support System - CDSS)** built to replicate clinical diagnostic reasoning through formal production rules (Horn clauses) and mathematical inference.

The system features:
- **Forward Chaining Inference Engine**: Data-driven, bottom-up reasoning that synthesizes observed symptom clusters into a prioritized differential diagnosis.
- **Backward Chaining Inference Engine**: Goal-driven, top-down hypothesis verification that mathematically proves or refutes suspected medical conditions and isolates missing clinical evidence.
- **Interactive Patient Telemetry & Vitals Triage**: Automated surveillance of Blood Pressure, SpO2, Heart Rate, and Temperature with real-time red-flag crisis warnings.
- **Interactive SVG Decision Network Graph**: Visual proof graph mapping active premises to fired production rules and derived diagnostic outcomes in real time.
- **Formal Clinical Report Generator**: 1-click printable/PDF medical documentation complete with patient telemetry, differential diagnoses, and an audit trail.

---

## 2. Theoretical Architecture & AI Foundations

### A. Forward Chaining (Data-Driven Bottom-Up Synthesis)
- **Mechanism**: Operates from known premises in **Working Memory** forward to derive all valid conclusions.
- **Formal Logic**: Evaluates production rules $R_i: P_1 \wedge P_2 \wedge \dots \wedge P_k \rightarrow C$ via **Modus Ponens** ($P \rightarrow Q, P \vdash Q$).
- **Conflict Resolution**: Ranks competing diagnoses by **Specificity** (highest matching premise ratio) and applies **Refractoriness** to prevent circular execution.
- **Clinical Role**: Primary screening for undiagnosed patient symptom presentations.

### B. Backward Chaining (Goal-Driven Top-Down Hypothesis Prover)
- **Mechanism**: Initiates with a target hypothesis $Q$ (suspected disease) and recursively queries the Knowledge Base to prove or refute the goal.
- **Subgoal Decomposition**: Decomposes $Q$ into subgoals ($P_1, P_2, \dots$). If all subgoals exist in the patient's record, the goal is **PROVEN**. If any premise is absent, the system identifies the exact missing evidence and suggests targeted clinician inquiries.
- **Clinical Role**: Emergency rule-outs (e.g. verifying acute Meningitis or Myocardial Infarction).

---

## 3. Knowledge Base Repository (Rules R01 — R12)

| Rule ID | Condition | Category | Severity | ICD-10 | Required Premises (Symptoms) |
|---|---|---|---|---|---|
| **R01** | Common Pneumonia | Respiratory | URGENT | `J18.9` | Fever, Cough, Fatigue, Shortness of Breath |
| **R02** | Viral Influenza (Flu) | Infectious | MODERATE | `J10.1` | Fever, Headache, Muscle Pain, Fatigue |
| **R03** | Meningitis | Neurological | CRITICAL EMERGENCY | `G03.9` | Fever, Headache, Stiff Neck, Sensitivity to Light |
| **R04** | Common Cold | Respiratory | ROUTINE | `J00` | Cough, Sneezing, Runny Nose, Sore Throat |
| **R05** | Dengue Fever | Infectious | URGENT | `A90` | Fever, Rash, Joint Pain, Headache |
| **R06** | Type 2 Diabetes | Endocrine | MODERATE | `E11.9` | Increased Thirst, Frequent Urination, Fatigue, Weight Loss |
| **R07** | Gastroenteritis | Gastrointestinal | MODERATE | `A09` | Fever, Abdominal Pain, Nausea, Diarrhea |
| **R08** | Bronchitis | Respiratory | MODERATE | `J20.9` | Cough, Shortness of Breath, Wheezing, Chest Tightness |
| **R09** | Myocardial Infarction | Cardiovascular | CRITICAL EMERGENCY | `I21.9` | Chest Pain, Shortness of Breath, Sweating, Dizziness |
| **R10** | Allergic Rhinitis | Immunological | ROUTINE | `J30.9` | Sneezing, Itchy Eyes, Runny Nose, Nasal Congestion |
| **R11** | Rheumatoid Arthritis | Musculoskeletal | MODERATE | `M06.9` | Joint Pain, Stiffness, Swelling, Reduced Mobility |
| **R12** | Iron Deficiency Anemia | Hematological | MODERATE | `D50.9` | Fatigue, Paleness, Weakness, Shortness of Breath |

---

## 4. System Architecture Diagram

```
+-----------------------------------------------------------------------+
|                    Client Browser Interface                           |
|       (Tailwind CSS, Glassmorphism, Web Audio Synthesizer, SVG)       |
+-----------------------------------+-----------------------------------+
                                    | HTTP REST API
                                    v
+-----------------------------------------------------------------------+
|                         Flask Application Core                        |
|        (/api/forward-chain, /api/backward-chain, /api/triage)         |
+-----------------------------------+-----------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+-------------------------------+               +-------------------------------+
|    Forward Chaining Engine    |               |    Backward Chaining Engine   |
|   (Data-Driven Multi-Pass)    |               |   (Goal-Driven Prover Tree)   |
+---------------+---------------+               +---------------+---------------+
                |                                               |
                +-----------------------+-----------------------+
                                        |
                                        v
+-----------------------------------------------------------------------+
|                    Clinical Knowledge Base Repository                 |
|             (rules.json - 12 Rules, ICD-10, Protocols, Vitals)        |
+-----------------------------------------------------------------------+
```

---

## 5. REST API Endpoints Specification

- `GET /health`: Healthcheck endpoint for cloud platforms.
- `GET /api/knowledge-base`: Returns all production rules and metadata.
- `GET /api/symptoms`: Returns all normalized clinical symptoms.
- `GET /api/symptoms/categorized`: Returns symptoms mapped by anatomical organ system.
- `GET /api/diseases`: Returns all target conditions with severity tiers.
- `GET /api/case-presets`: Returns pre-configured clinical case scenarios for instant viva demos.
- `POST /api/triage`: Evaluates patient vitals (BP, SpO2, HR, Temp) for clinical red-flags.
- `POST /api/forward-chain`: Executes forward chaining inference given `{ "symptoms": [...] }`.
- `POST /api/backward-chain`: Executes backward chaining given `{ "target": "...", "symptoms": [...] }`.
- `POST /api/test`: Runs the 5 automated clinical test cases and returns pass/fail metrics.

---

## 6. Local Installation & Quick Start

1. **Clone or Navigate to the Project**:
   ```powershell
   cd "S:\ai mini project"
   ```

2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```powershell
   python app.py
   ```
   Open your browser at: `http://localhost:5000`

4. **Run the Automated Test Suite**:
   ```powershell
   python tests/test_expert_system.py
   python tests/test_api.py
   python tests/test_rules.py
   ```

---

## 7. Cloud Deployment (Render, Railway, Google Cloud Run)

The repository includes a production `Dockerfile`, `Procfile`, `render.yaml`, and `requirements.txt`.

### Deploying Free on Render in 2 Minutes:
1. Push this folder to a GitHub repository.
2. Log into [Render.com](https://render.com) and click **New Web Service**.
3. Select your repository.
4. Render will auto-detect the configuration and deploy your app with a public `https://...onrender.com` URL.

*For complete details across all platforms, see [DEPLOYMENT_GUIDE.md](file:///s:/ai%20mini%20project/DEPLOYMENT_GUIDE.md).*

---

## 8. Academic Viva & Examiner Defense Checklist

- **Q1: What is the core reasoning mechanism of this system?**
  - *Answer*: It utilizes First-Order Symbolic Artificial Intelligence based on production rules ($P \rightarrow Q$) evaluated via Modus Ponens inference.
- **Q2: Why use Backward Chaining in medicine?**
  - *Answer*: Backward Chaining evaluates a specific diagnostic hypothesis top-down. If a clinician suspects a critical condition like Meningitis or Heart Attack, Backward Chaining directly checks which diagnostic criteria are present and identifies the exact missing evidence needed to confirm or rule out the disease.
- **Q3: How does the system resolve rule conflicts?**
  - *Answer*: Specificity ranking (prioritizing rules with the highest proportion of satisfied premises) and refractoriness (preventing identical rule firing in cyclical passes).
- **Q4: How does it ensure zero hallucination?**
  - *Answer*: Because all reasoning is deterministic and grounded strictly in the verified Knowledge Base (`rules.json`), with every derivation recorded in the explainable audit trail.

---

## 9. Academic Disclaimer
⚠️ **Academic Laboratory Project**: Developed for educational evaluation in Artificial Intelligence coursework. Not intended for direct clinical diagnostic use without licensed physician review.
