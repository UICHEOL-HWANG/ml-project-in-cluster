import mlflow
import pandas as pd 
from fastapi import FastAPI
from schemas import PredictIn, PredictOut
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from router.data import data_serve
from fastapi.middleware.cors import CORSMiddleware

def get_model():
    model = mlflow.sklearn.load_model(model_uri="./sk_model")
    return model


MODEL = get_model()

# Create a FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict", response_model=PredictOut)
def predict(data: PredictIn) -> PredictOut:
    data_dict = data.dict()
    data_dict.pop('birth_rate', None) 
    df = pd.DataFrame([data_dict])
    pred = MODEL.predict(df).item()

    birth_rate = data.birth_rate
    
    mse = mean_squared_error([birth_rate], [pred])
    mae = mean_absolute_error([birth_rate], [pred])
    r2 = r2_score([birth_rate], [pred])
    
    # Ensure non-negative values for the metrics
    mse = max(0, mse)
    mae = max(0, mae)
    r2 = max(0, r2)
    
    return PredictOut(mse=mse, mae=mae, r2=r2)

app.include_router(data_serve.router)