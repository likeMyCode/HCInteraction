import sys
import numpy as np
import matplotlib.pyplot as plt

import scipy as sc
from scipy.io import wavfile
from scipy.signal import decimate

def check_voice(nazwa_pliku):
	fs, sygnal = wavfile.read(nazwa_pliku)

	n = len(sygnal) # liczba probek
	czas = n / fs # czas nagrania
	
	if len(sygnal.shape) > 1: # nagranie stereo, bierzemy tylko jeden kanal
		sygnal = [s[0] for s in sygnal]

	spektrum = abs(sc.fft(sygnal)) # transformata Fouriera
	
	dlugosc = len(spektrum) / 2
	
	spektrum = spektrum[0 : dlugosc] # bierzemy tylko polowe
	
	hps = spektrum # kopiujemy spektrum aby skorzystac z algorytmu HPS (Harmonic Product Spectrum)
	
	for i in range(2, 4):
		s = decimate(spektrum, i)
		hps[0:len(s)] += s
	
	# badamy tylko czestotliwosci od 50 do 500
	# czestotliwosc glosu ludziego na pewno zawiera sie w tym przedziale
	
	od = 50 * czas # indeks czestotliwosci 50
	do = 500 * czas # indeks czestotliwosci 500
	
	hps = hps[od : do]
	
	hps = list(hps)
	
	maksimum = max(hps)
	
	indeks = hps.index(maksimum)
	
	czest = (od + indeks) / czas
	
	if czest > 170:
		return False # kobieta
	else:
		return True # mezczyzna


def main():
	if len(sys.argv) < 2:
		print ("Nie podano nazwy pliku")
		sys.exit(-1)
		
	meski = check_voice(sys.argv[1])

	if meski == True:
		print("M")
	else:
		print("K")


if __name__ == "__main__":
	main()

