# Compression de la voix humaine

## Lancement
Placez votre fichier au format `.wav` dans le dossier principal.  
(Vous pouvez par exemple utiliser ma lecture du début de *L'Étranger* de Camus pour faire des tests.)

Lancez le programme avec :
python main.py

## Fonctionnement
Le fichier `.wav` est d'abord simplifié en exploitant les caractéristiques de la voix humaine :
- Filtrage passe-bande entre 100 et 3400 Hz
- Suppression des faibles amplitudes
- Décimation (réduction du nombre d’échantillons)

Ce traitement est conçu pour de la parole humaine et ne convient pas à d'autres types de sons.

Ensuite, on compresse le signal avec des arbres de Huffman, puis on peut le décompresser.  
On atteint facilement des taux de compression autour de 80 %, avec pertes.

## Fonctions du menu
1. Simplifier un fichier `.wav`  
2. Compresser avec Huffman  
3. Simplifier puis compresser  
4. Décompresser un fichier `.huff`  
5. Quitter

## Fichiers générés
- `fichier_modifie.wav` : après simplification  
- `fichier.huff` : données compressées  
- `fichier.pkl` : table Huffman + framerate  
- `fichier_reconstruit.wav` : après décompression

## Taux de compression
100 × (1 - taille_compressée / taille_originale)
