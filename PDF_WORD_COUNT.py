import PyPDF2
import sys

"""This short script can extract the words count of a PDF
and it's really easy to use.
1. open terminal
2. type python3 and then space
3.drag this file to terminal
4.drag PDF you want to use
5.enter the word you want to count
6. Press Enter

"""


def get_txt(file_name):
	""" convert pdf to txt file"""
	with open(file_name, 'rb') as f:
		pdfReader = PyPDF2.PdfFileReader(f)
		total_pages = pdfReader.numPages

		all_txt = ''
		for i in range(total_pages):
			all_txt += pdfReader.getPage(i).extractText()
	return all_txt.lower()


def get_count(txt, word):
	""" get word count of a file, can be imporved by re Lib"""
	return len(txt.split(word.lower())) - 1


def process_file(file, word_list):
	"""get word count for current file"""

	result_dict = {}
	result_dict[file] = []
	s = get_txt(file)
	if type(word_list) == type([]): 
		for word in word_list:
			result_dict[file].append(str(get_count(s, word)))
	else:
		result_dict[file].append(str(get_count(s, word_list)))
	return result_dict

if __name__ == "__main__":
	print(process_file(sys.argv[1], sys.argv[2]))
