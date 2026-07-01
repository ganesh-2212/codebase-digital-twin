from analysis.architecture_impact import (
    ArchitectureImpactAnalyzer
)

analyzer = ArchitectureImpactAnalyzer()

result = analyzer.analyze(
    "APIRouter"
)

print(result)