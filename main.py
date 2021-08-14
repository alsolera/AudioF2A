import matplotlib.pyplot as plt
import inputFiles
import numpy as np
import scipy.signal as signal
import tkinter.simpledialog
from scipy.signal import butter, sosfilt


def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], analog=False, btype='band', output='sos')
        return sos


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        sos = butter_bandpass(lowcut, highcut, fs, order=order)
        y = sosfilt(sos, data)
        return y


def diff_peaks(data, timestep):
    
    diff = -np.diff(data)
    
    diff = butter_bandpass_filter(diff, .2, 5, 100, order=5)
    
    peaks, _ = signal.find_peaks(diff, height=None, threshold=None, distance=1.10/timestep, prominence=5, width=None)
    
#     plt.plot(diff)
#     plt.scatter(peaks,np.zeros_like(peaks))
#     plt.show()
    
    return peaks

root = tkinter.Tk()
root.withdraw()  # use to hide tkinter window
n_laps = tkinter.simpledialog.askinteger('Input', 'Timed laps', initialvalue = 9)
line_lenght = tkinter.simpledialog.askfloat('Input', 'Line lenght (m)', initialvalue=1000/(2*np.pi*n_laps))

print(line_lenght)


rate, data, cacheFname = inputFiles.get_file()
time, frequency = inputFiles.get_spectrum(cacheFname, data, rate)
timestep = time[1] - time[0]

passes_idx = diff_peaks(frequency, timestep)
passes_times = time[passes_idx]
lap_time = np.zeros(passes_idx.shape[0])

# speed calcs
for lap in range(0,passes_idx.shape[0]):
    #print(passes_times[lap])
    if lap > 0:
        lap_time[lap-1] = passes_times[lap] - passes_times[lap-1]
        speed = 3.6*line_lenght*np.pi*2/lap_time[lap-1]
        
        print('Vuelta: %i Tiempo: %.3fs Velocidad: %.3f km/h' % (lap, lap_time[lap-1], speed))

#Plot

plt.xlabel('Time')
plt.ylabel('Frequency')
 
plt.plot(time, frequency)#, 0.5, marker='.')
plt.vlines(passes_times, 0, 1000, colors='r', linestyles='dashed')
 
plt.grid(True, 'both', 'both')
plt.xticks(np.arange(min(time), max(time) + 1, 2))
for lap in range (1,passes_times.shape[0]):
    plt.text(passes_times[lap-1], 100, s=('%i' % lap))
 
plt.show(block=False)

start_lap = tkinter.simpledialog.askinteger('Input', 'Start lap')
total_time = passes_times[start_lap+n_laps-1] - passes_times[start_lap-1]

avg_speed = 3.6*line_lenght*np.pi*2*n_laps/total_time

print('Tiempo: %.2fs Velocidad: %.2f km/h' % (total_time, avg_speed))

