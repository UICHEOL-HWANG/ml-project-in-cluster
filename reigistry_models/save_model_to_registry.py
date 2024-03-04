import pandas as pd
import os 
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
import mlflow
from argparse import ArgumentParser

# database 관련 환경 변수 로드
os.environ['POSTGRES_USER'] = "Sesac"
os.environ['POSTGRES_PASSWORD'] = "Sesac"
os.environ['POSTGRES_DB'] = "Sesac_db"

# MLflow 관련 환경 변수 설정
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"

# 데이터베이스 연결
connection_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("POSTGRES_DB")}'
engine = create_engine(connection_string)
df = pd.read_sql("SELECT * FROM vital_statistics", engine)
target = 'birth_rate'
features = df.columns.drop(target)
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# 모델 학습
rfr = RandomForestRegressor()
rfr.fit(X_train, y_train)

# 모델 평가
pred = rfr.predict(X_test)
mse = mean_squared_error(y_test, pred)
mae = mean_absolute_error(y_test, pred)
r2 = r2_score(y_test, pred)

# 명령행 인자 파싱
parser = ArgumentParser()
parser.add_argument("--model-name", dest="model_name", type=str, default="sk_model")
args = parser.parse_args()

# MLflow 실험 설정
mlflow.set_experiment("new-exp")

# 모델 서명 및 입력 예제
signature = mlflow.models.signature.infer_signature(model_input=X_train, model_output=pred)
input_sample = X_train.iloc[:10]

# MLflow에 모델 로깅
with mlflow.start_run():
    mlflow.log_metrics({"mse": mse, "mae": mae, "r2": r2})
    mlflow.sklearn.log_model(
        sk_model=rfr,
        artifact_path=args.model_name,
        signature=signature,
        input_example=input_sample,
    )
