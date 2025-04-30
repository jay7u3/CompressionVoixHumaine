import pickle
import wave
import numpy as np

class Noeud:
    def __init__(self, symbole=None):
        self.symbole = symbole
        self.gauche = None
        self.droite = None

def reconstruire_arbre(codebook):
    racine = Noeud()
    for symbole, code in codebook.items():
        noeud = racine
        for bit in code:
            if bit == '0':
                if noeud.gauche is None:
                    noeud.gauche = Noeud()
                noeud = noeud.gauche
            else:
                if noeud.droite is None:
                    noeud.droite = Noeud()
                noeud = noeud.droite
        noeud.symbole = symbole
    return racine

def bytes_to_bits(data_bytes):
    return ''.join(f'{byte:08b}' for byte in data_bytes)

def decoder_bits(bits, arbre):
    signal = []
    noeud = arbre
    for bit in bits:
        noeud = noeud.gauche if bit == '0' else noeud.droite
        if noeud.symbole is not None:
            signal.append(noeud.symbole)
            noeud = arbre
    return signal

def decompression_huffman(fichier_huff, fichier_table, fichier_wav_sortie):
    # Charger la table et le framerate
    with open(fichier_table, 'rb') as f:
        data = pickle.load(f)
        codebook = data["codebook"]
        framerate = data["framerate"]

    arbre = reconstruire_arbre(codebook)

    # Charger les données compressées
    with open(fichier_huff, 'rb') as f:
        donnees_compressees = f.read()

    bits = bytes_to_bits(donnees_compressees)
    signal = decoder_bits(bits, arbre)
    signal_array = np.array(signal, dtype=np.int16)

    # Sauvegarder le WAV décompressé avec le bon framerate
    with wave.open(fichier_wav_sortie, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16 bits
        wf.setframerate(framerate)
        wf.writeframes(signal_array.tobytes())

    return fichier_wav_sortie
