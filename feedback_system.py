import json
import os
from datetime import datetime
from typing import Dict, List

class FeedbackSystem:
    def __init__(self, feedback_file="feedback.json"):
        self.feedback_file = feedback_file
        self.feedback_data = self._load_feedback()
    
    def _load_feedback(self) -> List[Dict]:
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_feedback(self):
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def add_feedback(self, code: str, finding_type: str, is_false_positive: bool, user_comment: str = ""):
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "code_hash": hash(code),
            "finding_type": finding_type,
            "is_false_positive": is_false_positive,
            "user_comment": user_comment
        }
        self.feedback_data.append(feedback_entry)
        self._save_feedback()
    
    def get_false_positive_rate(self, finding_type: str = None) -> float:
        relevant_feedback = self.feedback_data
        if finding_type:
            relevant_feedback = [f for f in self.feedback_data if f['finding_type'] == finding_type]
        
        if not relevant_feedback:
            return 0.0
        
        false_positives = sum(1 for f in relevant_feedback if f['is_false_positive'])
        return false_positives / len(relevant_feedback)