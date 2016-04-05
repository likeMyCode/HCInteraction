import matplotlib.pyplot as plt
import glob
import csv

MARKERS_LIST = ['o', 'v', 'D', 's', 'd']
COLORS_LIST = ['b', 'g', 'r', 'k', 'm']
FILES_LIST = ['rsel.csv', 'cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv']
HEURISTICS_LIST = ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']


def str_to_float(string):
	try:
		string = float(string)
	except ValueError:
		pass
	return string




def read_file(filename):
	arr = []
	with open(filename, newline='') as csvfile:
		handler = csv.reader(csvfile, delimiter=',')
		for row in handler:
			arr.append(row)	
	return arr	




def prepare_array(arr):
	new_arr = []
	for row in arr:
		temp = []
		for cell in row:
			temp.append(str_to_float(cell))
		new_arr.append(temp)
	return new_arr




def left_plot(arr, ax1, marker, color, heuristic):
	x, y = [], []
	xScaleFactor, yScaleFactor = 1000, 100

	for row in arr[1:]:
		x.append(row[1] / xScaleFactor)
		y.append((sum(row[2:]) / float(len(row[2:]))) * yScaleFactor)

	ax1.plot(x, y, c=color, marker=marker, label=heuristic, markevery=25)




def left_plot_info(ax1, ax2):
	ax1.set_xlabel('Rozegranych gier (x1000)')
	ax1.set_ylabel('Odsetek wygranych gier [%]')
	ax1.set_xlim([0,500000 / 1000])
	ax1.set_ylim([60, 100])
	ax1.legend(loc=4, fontsize='medium')
	ax1.grid() 

	ax2.set_xlabel('Pokolenie')
	ax2.set_xlim([0, 500000 / 1000])
	ax2.set_ylim([60, 100])
	ax2.set_xticks([0,100,200,300,400,500])
	ax2.set_xticklabels(['0','40','80','120','160','200']);
	



def right_plot(arr, i, ax4):
	y1 = []
	for cell in arr[-1][2:]:
		y1.append(cell * 100)

	y2 = (sum(arr[-1][2:]) / float(len(arr[-1][2:]))) * 100 
	ax4.scatter(i+1, y2, s=30)
	return y1




def right_plot_info(ax3, ax4, data):
	ax3.boxplot(data, notch=True)
	ax3.set_yticks([60,65,70,75,80,85,90,95,100])
	ax3.set_ylim([60,100])
	ax3.set_xticks([1,2,3,4,5])
	ax3.set_xticklabels(HEURISTICS_LIST, rotation=20, fontsize=11);
	ax3.yaxis.tick_right()
	ax3.grid()

	ax4.set_ylim([60,100])
	ax4.set_xticklabels(HEURISTICS_LIST, rotation=20, fontsize=11)
	ax4.set_yticklabels([])




def main():
	fig = plt.figure('Wykresik na piąteczkę')
	ax1 = plt.subplot(1, 2, 1)
	ax2 = ax1.twiny()
	ax3 = plt.subplot(1, 2, 2)
	ax4 = ax3.twinx()
	data = []
	
	
	#for file_name in glob.glob('*.csv'):       # NIE KORZYSTAM Z glob.glob, PONIEWAŻ WCZYTUJE ON PLIKI W MNIEJ WYGODNEJ KOLEJNOŚCI, 
						    # PRZEZ CO TRUDNIEJ DOBRAĆ, ŻEBY KOLORY WYKRESÓW BYŁY TAKIE JAK W TREŚCI

	for i in range(len(FILES_LIST)):
		left_plot(prepare_array(read_file(FILES_LIST[i])), ax1, MARKERS_LIST[i], COLORS_LIST[i], HEURISTICS_LIST[i])
	left_plot_info(ax1, ax2)

	
	for i in range(len(FILES_LIST)):
		data.append(right_plot(prepare_array(read_file(FILES_LIST[i])), i, ax4 ))
	right_plot_info(ax3, ax4, data)
	
	#plt.savefig('na5.pdf')	
	plt.show()
	

if __name__ == '__main__':
	main()
	
