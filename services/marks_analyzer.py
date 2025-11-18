# marks_analyzer.py
class MarksAnalyzer:
    def adjust(self, counts: dict, target_total: int) -> dict:
        """Adjust marks distribution to reach target total"""
        total_questions = sum(counts.values())
        
        if total_questions == 0:
            return {'mcq': 1, 'short': 4, 'long': 10}
        
        # Simple proportional distribution
        base_marks = {
            'mcq': 1,
            'short': 4, 
            'long': 10
        }
        
        current_total = (counts['mcq'] * base_marks['mcq'] + 
                        counts['short'] * base_marks['short'] + 
                        counts['long'] * base_marks['long'])
        
        if current_total == target_total:
            return base_marks
        
        # Adjust proportionally
        ratio = target_total / current_total
        adjusted_marks = {
            'mcq': max(1, round(base_marks['mcq'] * ratio)),
            'short': max(2, round(base_marks['short'] * ratio)),
            'long': max(5, round(base_marks['long'] * ratio))
        }
        
        return adjusted_marks