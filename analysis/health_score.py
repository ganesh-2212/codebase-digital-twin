class HealthScore:

    def calculate(
        self,
        smells=0,
        cycles=0,
        violations=0,
        high_risk_components=0
    ):

        score = 100

        # Architecture smells
        score -= smells * 2

        # Circular dependencies are severe architecture issues
        score -= cycles * 8

        # Layer violations reduce architecture quality
        score -= violations * 4

        # Components with high blast radius increase maintenance risk
        score -= high_risk_components * 2

        return max(score, 0)

    def get_status(
        self,
        score
    ):

        if score >= 90:
            return "Excellent"

        if score >= 75:
            return "Good"

        if score >= 60:
            return "Fair"

        if score >= 40:
            return "Poor"

        return "Critical"

    def evaluate(
        self,
        smells=0,
        cycles=0,
        violations=0,
        high_risk_components=0
    ):

        score = self.calculate(
            smells,
            cycles,
            violations,
            high_risk_components
        )

        return {
            "score": score,
            "status": self.get_status(score),
            "breakdown": {
                "smells": smells,
                "circular_dependencies": cycles,
                "layer_violations": violations,
                "high_risk_components": high_risk_components
            }
        }