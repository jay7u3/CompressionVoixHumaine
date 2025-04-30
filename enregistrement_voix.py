import sounddevice as sd
from scipy.io.wavfile import write

# Paramètres d'enregistrement
samplerate = 44100
duration = 60
filename = "enregistrement.wav"  # Nom du fichier de sortie

print("Enregistrement en cours...")
audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
sd.wait()
print("Enregistrement terminé.")

# Sauvegarde au format .wav
write(filename, samplerate, audio_data)
print(f"Fichier enregistré : {filename}")
