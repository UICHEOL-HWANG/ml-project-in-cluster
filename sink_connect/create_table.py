import psycopg2
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv

# 환경 변수에서 PostgreSQL 연결 정보 로드
USER = "targetuser"
PASSWORD = "targetpassword"
DB = "targetdatabase"


def create_table(db_connect):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS vital_statistics(
    birth_rate FLOAT,
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

if __name__ == "__main__":
    db_connect = None
    try:
        db_connect = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="target-postgres-server",
            port=5432,
            database=DB,
        )
        create_table(db_connect)
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
    finally:
        if db_connect is not None:
            db_connect.close()
