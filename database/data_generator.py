import time
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("./database/.env.prod")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def get_data():
    df = pd.read_csv('/usr/app/one_hot_encoded_statistics.csv',encoding="utf-8")
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ', '_') 
    return df

def create_table(db_connect):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS vital_statistics(
    Birth_rate FLOAT,
    Death_rate FLOAT,
    Natural_increase_rate FLOAT,
    Marrige_rate FLOAT,
    Divorce_rate FLOAT,
    Year INT,
    Month INT,
    Region_Busan INT, 
    Region_Chungcheongbuk_do INT,  
    Region_Chungcheongnam_do INT,  
    Region_Daegu INT,
    Region_Daejeon INT,
    Region_Gangwon_do INT,         
    Region_Gwangju INT,
    Region_Gyeonggi_do INT,        
    Region_Gyeongsangbuk_do INT,   
    Region_Gyeongsangnam_do INT,   
    Region_Incheon INT,
    Region_Jeju INT,
    Region_Jeollabuk_do INT,       
    Region_Jeollanam_do INT,       
    Region_Sejong INT,
    Region_Seoul INT,
    Region_Ulsan INT,
    ID SERIAL PRIMARY KEY
);
"""
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()

def insert_data(db_connect, data):
    insert_query = """
    INSERT INTO vital_statistics (
        Birth_rate, Death_rate, Natural_increase_rate, Marrige_rate, Divorce_rate,
        Year, Month, Region_Busan, Region_Chungcheongbuk_do, Region_Chungcheongnam_do, 
        Region_Daegu, Region_Daejeon, Region_Gangwon_do, Region_Gwangju, 
        Region_Gyeonggi_do, Region_Gyeongsangbuk_do, Region_Gyeongsangnam_do, 
        Region_Incheon, Region_Jeju, Region_Jeollabuk_do, Region_Jeollanam_do, 
        Region_Sejong, Region_Seoul, Region_Ulsan
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s
    );
    """
    with db_connect.cursor() as cur:
        cur.execute(insert_query, (
            data['Birth_rate'], data['Death_rate'], data['Natural_increase_rate'],
            data['Marrige_rate'], data['Divorce_rate'], data['Year'], data['Month'],
            data['Region_Busan'], data['Region_Chungcheongbuk_do'], 
            data['Region_Chungcheongnam_do'], data['Region_Daegu'], data['Region_Daejeon'], 
            data['Region_Gangwon_do'], data['Region_Gwangju'], data['Region_Gyeonggi_do'], 
            data['Region_Gyeongsangbuk_do'], data['Region_Gyeongsangnam_do'], data['Region_Incheon'], 
            data['Region_Jeju'], data['Region_Jeollabuk_do'], data['Region_Jeollanam_do'], 
            data['Region_Sejong'], data['Region_Seoul'], data['Region_Ulsan']
        ))
        db_connect.commit()

def generate_data(db_connect, df):
    try:
        while True:
            insert_data(db_connect, df.sample(1).squeeze())
            time.sleep(1)  # 주기 조정 가능
    except KeyboardInterrupt:
        print("Data generation interrupted.")

if __name__ == "__main__":
    try:
        db_connect = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host="db",  # Docker Compose 내에서 정의된 데이터베이스 서비스 이름
            port=5432,
            database=POSTGRES_DB,
        )
        df = get_data()
        create_table(db_connect)
        generate_data(db_connect, df)
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        db_connect.close()
