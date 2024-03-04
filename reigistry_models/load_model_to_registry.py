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

# database 관련 환경 변수 설정
os.environ['POSTGRES_USER'] = "Sesac"
os.environ['POSTGRES_PASSWORD'] = "Sesac"
os.environ['POSTGRES_DB'] = "Sesac_db"


os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"


parser = ArgumentParser()
parser.add_argument("--model-name", dest="model_name", type=str, default="sk_model")
parser.add_argument("--run-id", dest="run_id", type=str)
args = parser.parse_args()

model_pipeline = mlflow.sklearn.load_model(f"runs:/{args.run_id}/{args.model_name}")


connection_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("POSTGRES_DB")}'
engine = create_engine(connection_string)
df = pd.read_sql("SELECT * FROM vital_statistics", engine)
target = 'birth_rate'
features = df.columns.drop(target)
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

model_pipeline.fit(X_train, y_train)  # 모델 훈련

# 테스트 데이터를 사용하여 예측값 계산
y_pred = model_pipeline.predict(X_test)

# 예측값과 실제값을 사용하여 평가 지표 계산
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 결과 출력
print(f'mse: {mse}')
print(f'mae: {mae}')
print(f'r2: {r2}')

