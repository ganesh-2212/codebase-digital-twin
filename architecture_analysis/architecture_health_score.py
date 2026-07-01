import requests


class ArchitectureHealthScore:

    def calculate(self):

        score = 100
        breakdown = {}

        # =====================================
        # FETCH METRICS
        # =====================================
        cycles = self.safe_get("http://127.0.0.1:8000/circular-dependencies")
        violations = self.safe_get("http://127.0.0.1:8000/layer-violations")
        smells = self.safe_get("http://127.0.0.1:8000/smells")

        cycle_count = cycles.get("count", 0)
        violation_count = violations.get("count", 0)
        smell_count = len(smells.get("smells", []))

        # =====================================
        # NORMALIZATION BASE (IMPORTANT FIX)
        # =====================================
        total = max(smell_count + violation_count + cycle_count, 1)

        # =====================================
        # CIRCULAR DEPENDENCIES (HIGHEST WEIGHT)
        # =====================================
        cycle_penalty = min((cycle_count / total) * 100, 25)
        score -= cycle_penalty

        breakdown["circular_dependencies"] = {
            "count": cycle_count,
            "penalty": round(cycle_penalty, 2)
        }

        # =====================================
        # LAYER VIOLATIONS
        # =====================================
        violation_penalty = min((violation_count / total) * 80, 20)
        score -= violation_penalty

        breakdown["layer_violations"] = {
            "count": violation_count,
            "penalty": round(violation_penalty, 2)
        }

        # =====================================
        # SMELLS (NORMALIZED)
        # =====================================
        smell_penalty = min((smell_count / total) * 60, 30)
        score -= smell_penalty

        breakdown["smells"] = {
            "count": smell_count,
            "penalty": round(smell_penalty, 2)
        }

        # =====================================
        # HIGH RISK COMPONENTS (DERIVED)
        # =====================================
        high_risk = min(smell_count // 10, 20)
        risk_penalty = (high_risk / max(total, 1)) * 20
        score -= risk_penalty

        breakdown["high_risk_components"] = {
            "count": high_risk,
            "penalty": round(risk_penalty, 2)
        }

        # =====================================
        # FINAL SCORE NORMALIZATION
        # =====================================
        score = max(0, min(100, round(score, 2)))

        # =====================================
        # STATUS MAPPING
        # =====================================
        if score >= 85:
            status = "Excellent"
        elif score >= 70:
            status = "Good"
        elif score >= 50:
            status = "Fair"
        elif score >= 30:
            status = "Poor"
        else:
            status = "Critical"

        return {
            "score": score,
            "status": status,
            "breakdown": breakdown
        }

    # =====================================
    # SAFE API CALL
    # =====================================
    def safe_get(self, url):
        try:
            return requests.get(url, timeout=3).json()
        except:
            return {}