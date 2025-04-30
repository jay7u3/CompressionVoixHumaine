import wave
import contextlib
import os
import numpy as np
from scipy.signal import butter, lfilter

LOWCUT = 100     # Fréquence de coupure basse (Hz)
HIGHCUT = 3400.0 # Fréquence de coupure haute (Hz)
ORDER = 5        # Ordre du filtre
SEUIL = 100      # Seuil pour la détection de voix (amplitude)
FACTEUR = 2      # Facteur de décimation

def filtre_passe_bande(signal, fs, lowcut=LOWCUT, highcut=HIGHCUT, order=ORDER):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal)

def detection_voix(signal, seuil):
    signal_filtré = np.zeros_like(signal)
    signal_filtré[np.abs(signal) > seuil] = signal[np.abs(signal) > seuil]
    return signal_filtré

def decimation(signal, facteur=FACTEUR):
    return signal[::facteur]

def ecrire_wav(fichier_sortie, signal, framerate):
    signal = signal.astype(np.int16)
    with wave.open(fichier_sortie, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2) 
        wf.setframerate(framerate)
        wf.writeframes(signal.tobytes())

def simplifier_wav(fichier_wav):
    if not os.path.exists(fichier_wav):
        return None, None

    with contextlib.closing(wave.open(fichier_wav, 'rb')) as wav:
        nchannels = wav.getnchannels()
        framerate = wav.getframerate()
        nframes = wav.getnframes()
        sampwidth = wav.getsampwidth()

        signal = wav.readframes(nframes)
        audio = np.frombuffer(signal, dtype=np.int16)

        if nchannels == 2:
            audio = audio[::2]  # Mono

    # Traitement du signal
    audio_filtre = filtre_passe_bande(audio, framerate)
    audio_voix = detection_voix(audio_filtre, seuil=SEUIL)
    audio_deci = decimation(audio_voix, facteur=FACTEUR)
    framerate_deci = framerate // FACTEUR

    # Fichier de sortie
    fichier_modifie = os.path.splitext(fichier_wav)[0] + "_modifie.wav"
    ecrire_wav(fichier_modifie, audio_deci, framerate_deci)

    return fichier_modifie
