from typing import Tuple
import wave
import numpy as np
import time
from tqdm import tqdm, trange

class AudioGenerator:   
    @classmethod
    def _clean_before_sine(cls, hertz_data:list[float], duration_data:list[float]) -> Tuple:
        """
        Cleans the tone and durations list provided for cleaner tone creation.
        Returns a tuple (tone:list[float], duration:list[float])
        """

        clean_tone:list[float] = []
        clean_duration:list[float] = []
        
        for i in range(len(hertz_data)-1):
            if hertz_data[i] != hertz_data[i+1]:
                clean_tone.append(hertz_data[i])
                clean_duration.append(duration_data[i])
            else:
                currentDur = clean_duration[len(clean_duration)-1]
                currentDur += duration_data[i]
                clean_duration[len(clean_duration)-1] = currentDur

        return clean_tone, clean_duration


    @classmethod
    def _sinewave(cls, freq:float=440, ms:float = 500, last_phase:float = 0, sample_rate:float = 22050.0)-> Tuple:
        """
        Creates a sinewave of given frequency and duration.
        Last phase is used as phase shifting between two different hertz values to minimize clicking and artifacts.
        Returns a tuple (audio:list[float], last_phase:float)
        """

        num_samples = int(ms * (sample_rate / 1000))
        audio = []

        for i in range(num_samples):
            audio.insert(i, np.sin(2 * np.pi * freq * (i / sample_rate) + last_phase))

        last_phase = (last_phase + 2 * np.pi * freq * (num_samples / sample_rate)) % (2 * np.pi)
        return audio, last_phase


    @classmethod
    def _save_audio(cls, file_name:str, audio:list[float], sample_rate:float = 22050.0, volume:float = 0.5) -> None:
        """
        Creates a .wav file with given filename and audio data.
        """
        sa_start = time.perf_counter()
        wav_file = wave.open(file_name,'w')
        wav_file.setnchannels(1)
        wav_file.setframerate(sample_rate)
        wav_file.setsampwidth(2)
        wav_file.setcomptype("NONE","not compressed")
        
        volume:float = 32767.0 * volume
        
        values = list(np.array(audio) * volume)
        
        byte_array = bytearray(np.int16(values))
        wav_file.writeframes(byte_array)
        wav_file.close()

    @classmethod
    def create_audio(cls, file_name:str, raw_hertz_list:list, raw_duration_list:list, sample_rate:float = 22050.0) -> None:
        """
        Takes raw hertz and duration lists, cleans them, and creates a .wav file with given filename.
        """        
        hertz_data, duration_data = cls._clean_before_sine(raw_hertz_list,raw_duration_list)
        
        audio:list[float] = []
        sine_data:list[float] = []
        phase:float = 0
        
        sw_start = time.perf_counter()

        print("----- Creating audio file -----")
        for index in trange(len(hertz_data)):
            sine_data,phase = cls._sinewave(hertz_data[index],duration_data[index],phase,sample_rate)
            for index in sine_data:
                audio.append(index)

        cls._save_audio(file_name, audio, sample_rate)

if __name__ == '__main__':
    exit()