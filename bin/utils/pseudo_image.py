from numpy import ndarray
from bin.lib.sstv import MODE
from bin.settings import get_settings
from PIL import Image
import numpy as np
import os
import random

# TODO:
# Make the image be modifiable with "sliders"
# in laymans terms. Give the possibility modify the values

class PseudoImage:
    def __init__(self, name:str, image:ndarray) -> None:
        self.image:ndarray = image
        self.name = name

    def fake_image(self, mode:MODE) -> None:
        """
        Just modifies the image to be more "sstv" like without the need to actually decode the audio.
        It is horrible to look at but works. 
        """
        print(" ")
        print("--------- Creating fake decoded image ---------")

        width = get_settings(mode).image_size[0]
        height = get_settings(mode).image_size[1]

        # General quality changes
        for value in self.image:
            value *= 128 # "true color"
            value += 10 # Brightness

        # Which rows will get "messed up"
        messed_up_lines:list[tuple] = []
        amount = random.randint(1,4)
        for index in range(amount):
            start = random.randint(0,height)
            end = random.randint(start+2,start+4)
            line = (start,end)
            messed_up_lines.append(line)

        # how much gets skewed
        skewed_lines:list[tuple] = []
        amount_skewed = random.randint(1,5)
        for index in range(amount_skewed):
            start:int = random.randint(0,height)
            end:int = random.randint(start, start + 100)
            skewed_lines.append((start,end))

        # "Aberation"
        for row in range(height-1):
            for column in range(width-1):
                try:
                    self.image[row,column][2] = self.image[row,column+5 % column][2]
                    self.image[row,column][1] = self.image[row,column+4 % column][1]
                    self.image[row,column][0] = self.image[row,column+0 % column][0]
                # Too lazy figure out the exception here. 
                except Exception:
                    continue

        # Noise
        for row in range(height-1):
            for column in range(width-1):
                # Extra noise lines
                for line in messed_up_lines:
                    if row > line[0] and row < line[1]:
                        self.image[row,column][0] += random.randint(0,255)
                        self.image[row,column][1] += random.randint(0,255)
                        self.image[row,column][2] += random.randint(0,100)
                
                # mess up the first 4 rows
                if row==1 or row==2 or row==3 or row==4:
                    self.image[row,column][0] += random.randint(0,255)
                    self.image[row,column][1] += random.randint(0,255)
                    self.image[row,column][2] += random.randint(0,100)
                
                # mess up the last 4 rows
                if row==height-4 or row==height-3 or row==height-2 or row==height-1:
                    self.image[row,column][0] += random.randint(0,255)
                    self.image[row,column][1] += random.randint(0,255)
                    self.image[row,column][2] += random.randint(0,100)
                
                # General noise addition
                self.image[row,column][random.randint(0,2)] += random.randint(0,25)


        # Side color addition
        for row in range(height-1):
            for column in range(width-1):
                # More green in the left
                max = 25
                if column <= max:
                    addition = 128 * (1 - column / max) + random.randint(-10,10)
                    self.image[row,column][0] = self.image[row,int(column+addition/10)%width][0]
                    self.image[row,column][1] += addition / 10
                    self.image[row,column][2] = self.image[row,int(column+addition/10)%width][2]
                
                # red on the right
                min = width - 25
                if column >= min:
                    addition = 128 * (1 - (column-width)/(min-width))
                    self.image[row,column][0] += addition / 5
        

        #skew
        for row in range(height-1):
            for column in range(width-1):        
                for line in skewed_lines:
                    if row > line[0] and row < line[1]: 
                        if row >= line[0] and row <= line[1]:
                            amount = int((line[1] - row) / 10)
                            self.image[row,column] = self.image[row,(column + amount) % width]



        # Converting everything back to and visible image
        img = self.image.astype(np.uint8)
        img = Image.fromarray(img)
        cwd = os.getcwd()
        save_path = os.path.join(cwd,"encoded")
        os.makedirs(save_path,exist_ok=True)
        img.save(fp=f"{save_path}/{self.name}.bmp")

        return

if __name__ == '__main__':
    exit()