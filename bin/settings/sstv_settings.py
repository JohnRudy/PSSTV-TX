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
        _total_sync_times:float = (
            (sync_ms['even separator'] * image_size[1]) + 
            (sync_ms['porch'] * image_size[1]) +
            sync_ms['sync pulse']
        )
        y_pixel_ms:float = (_total_time_ms - _total_sync_times) / image_size[1] / 8 * 4 / image_size[0]
        rb_pixel_ms:float = (_total_time_ms - _total_sync_times) / image_size[1] / 8 * 4 / image_size[0]

    class WCSC2120Settings(BaseModel):
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
        _total_time_ms:float = 120000
        _total_sync_times:float = sync_ms['sync pulse'] * image_size[1]
        green_pixel_ms:float = (_total_time_ms - _total_sync_times) / image_size[1] / 8 * 4 / image_size[0]
        redblue_pixel_ms:float = (_total_time_ms - _total_sync_times) / image_size[1] / 8 * 2 / image_size[0]

# This might be unnecessary for this purpose
# But it makes life a little easier. 
@lru_cache(maxsize=1)
def get_settings(mode:MODE):
    if mode==MODE.ROBOT_36:
        return SSTVSettings.Robot36Settings()
    if mode==MODE.WC_SC2_120:
        return SSTVSettings.WCSC2120Settings()