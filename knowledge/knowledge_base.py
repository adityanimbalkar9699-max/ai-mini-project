import json
import os

class KnowledgeBase:
    def __init__(self, filepath=None):
        if filepath is None:
            filepath = os.path.join(os.path.dirname(__file__), 'rules.json')
        self.filepath = filepath
        self.rules = self.load_rules()

    def load_rules(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading rules.json: {e}")
            return []

    def get_all_rules(self):
        return self.rules

    def get_all_symptoms(self):
        symptoms_set = set()
        for rule in self.rules:
            for s in rule.get("symptoms", []):
                symptoms_set.add(s)
        return sorted(list(symptoms_set))

    def get_all_diseases(self):
        return [
            {
                "id": r["id"],
                "name": r["diagnosis"],
                "category": r.get("category", "General"),
                "severity": r.get("severity", "MODERATE"),
                "icd10": r.get("icd10", "N/A")
            }
            for r in self.rules
        ]

    def get_disease_names(self):
        return [r["diagnosis"] for r in self.rules]

    def get_disease_by_name(self, name):
        target = name.strip().lower()
        for r in self.rules:
            if r["diagnosis"].strip().lower() == target:
                return r
        return None

    def get_categorized_symptoms(self):
        # Human-curated anatomical mapping of the 24+ clinical signals
        category_map = {
            "Cardiovascular": ["chest_pain", "chest_tightness", "sweating", "dizziness"],
            "Respiratory": ["shortness_of_breath", "cough", "wheezing", "sneezing", "runny_nose", "nasal_congestion", "sore_throat"],
            "Neurological": ["headache", "stiff_neck", "sensitivity_to_light"],
            "Gastrointestinal": ["nausea", "vomiting", "diarrhea", "abdominal_pain"],
            "Endocrine & Metabolic": ["increased_thirst", "frequent_urination", "unexplained_weight_loss"],
            "Musculoskeletal": ["joint_pain", "stiffness", "swelling", "reduced_mobility", "muscle_pain"],
            "Immunological & ENT": ["itchy_eyes", "rash"],
            "Systemic / General": ["fever", "fatigue", "weakness", "paleness"]
        }
        return category_map

    def get_case_presets(self):
        return [
            {
                "id": "CASE-01",
                "title": "Code Blue: Acute Myocardial Infarction",
                "patient": {"age": 58, "gender": "Male", "bp": "165/100", "hr": 112, "spo2": 93, "temp": 37.1},
                "symptoms": ["chest_pain", "shortness_of_breath", "sweating", "dizziness"],
                "target_disease": "Myocardial Infarction (Heart Attack)",
                "expected": "Myocardial Infarction (Heart Attack)",
                "mode": "forward",
                "tag": "EMERGENCY"
            },
            {
                "id": "CASE-02",
                "title": "Pediatric/Young Adult: Acute Meningitis Crisis",
                "patient": {"age": 19, "gender": "Female", "bp": "118/76", "hr": 104, "spo2": 98, "temp": 39.4},
                "symptoms": ["fever", "headache", "stiff_neck", "sensitivity_to_light"],
                "target_disease": "Meningitis",
                "expected": "Meningitis",
                "mode": "forward",
                "tag": "EMERGENCY"
            },
            {
                "id": "CASE-03",
                "title": "Pulmonary: Community-Acquired Pneumonia",
                "patient": {"age": 67, "gender": "Male", "bp": "130/84", "hr": 96, "spo2": 90, "temp": 38.8},
                "symptoms": ["fever", "cough", "fatigue", "shortness_of_breath"],
                "target_disease": "Common Pneumonia",
                "expected": "Common Pneumonia",
                "mode": "forward",
                "tag": "URGENT"
            },
            {
                "id": "CASE-04",
                "title": "Metabolic Screening: Suspected Type 2 Diabetes",
                "patient": {"age": 45, "gender": "Female", "bp": "138/88", "hr": 78, "spo2": 99, "temp": 36.8},
                "symptoms": ["increased_thirst", "frequent_urination", "fatigue", "unexplained_weight_loss"],
                "target_disease": "Type 2 Diabetes Mellitus",
                "expected": "Type 2 Diabetes Mellitus",
                "mode": "backward",
                "tag": "ENDOCRINE"
            },
            {
                "id": "CASE-05",
                "title": "Seasonal Outbreak: Influenza vs Dengue Differential",
                "patient": {"age": 28, "gender": "Male", "bp": "110/72", "hr": 88, "spo2": 97, "temp": 39.1},
                "symptoms": ["fever", "headache", "muscle_pain", "fatigue"],
                "target_disease": "Viral Influenza (Flu)",
                "expected": "Viral Influenza (Flu)",
                "mode": "forward",
                "tag": "INFECTIOUS"
            }
        ]

# Global singleton instance
kb = KnowledgeBase()
