import os
from simplification import simplifier_wav
from huffman.compression_huffman import compresser_wav
from huffman.decompression_huffman import decompression_huffman

def menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Simplifier un fichier WAV")
    print("2. Compresser un fichier WAV avec Huffman")
    print("3. Simplifier + Compresser un fichier WAV")
    print("4. Décompresser un fichier Huffman")
    print("5. Quitter")

def get_taille(filename):
    return os.path.getsize(filename) if os.path.exists(filename) else 0

def main():
    while True:
        menu()
        choix = input("Choix : ")

        if choix == '1':
            fichier = input("Nom du fichier WAV à simplifier : ").strip()
            if not os.path.exists(fichier):
                print("Fichier introuvable.")
                continue
            sortie = simplifier_wav(fichier)
            print(f"\nSimplification terminée : {sortie}")

        elif choix == '2':
            fichier = input("Nom du fichier WAV à compresser : ").strip()
            if not os.path.exists(fichier):
                print("Fichier introuvable.")
                continue
            huff_out = os.path.splitext(fichier)[0] + ".huff"
            pkl_out = os.path.splitext(fichier)[0] + ".pkl"
            _, _, taille_compressee = compresser_wav(fichier, huff_out, pkl_out)
            taille_original = os.path.getsize(fichier)
            taux = 100 * (1 - taille_compressee / taille_original)
            print(f"Taux de compression (Huffman) : {taux:.2f}%")

        elif choix == '3':
            fichier = input("Nom du fichier WAV à simplifier puis compresser : ").strip()
            if not os.path.exists(fichier):
                print("Fichier introuvable.")
                continue
            fichier_simplifie = simplifier_wav(fichier)
            huff_out = os.path.splitext(fichier_simplifie)[0] + ".huff"
            pkl_out = os.path.splitext(fichier_simplifie)[0] + ".pkl"
            _, _, taille_compressee = compresser_wav(fichier_simplifie, huff_out, pkl_out)
            taille_original = os.path.getsize(fichier)
            taux = 100 * (1 - taille_compressee / taille_original)
            print(f"Taux de compression (simplification + Huffman) : {taux:.2f}%")

        elif choix == '4':
            huff_file = input("Nom du fichier .huff à décompresser : ").strip()
            table_file = input("Nom du fichier .pkl (table Huffman) : ").strip()
            if not os.path.exists(huff_file) or not os.path.exists(table_file):
                print("Fichier(s) manquant(s).")
                continue
            sortie = os.path.splitext(huff_file)[0] + "_reconstruit.wav"
            decompression_huffman(huff_file, table_file, sortie)
            print(f"Fichier décompressé : {sortie}")

        elif choix == '5':
            print("Fin du programme.")
            break

        else:
            print("Choix invalide. Réessaye.")

if __name__ == "__main__":
    main()
