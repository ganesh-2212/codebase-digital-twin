from analysis.change_impact_predictor import (
    ChangeImpactPredictor
)

predictor = ChangeImpactPredictor()

result = predictor.predict(
    "APIRouter"
)

for k, v in result.items():

    print(k, ":", v)