import matplotlib.pyplot as plt
import glob
import csv

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


def prepare_plot(arr, heuristic):
	x, y = [], []
	for row in arr[1:]:
		x.append(row[1])
		y.append(sum(row[2:]) / float(len(row[2:])))
	plt.plot(x, y, label=heuristic)


def draw_plot():
	plt.xlabel('Rozegranych gier')
	plt.ylabel('Odsetek wygranych gier')
	plt.legend(loc=4)
	plt.xlim([0,500000])
	plt.show()


def main():
	for i in range(len(FILES_LIST)):
		prepare_plot(prepare_array(read_file(FILES_LIST[i])), HEURISTICS_LIST[i])
	draw_plot()


if __name__ == '__main__':
	main()
