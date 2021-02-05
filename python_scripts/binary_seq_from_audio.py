import os
import numpy as np
from scipy.fft import fft, ifft, rfft, irfft
from scipy.io import wavfile
from scipy.signal import butter, lfilter


samplerate, data = wavfile.read('../Other/audio_data/DKITCHEN/ch01.wav')



def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y




def sound_to_binary(data,samplerate,write_file):

    frames = 3000000
    r = samplerate
    m = 30
    t = 5*60
    l = len(data)/t
    d = int(r*(l/frames))
    bfilter = []
    counter = 0

    #print(d)
    S = []
    counter = 0
    for i in range(0, frames-1):
        hanning = []
        f_i = data[(i*d):(i+1)*d]
        if len(f_i) == 0:
            continue
        print(f_i)
        S_i = np.real(fft(f_i))
        hanning = np.hanning(len(S_i))
        S_i = S_i * hanning

        b = (max(S_i) - min(S_i))/m
        S.append([])
        fs = max(S_i) - min(S_i)
        for j in range(1, m-1): 
            S[counter].append(butter_bandpass_filter(S_i, b*j, b*(j+1), fs))

        counter+=1

    for i in range(1,len(S)-1):
        for j in range(0,len(S[i])-2):
            sum_ = np.sum(S[i][j]) - np.sum(S[i][j+1]) - np.sum(S[i-1][j]) - np.sum(S[i-1][j+1])
            if sum_ > 0:
                bit = '1'
            else:
                bit = '0'
            with open(write_file, "a") as f:
                f.write(bit)


def main():
    path = '../Other/audio_data'
    write_file = "../nist_test_results/audio_bits_before.txt"

    if os.path.exists(write_file):
        os.remove(write_file)

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if "ch01.wav" in name:
                sound_file = f"{root}/{name}"
                samplerate,data = wavfile.read(sound_file)
                sound_to_binary(data,samplerate,write_file)

if __name__ == "__main__":
    main()