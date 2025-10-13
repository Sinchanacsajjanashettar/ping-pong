import wave
import struct
import math
import os

def generate_wav(filename, freq=440, duration=0.3, volume=0.5):
    """
    Generate a playable stereo 16-bit WAV file for Pygame.
    """
    framerate = 44100
    amplitude = int(32767 * volume)
    n_samples = int(duration * framerate)

    os.makedirs("sounds", exist_ok=True)
    wav_file = wave.open(filename, 'w')
    wav_file.setparams((2, 2, framerate, n_samples, 'NONE', 'not compressed'))  # stereo, 16-bit

    for i in range(n_samples):
        t = i / framerate
        sample = int(amplitude * math.sin(2 * math.pi * freq * t))
        data = struct.pack('<hh', sample, sample)  # stereo
        wav_file.writeframesraw(data)

    wav_file.close()

# Generate sounds
generate_wav("sounds/paddle_hit.wav", freq=1000, duration=0.2, volume=0.7)  # Paddle hit
generate_wav("sounds/wall_hit.wav", freq=600, duration=0.2, volume=0.7)     # Wall hit
generate_wav("sounds/score.wav", freq=400, duration=0.4, volume=0.8)        # Score

print("Playable WAV files created in 'sounds/' folder.")
