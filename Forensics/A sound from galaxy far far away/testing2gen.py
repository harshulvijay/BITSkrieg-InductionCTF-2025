import numpy as np
import wave
from collections import Counter

def generate_tone(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a sine wave tone for given frequency and duration."""
    frames = int(duration * sample_rate)
    t = np.linspace(0, duration, frames)
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave_data

def generate_silence(duration, sample_rate=44100):
    """Generate silence for given duration."""
    frames = int(duration * sample_rate)
    return np.zeros(frames)

def create_sequential_audio_file(frequencies, filename="sequential_tones.wav"):
    # Define parameters
    sample_rate = 44100
    note_duration = 0.5  # 0.5 second per note
    gap_duration = 0.5   # 0.5 second gap between notes
    
    print(f"Creating audio with {len(frequencies)} notes...")
    print(f"Frequency sequence: {frequencies}")
    
    # Count frequency occurrences
    frequency_counts = Counter(frequencies)
    
    # Print frequency statistics
    print(f"\nFrequency occurrence statistics:")
    print(f"{'Frequency (Hz)':<15} {'Occurrences':<12}")
    print("-" * 30)
    for freq in sorted(frequency_counts.keys()):
        print(f"{freq:<15} {frequency_counts[freq]:<12}")
    
    # Generate audio data
    print(f"\nGenerating audio...")
    audio_data = []
    
    for i, frequency in enumerate(frequencies):
        print(f"Processing note {i+1}/{len(frequencies)}: {frequency} Hz")
        
        # Generate tone
        tone = generate_tone(frequency, note_duration, sample_rate)
        audio_data.extend(tone)
        
        # Add gap (except after the last note)
        if i < len(frequencies) - 1:
            silence = generate_silence(gap_duration, sample_rate)
            audio_data.extend(silence)
    
    # Convert to numpy array and normalize
    audio_data = np.array(audio_data)
    
    # Convert to 16-bit integers
    audio_data_int = np.int16(audio_data * 32767)
    
    # Save as WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data_int.tobytes())
    
    total_duration = (len(frequencies) * note_duration) + ((len(frequencies) - 1) * gap_duration)
    print(f"\nAudio file '{filename}' created successfully!")
    print(f"Total duration: {total_duration:.1f} seconds ({total_duration/60:.2f} minutes)")
    print(f"File contains {len(frequencies)} notes in exact order")
    
    # Show sequence details
    print(f"\nSequence details:")
    unique_freqs = len(set(frequencies))
    print(f"Unique frequencies used: {unique_freqs}")
    print(f"Most common frequency: {frequency_counts.most_common(1)[0][0]} Hz ({frequency_counts.most_common(1)[0][1]} times)")
    
    return filename

if __name__ == "__main__":
    # Your specified frequency sequence
    frequency_sequence = [660, 560, 520, 620, 200, 620, 220, 640, 200, 340, 
                         600, 200, 220, 260, 340, 220, 380, 200, 460, 660, 420]
    
    create_sequential_audio_file(frequency_sequence, "sequential_frequency_audio.wav")