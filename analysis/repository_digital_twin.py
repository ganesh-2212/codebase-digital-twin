from analysis.reasoning_engine_v4 import (
    ReasoningEngineV4
)

from analysis.change_impact_predictor import (
    ChangeImpactPredictor
)


class RepositoryDigitalTwin:

    def __init__(self):

        self.reasoner = (
            ReasoningEngineV4()
        )

        self.predictor = (
            ChangeImpactPredictor()
        )

    # ==========================================
    # REPOSITORY Q&A
    # ==========================================

    def answer(
        self,
        query
    ):

        return self.reasoner.reason(
            query
        )

    # ==========================================
    # CHANGE IMPACT PREDICTION
    # ==========================================

    def predict_change(
        self,
        component
    ):

        return self.predictor.predict(
            component
        )


if __name__ == "__main__":

    twin = RepositoryDigitalTwin()

    while True:

        print("\n======================")
        print("Repository Digital Twin")
        print("======================")
        print("1. Ask Question")
        print("2. Predict Change Impact")
        print("3. Exit")

        choice = input(
            "\nChoice: "
        )

        if choice == "1":

            query = input(
                "\nQuestion: "
            )

            answer = twin.answer(
                query
            )

            print("\n")
            print(answer)

        elif choice == "2":

            component = input(
                "\nComponent: "
            )

            result = twin.predict_change(
                component
            )

            print("\n")

            for k, v in result.items():

                print(
                    f"{k}: {v}"
                )

        elif choice == "3":

            print(
                "\nExiting Digital Twin..."
            )

            break

        else:

            print(
                "\nInvalid choice"
            )