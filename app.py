from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys

# Dynamic root path resolution for Cloud Servers (Fixes ModuleNotFoundError)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge.knowledge_base import kb
from inference import run_forward_chaining, run_backward_chaining

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# Direct image routes for root project images and standard asset paths
@app.route('/bg image .jpg')
@app.route('/bg-image.jpg')
@app.route('/medical-bg.jpg')
def serve_bg_image_root():
    return send_from_directory(os.path.dirname(__file__), 'bg image .jpg')

@app.route('/images/<path:filename>')
def serve_images(filename):
    static_images = os.path.join(os.path.dirname(__file__), 'static', 'images')
    if os.path.exists(os.path.join(static_images, filename)):
        return send_from_directory(static_images, filename)
    public_images = os.path.join(os.path.dirname(__file__), 'public', 'images')
    if os.path.exists(os.path.join(public_images, filename)):
        return send_from_directory(public_images, filename)
    return send_from_directory(os.path.dirname(__file__), 'bg image .jpg')

@app.route('/public/images/<path:filename>')
def serve_public_images(filename):
    public_images = os.path.join(os.path.dirname(__file__), 'public', 'images')
    return send_from_directory(public_images, filename)

@app.route('/pxADSsRzsOUiyL2ytMSCNsh8WnSvx42rYMCjghWOzknxK5giCppHpiBG4yVIQ4UoG1uVmM5DeEldoLURxqNRgxygiShpx1ohWKrP7_g40KBhBivKZrAv7t5HnZ5B4AXUdHq-PLMmCZDrDssVtUuBglY8wUSs3pfuCofKV5n4rmrNVc_VRIhzdXVj3Q4b0PGB.jpg')
def serve_second_image_root():
    return send_from_directory(os.path.dirname(__file__), 'pxADSsRzsOUiyL2ytMSCNsh8WnSvx42rYMCjghWOzknxK5giCppHpiBG4yVIQ4UoG1uVmM5DeEldoLURxqNRgxygiShpx1ohWKrP7_g40KBhBivKZrAv7t5HnZ5B4AXUdHq-PLMmCZDrDssVtUuBglY8wUSs3pfuCofKV5n4rmrNVc_VRIhzdXVj3Q4b0PGB.jpg')

# Security & CORS headers helper
@app.after_request
def add_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# --- Core Web Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "AI Clinical Decision Support Expert System",
        "version": "2.4.0-cloud",
        "rules_loaded": len(kb.get_all_rules()),
        "engine": "Symbolic Logic (Forward & Backward Chaining)"
    }), 200

# --- Knowledge Base Discovery API ---
@app.route('/api/knowledge-base', methods=['GET'])
@app.route('/rules', methods=['GET'])
def get_knowledge_base():
    rules = kb.get_all_rules()
    return jsonify({
        "status": "success",
        "total_rules": len(rules),
        "rules": rules
    })

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    all_symptoms = kb.get_all_symptoms()
    return jsonify({
        "status": "success",
        "total_symptoms": len(all_symptoms),
        "symptoms": all_symptoms
    })

@app.route('/api/symptoms/categorized', methods=['GET'])
def get_categorized_symptoms():
    return jsonify({
        "status": "success",
        "categories": kb.get_categorized_symptoms()
    })

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    diseases = kb.get_all_diseases()
    names = kb.get_disease_names()
    return jsonify({
        "status": "success",
        "total_diseases": len(diseases),
        "diseases": diseases,
        "disease_names": names
    })

@app.route('/api/case-presets', methods=['GET'])
def get_case_presets():
    return jsonify({
        "status": "success",
        "presets": kb.get_case_presets()
    })

# --- Clinical Triage API ---
@app.route('/api/triage', methods=['POST'])
def clinical_triage():
    data = request.get_json() or {}
    vitals = data.get('vitals', {})
    symptoms = data.get('symptoms', [])

    red_flags = []
    triage_level = "ROUTINE"

    # Evaluate vital signs
    try:
        spo2 = float(vitals.get('spo2', 98))
        hr = float(vitals.get('hr', 75))
        temp = float(vitals.get('temp', 37.0))
        bp_str = str(vitals.get('bp', '120/80'))

        if spo2 < 92:
            red_flags.append(f"Hypoxemia Alert: SpO2 is {spo2}% (Normal: >= 95%). Immediate oxygen therapy indicated.")
            triage_level = "CRITICAL EMERGENCY"
        elif spo2 < 95:
            red_flags.append(f"Borderline SpO2: {spo2}%. Respiratory distress monitoring required.")
            if triage_level != "CRITICAL EMERGENCY":
                triage_level = "URGENT"

        if hr > 115:
            red_flags.append(f"Tachycardia Alert: Heart Rate is {hr} BPM.")
            if triage_level != "CRITICAL EMERGENCY":
                triage_level = "URGENT"

        if temp >= 39.0:
            red_flags.append(f"High Pyrexia: Body Temperature is {temp}°C (>= 102.2°F).")
            if triage_level != "CRITICAL EMERGENCY":
                triage_level = "URGENT"

        if '/' in bp_str:
            systolic = float(bp_str.split('/')[0])
            if systolic >= 180:
                red_flags.append(f"Hypertensive Crisis Alert: Systolic BP {systolic} mmHg (>= 180 mmHg).")
                triage_level = "CRITICAL EMERGENCY"
    except Exception:
        pass

    # Check emergency symptoms
    emergency_symptoms = {"chest_pain", "stiff_neck", "shortness_of_breath"}
    detected_emergency = [s for s in symptoms if s in emergency_symptoms]
    if detected_emergency:
        if triage_level != "CRITICAL EMERGENCY":
            triage_level = "URGENT"
        red_flags.append(f"High-Risk Signal(s) Observed: {', '.join(s.replace('_', ' ') for s in detected_emergency)}")

    return jsonify({
        "status": "success",
        "triage_level": triage_level,
        "red_flags": red_flags,
        "vitals_evaluated": vitals
    })

# --- AI Inference Engines API ---
@app.route('/api/forward-chain', methods=['POST'])
def api_forward_chain():
    data = request.get_json() or {}
    symptoms = data.get('symptoms', [])
    if not symptoms:
        return jsonify({
            "status": "error",
            "message": "No symptoms provided. Please select at least one clinical symptom."
        }), 400

    results = run_forward_chaining(kb.get_all_rules(), symptoms)

    return jsonify({
        "status": "success",
        "mode": "Forward Chaining",
        "input_symptoms": symptoms,
        "matches_found": len(results),
        "results": results
    })

@app.route('/api/backward-chain', methods=['POST'])
def api_backward_chain():
    data = request.get_json() or {}
    target = data.get('target', '').strip()
    symptoms = data.get('symptoms', [])
    if not target:
        return jsonify({
            "status": "error",
            "message": "Target disease hypothesis is required for Backward Chaining."
        }), 400

    result = run_backward_chaining(kb.get_all_rules(), target, symptoms)

    return jsonify({
        "status": "success",
        "mode": "Backward Chaining",
        "target_disease": target,
        "input_symptoms": symptoms,
        "result": result
    })

# Backward-compatible diagnostic endpoint
@app.route('/diagnose', methods=['POST'])
def api_diagnose_compat():
    data = request.get_json() or {}
    mode = data.get('mode', 'forward')
    symptoms = data.get('symptoms', [])
    target = data.get('target', '')

    if mode == 'backward':
        result = run_backward_chaining(kb.get_all_rules(), target, symptoms)
        return jsonify({
            "status": "success",
            "mode": "Backward Chaining",
            "result": result
        })
    else:
        results = run_forward_chaining(kb.get_all_rules(), symptoms)
        return jsonify({
            "status": "success",
            "mode": "Forward Chaining",
            "results": results,
            "input_symptoms": symptoms
        })

# --- Validation Lab Automated Test Suite API ---
@app.route('/api/test', methods=['POST'])
def api_test():
    test_cases = [
        {"name": "Test 01: Pneumonia Symptoms", "symptoms": ["fever", "cough", "fatigue", "shortness_of_breath"], "mode": "forward", "expected": "Common Pneumonia"},
        {"name": "Test 02: Influenza Symptoms", "symptoms": ["fever", "headache", "muscle_pain", "fatigue"], "mode": "forward", "expected": "Viral Influenza (Flu)"},
        {"name": "Test 03: Meningitis Emergency", "symptoms": ["fever", "headache", "stiff_neck", "sensitivity_to_light"], "mode": "forward", "expected": "Meningitis"},
        {"name": "Test 04: Backward Chaining Valid", "target": "Common Pneumonia", "symptoms": ["fever", "cough", "fatigue", "shortness_of_breath"], "mode": "backward", "expected": "Verified"},
        {"name": "Test 05: Backward Chaining Partial", "target": "Dengue Fever", "symptoms": ["fever", "headache"], "mode": "backward", "expected": "Unverified (Missing Evidence)"}
    ]

    test_results = []
    for tc in test_cases:
        if tc["mode"] == "forward":
            res = run_forward_chaining(kb.get_all_rules(), tc["symptoms"])
            passed = len(res) > 0 and res[0]["is_full_match"] and res[0]["diagnosis"] == tc["expected"]
            top_diagnosis = res[0]['diagnosis'] if res else 'No Match'
            test_results.append({
                "test_name": tc["name"],
                "strategy": "Forward Chaining",
                "input": ", ".join(tc["symptoms"]),
                "expected": tc["expected"],
                "actual": top_diagnosis,
                "status": "PASS" if passed else "FAIL",
                "details": f"Derived: {top_diagnosis} ({res[0]['match_ratio']}% match)" if res else "No rules fired"
            })
        else:
            res = run_backward_chaining(kb.get_all_rules(), tc["target"], tc["symptoms"])
            if tc["expected"] == "Verified":
                passed = res.get("matched") is True
                actual_str = "Verified (100% satisfied)" if res.get("matched") else "Unverified"
            else:
                passed = (res.get("matched") is False) and (len(res.get("missing_symptoms", [])) > 0)
                actual_str = f"Unverified (Missing: {', '.join(res.get('missing_symptoms', []))})"

            test_results.append({
                "test_name": tc["name"],
                "strategy": "Backward Chaining",
                "input": f"Target: {tc['target']} | Symptoms: {', '.join(tc['symptoms'])}",
                "expected": tc["expected"],
                "actual": actual_str,
                "status": "PASS" if passed else "FAIL",
                "details": f"Target: {tc['target']} | Satisfied: {len(res.get('satisfied_symptoms', []))} | Missing: {len(res.get('missing_symptoms', []))}"
            })

    total_tests = len(test_cases)
    passed_tests = sum(1 for t in test_results if t["status"] == "PASS")

    return jsonify({
        "status": "success",
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "success_rate": f"{round((passed_tests / total_tests) * 100, 1)}%",
        "test_results": test_results
    })

# --- Cloud & Execution Entrypoint ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"[*] Starting AI Clinical Decision Support Platform on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)
