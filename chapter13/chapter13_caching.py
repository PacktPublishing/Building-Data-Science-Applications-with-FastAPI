import os
from typing import List, Optional, Tuple

import joblib
from fastapi import FastAPI, Depends, status
from joblib import memory
from pydantic import BaseModel
from sklearn.pipeline import Pipeline


class PredictionInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    category: str


memory = joblib.Memory(location="cache.joblib")


@memory.cache(ignore=["model"])
def predict(model: Pipeline, text: str) -> int:
    prediction = model.predict([text])
    return prediction[0]


class NewsgroupsModel:
    model: Optional[Pipeline]
    targets: Optional[List[str]]

    def load_model(self):
        """Loads the model"""
        model_file = os.path.join(os.path.dirname(__file__), "newsgroups_model.joblib")
        loaded_model: Tuple[Pipeline, List[str]] = joblib.load(model_file)
        model, targets = loaded_model
        self.model = model
        self.targets = targets

    def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model or not self.targets:
            raise RuntimeError("Model is not loaded")
        prediction = predict(self.model, input.text)
        category = self.targets[prediction]
        return PredictionOutput(category=category)


app = FastAPI()
newgroups_model = NewsgroupsModel()


@app.post("/prediction")
def prediction(
    output: PredictionOutput = Depends(newgroups_model.predict),
) -> PredictionOutput:
    return output


@app.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
def delete_cache():
    memory.clear()


@app.on_event("startup")
async def startup():
    newgroups_model.load_model()
