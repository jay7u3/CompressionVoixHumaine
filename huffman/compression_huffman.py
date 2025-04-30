import wave
import os
import heapq
import pickle
import numpy as np
from collections import Counter

class Noeud:
    def __init__(self, symbole=None, freq=0):
        self.symbole = symbole
        self.freq = freq
        self.gauche = None
        self.droite = None

    def __lt__(self, autre):
        return self.freq < autre.freq

def construire_arbre_huffman(frequences):
    heap = [Noeud(symbole, freq) for symbole, freq in frequences.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        gauche = heapq.heappop(heap)
        droite = heapq.heappop(heap)
        parent = Noeud(None, gauche.freq + droite.freq)
        parent.gauche = gauche
        parent.droite = droite
        heapq.heappush(heap, parent)

    return heap[0]

def generer_codes(arbre, prefixe="", codebook=None):
    if codebook is None:
        codebook = {}
    if arbre.symbole is not None:
        codebook[arbre.symbole] = prefixe
    else:
        generer_codes(arbre.gauche, prefixe + "0", codebook)
        generer_codes(arbre.droite, prefixe + "1", codebook)
    return codebook

def encoder_signal(signal, codebook):
    return ''.join(codebook[val] for val in signal)

def bits_to_bytes(bits):
    while len(bits) % 8 != 0:
        bits += '0'
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

def compresser_wav(fichier_wav, fichier_huff, fichier_table):
    with wave.open(fichier_wav, 'rb') as wav:
        nchannels = wav.getnchannels()
        assert nchannels == 1, "Le fichier doit être mono."
        sampwidth = wav.getsampwidth()
        assert sampwidth == 2, "Le fichier doit être 16 bits."
        framerate = wav.getframerate()
        nframes = wav.getnframes()
        data = wav.readframes(nframes)
        signal = np.frombuffer(data, dtype=np.int16)

    frequences = Counter(signal)
    arbre = construire_arbre_huffman(frequences)
    codebook = generer_codes(arbre)
    bits = encoder_signal(signal, codebook)
    donnees_compressees = bits_to_bytes(bits)

    with open(fichier_huff, 'wb') as f:
        f.write(donnees_compressees)

    with open(fichier_table, 'wb') as f:
        pickle.dump({"codebook": codebook, "framerate": framerate}, f)

    taille_compressee = os.path.getsize(fichier_huff)

    return fichier_huff, fichier_table, taille_compressee
