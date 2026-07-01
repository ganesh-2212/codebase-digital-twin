from analysis.impact_analyzer import (
    ImpactAnalyzer
)

analyzer = ImpactAnalyzer()

target = "fastapi/routing.py"

results = analyzer.analyze(
    target,
    depth=2
)

print("\nImpact Results:\n")

for r in results:

    print(r)