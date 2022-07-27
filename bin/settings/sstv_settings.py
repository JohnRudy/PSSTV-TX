from datetime import timedelta
from functools import lru_cache
from pydantic import BaseModel
from tqdm import tqdm, trange
from bin.lib.sstv import MODE

# TODO:
# Find something that actually shows right syncs and timings.

class SSTVSettings():
    class Robot36Settings(BaseModel):
        name:str = 'R36'
        VISCode:int=8 # as decimal
        image_size:tuple = (320,240)
        # More than likely, these are wrong        
        sync_ms:dict[str,int] = {
            'sync pulse' : 9,
            'sync porch' : 3,
            'even separator': 4.5,
            'odd separator': 4.5, 
            'porch' : 1.5,
        }
        sync_hz:dict[str,int] = {
            'sync pulse' : 1200,
            'sync porch' : 1500,
            'even separator': 1500,
            'odd separator' :  2300,
            'porch' : 1900,
        }
        _total_time_ms:float = 36000
        y_pixel_ms:float = 88 / image_size[0]
        rb_pixel_ms:float = 44 / image_size[0]

    class WSC2120Settings(BaseModel):
        name:str = 'WSC2120'
        VISCode:int=63 # as decimal
        image_size:tuple = (320,256)
        # These might be wrong as well. 
        sync_ms:dict[str,int] = {
            'sync pulse' : 5,
        }
        sync_hz:dict[str,int] = {
            'sync pulse' : 1200,
        }
        _total_time_ms:float = 12000
        green_pixel_ms:float = 235 / 320
        redblue_pixel_ms:float = 117 / 320

    class WSC2180Settings(BaseModel):
        name:str = 'WSC2180'
        VISCode:int=55 # as decimal
        image_size:tuple = (320,256)
        sync_ms:dict[str,int] = {
            'sync pulse' : 5.5225,
            'sync porch' : 0.5
        }
        sync_hz:dict[str,int] = {
            'sync pulse' : 1200,
            'sync porch' : 1500
        }
        _total_time_ms:float = 182
        pixle_time = 0.7344

    class Martin2Settings(BaseModel):
        name:str = 'M2'
        VISCode:int=40 # as decimal
        image_size:tuple = (320,256)
        sync_ms:dict[str,int] = {
            'sync pulse' : 4.862,
            'sync porch' : 0.572,
            'separator' : 0.572,
        }
        sync_hz:dict[str,int] = {
            'sync pulse' : 1200,
            'sync porch' : 1500,
            'separator' : 1500,
        }
        _total_time_ms:float = 58060
        pixel_time:float = 0.2288

# This might be unnecessary for this purpose
# But it makes life a little easier. 
@lru_cache(maxsize=1)
def get_settings(mode:MODE):
    if mode==MODE.ROBOT_36:
        return SSTVSettings.Robot36Settings()
    if mode==MODE.WC_SC2_120:
        return SSTVSettings.WSC2120Settings()
    if mode==MODE.WC_SC2_180:
        return SSTVSettings.WSC2180Settings()
    if mode==MODE.MARTIN2:
        return SSTVSettings.Martin2Settings()