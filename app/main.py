import uvicorn
import numpy as np
from typing import List, Union
from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel, conlist

# create FastAPI app
app = FastAPI(title="Predicting whether an NBA player is worth an investment")


# Represents a nba player stats data point
#  features : array(['GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB'], dtype=object)),
class NbaPlayerStat(BaseModel):
    gp: float
    Min: float
    pts: float
    fgm: float
    fga: float
    ftm: float
    fta: float
    oreb: float
    dreb: float
    reb: float


# Represents a batch of nba player stats
class NbaPlayerStats(BaseModel):
    batches: List[conlist(item_type=float, min_items=10, max_items=10)]


@app.get("/")
def home():
    return "Welcome to NBA Player Career Longevity Prediction API. Now head over to http://localhost:8000/docs."


@app.on_event("startup")
def load_model():
    # Load model from pickle file
    global model
    try:
        # (AdaBoostClassifier(algorithm='SAMME', base_estimator=SGDClassifier(), n_estimators=20, random_state=2024),  'RFE_LogisticRegression with adaBoostClassifier', 0.8778704276856298,
        #  features : array(['GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB'], dtype=object)),
        model = joblib.load("app/best_model_for_cautious_investors_v0.pkl")
    except Exception as e:
        print(f"Error loading the model: {e}")
        model = None
    return model


@app.post("/predict")
def prediction(data: Union[NbaPlayerStats, NbaPlayerStat], batch: bool):

    # checking model load
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        pred = None
        if batch:  # batch mode activated
            # handling data
            batches = data.batches
            np_batches = np.array(batches)
            # inference
            pred = model.predict(np_batches).tolist()

        else:  # no bacth
            data_point = np.array(
                [
                    [
                        data.gp,
                        data.Min,
                        data.pts,
                        data.fgm,
                        data.fga,
                        data.ftm,
                        data.fta,
                        data.oreb,
                        data.dreb,
                        data.reb,
                    ]
                ]
            )
            # inference
            pred = model.predict(data_point).tolist()
            pred = pred[0]

        return {"Prediction": pred}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# if __name__ == "__main__":
#     host = "127.0.0.1"
#     # Spin up the server!
#     uvicorn.run(app, host=host, port=8000)
