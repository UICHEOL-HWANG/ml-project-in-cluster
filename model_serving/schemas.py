from pydantic import BaseModel, Field
from typing import Optional


class PredictIn(BaseModel):
    birth_rate: float
    death_rate: float
    natural_increase_rate: float
    marrige_rate: float
    divorce_rate: float
    year: int
    month: int
    region_busan: int 
    region_chungcheongbuk_do: int  
    region_chungcheongnam_do: int  
    region_daegu: int
    region_daejeon: int
    region_gangwon_do: int         
    region_gwangju: int
    region_gyeonggi_do: int        
    region_gyeongsangbuk_do: int   
    region_gyeongsangnam_do: int   
    region_incheon: int
    region_jeju: int
    region_jeollabuk_do: int       
    region_jeollanam_do: int       
    region_sejong: int
    region_seoul: int
    region_ulsan: int
    id: Optional[int] = Field(None, alias='id')

class PredictOut(BaseModel):
    mse : float 
    mae : float 
    r2 : float 
    

class DataServing(BaseModel):
    birth_rate: float
    death_rate: float
    natural_increase_rate: float
    marrige_rate: float
    divorce_rate: float
    year: int
    month: int
    region_busan: int 
    region_chungcheongbuk_do: int  
    region_chungcheongnam_do: int  
    region_daegu: int
    region_daejeon: int
    region_gangwon_do: int         
    region_gwangju: int
    region_gyeonggi_do: int        
    region_gyeongsangbuk_do: int   
    region_gyeongsangnam_do: int   
    region_incheon: int
    region_jeju: int
    region_jeollabuk_do: int       
    region_jeollanam_do: int       
    region_sejong: int
    region_seoul: int
    region_ulsan: int
    id: Optional[int] = Field(None, alias='id')