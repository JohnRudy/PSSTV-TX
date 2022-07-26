from typing import Tuple
from bin.lib.sstv import SSTV, MODE
from numpy import ndarray
from tqdm import trange
from bin.settings import get_settings
from bin.lib.sstv.encoder_base import BaseEncoder

settings = get_settings(MODE.ROBOT_36)

class Robot36(BaseEncoder):
    def __init__(self, image: ndarray) -> None:
        super().__init__(image)

    def add_to_data(self,new_hertz:list[float], new_dur:list[float] ) -> None:
        for i in new_hertz:
            self.hertz.append(i)
        for j in new_dur:
            self.duration.append(j)

    # TODO:
    # Check the header and vis code for this. 
    # Currently they seem to be off. 
    # The sync and porch values might be wrong as well.
    def encode(self) -> Tuple:
        """
        Encoding to Robot36 standard.
        Returns a tuple (hertz, ms)
        """
        print("----- Beginning turning image to audio data -----")

        # header and vis
        self.hertz, self.duration = SSTV.initial()
        vis_code = SSTV.vis_code(settings.VISCode)
        v_hertz, v_dur = SSTV.vis_to_hertz(vis_code)
        self.add_to_data(v_hertz, v_dur)
        
        self.add_to_data([1300],[30]) # Parity
        self.add_to_data([1200],[30]) # vis stop
        
        for row in trange(239):
            y:list[float] = []
            ry:list[float] = []
            by:list[float] = []

            for column in range(319):
                yryby = SSTV.to_YRyBy(self.image[row,column])
                y.append(yryby[0])
                ry.append(yryby[1])
                by.append(yryby[2])
            
            # Sync    
            self.add_to_data(
                [settings.sync_hz['sync pulse']], 
                [settings.sync_ms['sync pulse']]
            )
            # Porch
            self.add_to_data(
                [settings.sync_hz['sync porch']], 
                [settings.sync_ms['sync porch']]
            ) 
            
            # Y values
            for value in y:
                self.hertz.append(SSTV.float_to_hertz(value))
                self.duration.append(settings.y_pixel_ms)      

            # Separator
            if row % 2 == 0:
                self.add_to_data(
                    [settings.sync_hz['even separator']], 
                    [settings.sync_ms['even separator']]
                )
                # Porch
                self.add_to_data(
                    [settings.sync_hz['porch']], 
                    [settings.sync_ms['porch']]
                ) 
                
            if row % 2 == 1:
                self.add_to_data(
                    [settings.sync_hz['odd separator']], 
                    [settings.sync_ms['odd separator']]
                )
                    # Porch
                self.add_to_data(
                    [settings.sync_hz['porch']], 
                    [settings.sync_ms['porch']]
                )
                

            # RyBy values 
            for value in range(len(ry)):
                if row % 2 == 0:
                    self.hertz.append(SSTV.float_to_hertz(ry[value]))
                    self.duration.append(settings.rb_pixel_ms)
          
                if row % 2 == 1:
                    self.hertz.append(SSTV.float_to_hertz(by[value]))
                    self.duration.append(settings.rb_pixel_ms)

        return self.hertz, self.duration

if __name__ == "__main__":
    exit()