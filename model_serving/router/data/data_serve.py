import psycopg2
import pandas as pd 
from fastapi import APIRouter, Depends
from database import get_db

router = APIRouter()

@router.get("/vital_statistics")
def read_all_vital_statistics(connection=Depends(get_db)):
    # 데이터를 Pandas DataFrame으로 변환
    data = pd.read_sql("SELECT * FROM vital_statistics", con=connection)

    regions = ['region_busan', 'region_chungcheongbuk_do', 'region_chungcheongnam_do', 'region_daegu', 'region_daejeon', 'region_gangwon_do',
           'region_gwangju', 'region_gyeonggi_do', 'region_gyeongsangbuk_do', 'region_gyeongsangnam_do', 'region_incheon', 'region_jeju',
           'region_jeollabuk_do', 'region_jeollanam_do', 'region_sejong', 'region_seoul', 'region_ulsan']
    data['region'] = data[regions].idxmax(axis=1)

    data.drop(regions + ['id'], axis=1, inplace=True)
    
    return data.to_dict(orient='records')


@router.get("/groupby_vital")
def read_groupby_vital(connection=Depends(get_db)):
    data = pd.read_sql("SELECT * FROM vital_statistics", con=connection)

    regions = ['region_busan', 'region_chungcheongbuk_do', 'region_chungcheongnam_do', 'region_daegu', 'region_daejeon', 'region_gangwon_do',
           'region_gwangju', 'region_gyeonggi_do', 'region_gyeongsangbuk_do', 'region_gyeongsangnam_do', 'region_incheon', 'region_jeju',
           'region_jeollabuk_do', 'region_jeollanam_do', 'region_sejong', 'region_seoul', 'region_ulsan']
    data['region'] = data[regions].idxmax(axis=1)
    data.drop(regions + ['id'], axis=1, inplace=True)
    # Correcting the year values
    data['year'] = data['year'].apply(lambda x: x + 2000 if x < 100 else x)

    # Recreating the date column with the corrected year values
    data['date'] = pd.to_datetime(data['year'].astype(str) + '-' + data['month'].astype(str))
    data = data.drop(['region','year','month','natural_increase_rate','marrige_rate','divorce_rate'],axis=1)
    # Grouping the data by date again and calculating the mean for each rate
    grouped_data = data.groupby('date').mean().reset_index()

    return grouped_data.to_dict(orient='records')


@router.get("/groupby_divorce")
def read_groupby_vital(connection=Depends(get_db)):
    data = pd.read_sql("SELECT * FROM vital_statistics", con=connection)

    regions = ['region_busan', 'region_chungcheongbuk_do', 'region_chungcheongnam_do', 'region_daegu', 'region_daejeon', 'region_gangwon_do',
           'region_gwangju', 'region_gyeonggi_do', 'region_gyeongsangbuk_do', 'region_gyeongsangnam_do', 'region_incheon', 'region_jeju',
           'region_jeollabuk_do', 'region_jeollanam_do', 'region_sejong', 'region_seoul', 'region_ulsan']
    data['region'] = data[regions].idxmax(axis=1)
    data.drop(regions + ['id'], axis=1, inplace=True)
    # Correcting the year values
    data['year'] = data['year'].apply(lambda x: x + 2000 if x < 100 else x)

    # Recreating the date column with the corrected year values
    data['date'] = pd.to_datetime(data['year'].astype(str) + '-' + data['month'].astype(str))
    data = data.drop(['region','year','month','natural_increase_rate'],axis=1)
    # Grouping the data by date again and calculating the mean for each rate
    grouped_data = data.groupby('date').mean().reset_index()

    return grouped_data.to_dict(orient='records')


@router.get("/region_death")
def read_groupby_vital(connection=Depends(get_db)):
    data = pd.read_sql("SELECT * FROM vital_statistics", con=connection)

    regions = ['region_busan', 'region_chungcheongbuk_do', 'region_chungcheongnam_do', 'region_daegu', 'region_daejeon', 'region_gangwon_do',
           'region_gwangju', 'region_gyeonggi_do', 'region_gyeongsangbuk_do', 'region_gyeongsangnam_do', 'region_incheon', 'region_jeju',
           'region_jeollabuk_do', 'region_jeollanam_do', 'region_sejong', 'region_seoul', 'region_ulsan']
    data['region'] = data[regions].idxmax(axis=1)
    data.drop(regions + ['id'], axis=1, inplace=True)
    # Correcting the year values
    data['year'] = data['year'].apply(lambda x: x + 2000 if x < 100 else x)

    # Recreating the date column with the corrected year values
    data['date'] = pd.to_datetime(data['year'].astype(str) + '-' + data['month'].astype(str))
    data = data.drop(['date','year','month','natural_increase_rate','divorce_rate','marrige_rate'],axis=1)
    # Grouping the data by date again and calculating the mean for each rate
    grouped_data = data.groupby('region').mean().reset_index()

    return grouped_data.to_dict(orient='records')

@router.get("/region_death")
def read_groupby_vital(connection=Depends(get_db)):
    data = pd.read_sql("SELECT * FROM vital_statistics", con=connection)

    regions = ['region_busan', 'region_chungcheongbuk_do', 'region_chungcheongnam_do', 'region_daegu', 'region_daejeon', 'region_gangwon_do',
           'region_gwangju', 'region_gyeonggi_do', 'region_gyeongsangbuk_do', 'region_gyeongsangnam_do', 'region_incheon', 'region_jeju',
           'region_jeollabuk_do', 'region_jeollanam_do', 'region_sejong', 'region_seoul', 'region_ulsan']
    data['region'] = data[regions].idxmax(axis=1)
    data.drop(regions + ['id'], axis=1, inplace=True)
    # Correcting the year values
    data['year'] = data['year'].apply(lambda x: x + 2000 if x < 100 else x)

    # Recreating the date column with the corrected year values
    data['date'] = pd.to_datetime(data['year'].astype(str) + '-' + data['month'].astype(str))
    data = data.drop(['date','year','month','natural_increase_rate','divorce_rate','marrige_rate'],axis=1)
    # Grouping the data by date again and calculating the mean for each rate
    grouped_data = data.groupby('region').mean().reset_index()

    return grouped_data.to_dict(orient='records')


@router.get("/natural_increase_rate")
def read_groupby_vital(connection=Depends(get_db)):
    data = pd.read_sql("SELECT * FROM vital_statistics", con=connection)

    regions = ['region_busan', 'region_chungcheongbuk_do', 'region_chungcheongnam_do', 'region_daegu', 'region_daejeon', 'region_gangwon_do',
           'region_gwangju', 'region_gyeonggi_do', 'region_gyeongsangbuk_do', 'region_gyeongsangnam_do', 'region_incheon', 'region_jeju',
           'region_jeollabuk_do', 'region_jeollanam_do', 'region_sejong', 'region_seoul', 'region_ulsan']
    data['region'] = data[regions].idxmax(axis=1)
    data.drop(regions + ['id'], axis=1, inplace=True)
    # Correcting the year values
    data['year'] = data['year'].apply(lambda x: x + 2000 if x < 100 else x)

    # Recreating the date column with the corrected year values
    data['date'] = pd.to_datetime(data['year'].astype(str) + '-' + data['month'].astype(str))
    data = data.drop(['date','year','month','divorce_rate','marrige_rate'],axis=1)
    # Grouping the data by date again and calculating the mean for each rate
    grouped_data = data.groupby('region')['natural_increase_rate'].mean().reset_index()

    return grouped_data.to_dict(orient='records')
