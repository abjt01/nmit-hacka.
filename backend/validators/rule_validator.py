from typing import Dict, List, Tuple

class RuleValidator:
    """Physics and common-sense validation rules"""
    
    @staticmethod
    def validate_problem(problem_data: Dict) -> Tuple[bool, List[str]]:
        """Apply rule-based checks for impossible scenarios"""
        errors = []
        
        params = problem_data.get("parameters", {})
        category = problem_data.get("category", "")
        
        # Speed validation
        if "speed" in str(params).lower():
            for key, value in params.items():
                if "speed" in key.lower():
                    if value < 0:
                        errors.append(f"Negative speed: {key} = {value}")
                    if value > 500:
                        errors.append(f"Unrealistic speed: {key} = {value} km/h")
        
        # Time validation
        if "time" in str(params).lower() or "hour" in str(params).lower():
            for key, value in params.items():
                if any(word in key.lower() for word in ["time", "hour", "minute"]):
                    if value < 0:
                        errors.append(f"Negative time: {key} = {value}")
                    if value > 100:
                        errors.append(f"Unrealistic time: {key} = {value}")
        
        # Distance validation
        if "distance" in str(params).lower():
            for key, value in params.items():
                if "distance" in key.lower():
                    if value < 0:
                        errors.append(f"Negative distance: {key} = {value}")
                    if value > 10000:
                        errors.append(f"Unrealistic distance: {key} = {value} km")
        
        # Work rate validation
        if "work" in category.lower():
            for key, value in params.items():
                if "days" in key.lower() or "rate" in key.lower():
                    if value <= 0:
                        errors.append(f"Invalid work parameter: {key} = {value}")
                    if value > 365:
                        errors.append(f"Unrealistic work duration: {key} = {value} days")
        
        # MCQ validation
        options = problem_data.get("options", {})
        if options:
            values = []
            for opt_val in options.values():
                try:
                    # Extract numeric part
                    num = float(''.join(filter(lambda x: x.isdigit() or x in '.-', str(opt_val))))
                    values.append(num)
                except:
                    pass
            
            # Check for duplicate options
            if len(values) != len(set(values)):
                errors.append("Duplicate option values detected")
            
            # Check if options are reasonably spaced
            if values:
                values_sorted = sorted(values)
                for i in range(len(values_sorted) - 1):
                    if abs(values_sorted[i+1] - values_sorted[i]) < 0.01:
                        errors.append("Options too close together")
                        break
        
        return len(errors) == 0, errors
