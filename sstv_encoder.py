from typing import AnyStr
from bin.lib.modes import Robot36, WraaseSC2_120
from bin.lib.sstv.sutils import MODE
from bin.utils import AudioGenerator as ag
from bin.utils import ImageAsArray
from bin.lib.sstv import PseudoImage
import os

# TODO:
# Create a encoder manager to get the proper encoder.
# Add other encoders 

def main() -> None:
    """
    Main entrypoint. 
    Loads all images in root/images folder
    Creates encoded audio files of that image.
    Makes a pseudo solved image. (filter)
    Saves the audio and image to separate folders.
    """
    cwd = os.getcwd()
    images_dir = os.path.join(cwd,'images')
    all_images:list[AnyStr] = []
    
    print(" ")
    print("---------- loading images ----------")
    for root,dirs,files in os.walk(images_dir):
        for file in files:
            all_images.append(os.path.join(root,file))

    # This will be taken away once a encoder manager is done.
    # ----------------------------------
    mode = MODE.WC_SC2_120

    for image in all_images:
        image_array = ImageAsArray.to_array(str(image), mode)
        
        name = str(image).rsplit('/',1)[1].rsplit('.',1)[0]

        # Switch to encoder manager
        if mode == MODE.ROBOT_36:
            r36 = Robot36(image_array)
            hertz, duration = r36.encode()
        
        if mode == MODE.WC_SC2_120:
            wsc2120 = WraaseSC2_120(image_array)
            hertz, duration = wsc2120.encode()
     # ----------------------------------
        print(" ")

        os.makedirs('audio', exist_ok=True)
        audio_dir = os.path.join(cwd,'audio')

        # There has to be a simpler way of doing this...
        save_loc = f"{audio_dir}/{name}_{mode.value}.wav"
        ag.create_audio(save_loc,hertz,duration,22500.0)

        # This has to be done last!
        # The image is pulled from memory.
        # Doing it before audio data would break the audio. 
        pseudo_image = PseudoImage(f"{name}",image_array)
        pseudo_image.fake_image(mode)
        
        print(" ")
    print('---------- Done ----------')

if __name__ == '__main__':
    main()