import numpy as np
from scipy.io import wavfile

def extract_frequencies(wav_file):
    # Read wav file
    sample_rate, data = wavfile.read(wav_file)

    # If stereo, take one channel
    if len(data.shape) > 1:
        data = data[:, 0]

    # Parameters
    N = len(data)
    window_size = sample_rate // 10   # 0.1 sec windows

    freq_list = []
    prev_freq = None

    for i in range(0, N, window_size):
        segment = data[i:i+window_size]
        if len(segment) == 0:
            continue

        # FFT on segment
        seg_fft = np.fft.fft(segment)
        seg_freqs = np.fft.fftfreq(len(segment), 1/sample_rate)
        seg_magnitudes = np.abs(seg_fft[:len(segment)//2])

        if len(seg_magnitudes) > 0:
            dominant_idx = np.argmax(seg_magnitudes)
            dominant_freq = round(abs(seg_freqs[dominant_idx]))

            # Skip 0 and avoid consecutive repeats
            if dominant_freq != 0 and dominant_freq != prev_freq:
                freq_list.append(dominant_freq)
                prev_freq = dominant_freq

    return freq_list


# Example usage:
wav_file = "FLAGAUDIO.wav"
freqs_in_order = extract_frequencies(wav_file)
print(freqs_in_order)
