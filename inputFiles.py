import crepe
from scipy.io import wavfile
import numpy as np
import os
import tkinter.filedialog

def get_file():
    try:  # Load initial dir file
        CF = open('input.conf', 'r')
        initialdir = CF.read()
        # print(initialdir)
        CF.close()
    except:
        initialdir = '../'
            
    root = tkinter.Tk()
    root.withdraw()  # use to hide tkinter window
    file_exts = r"*.mp3 *.mp4 *.wav"
    fname = tkinter.filedialog.askopenfilename(parent=root, initialdir=initialdir,
                                                       title='Select audio/video file',
                                                       filetypes=(('audio', file_exts), ('all files', '*.*')))
    extension = os.path.splitext(fname)[-1]
    
    if extension != '.wav':  # Convert to .wav using ffmpeg
        print('Convert to .waw file')
        file, extension = os.path.splitext(fname)
        # Convert video into .wav file
        os.system('ffmpeg -i {file}{ext} {file}.wav -y'.format(file=file, ext=extension))
    
    rate, data = wavfile.read(os.path.splitext(fname)[0] + '.wav')  # See source
    cacheFname = os.path.splitext(fname)[0] + '_cached.npz'
    
    try:  # Save initial dir file
        CF = open('input.conf', 'w')
        CF.write(os.path.dirname(fname)) 
        CF.close()
    except:
        print ('Warning: could not save path')
        
    return rate, data, cacheFname

def get_spectrum(cacheFname, data, rate):
    try:
        # try to load the cached file
        npz_conf = np.load(cacheFname)
        time = npz_conf['time']
        frequency = npz_conf['frequency']
        confidence = npz_conf['confidence']
        activation = npz_conf['activation']
        print('Loaded file from cache')
        
    except:
        # use crepe neural network for frequency anlysis https://pypi.org/project/crepe/
        time, frequency, confidence, activation = crepe.predict(data, rate, viterbi=True, step_size=2)
        
        # Save cache file
        np.savez(cacheFname, time=time, frequency=frequency, confidence=confidence, activation=activation)
        print('Saved cache file')
        
    return time, frequency
