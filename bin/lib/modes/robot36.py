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
        for row in trange(239):
            y_sl:list[float] = []
            ry_sl:list[float] = []
            by_sl:list[float] = []
            # get the luminance and chrominance value for each pixel
            for column in range(319):
                r = float(self.image[row,column][0])
                g = float(self.image[row,column][1])
                b = float(self.image[row,column][2])
                l = SSTV.to_luminance(r, g, b)
                c = SSTV.to_chrominance(r, g, b, l)
                y_sl.append(l)
                ry_sl.append(c[0])
                by_sl.append(c[1])
            # Sync    
            self.add_to_data([settings.sync_hz['sync pulse']], [settings.sync_ms['sync pulse']])
            # Porch
            self.add_to_data([settings.sync_hz['porch']], [settings.sync_ms['porch']]) 
            # y line
            y_hertz, y_dur = SSTV.scanline(y_sl, settings.y_pixel_ms )
            self.add_to_data(y_hertz, y_dur)
            # Even
            if row % 2 == 0:
                # separator
                self.add_to_data([settings.sync_hz['even separator']], [settings.sync_ms['even separator']])
                # r-y
                e_hertz, e_dur = SSTV.scanline(ry_sl, settings.rb_pixel_ms)
                self.add_to_data(e_hertz,e_dur)
            # odd
            if row % 2 == 1:
                # separator
                self.add_to_data([settings.sync_hz['odd separator']], [settings.sync_ms['odd separator']])
                # b-y
                o_hertz, o_dur = SSTV.scanline(by_sl, settings.rb_pixel_ms)
                self.add_to_data(o_hertz, o_dur)
        return self.hertz, self.duration

if __name__ == "__main__":
    exit()