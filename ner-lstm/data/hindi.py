from wxconv import WXC
import random

wxc = WXC(order='utf2wx')

def tag_extract(string):
	tag_list = ['PERSON', 'ORGANIZATION', 'LOCATION', 'ENTERTAINMENT', 'FACILITIES', 'ARTIFACT', 'LIVTHINGS', 'LOCOMOTIVE', 'PLANTS', 'MATERIALS', 'DISEASE', 'O']
	for tag in tag_list:
		if tag in string:
			return tag

def write_conll(sentences, output):
	f = open(output, 'w')
	for sentence in sentences:
		for word in sentence:
			f.write(word + '\n')
		f.write('\n')
	f.close()

sentences = []
sentence = []
ner_tag = 'O'

for line in open('hindi-annotated-ssf-Form.txt'):
	print(line)
	if line.startswith('<Sentence'):
		sentence = []
	elif line.startswith('</Sentence'):
		sentences.append(sentence)
		print(sentences)
	elif line.startswith('<ENAMEX'):
		ner_tag = tag_extract(line)
		print(ner_tag)
	else:
		print("bump")
		line = line.split()
		if len(line) == 0:
			continue
		try:
			index = float(line[0])
			if index != int(index):
				sentence.append(wxc.convert(line[1]) + ' ' + line[2] + ' ' + '.' + ' ' + ner_tag)
		except ValueError:
			pass
		ner_tag = 'O'
random.shuffle(sentences)
train = 0.8 * len(sentences) // 1
test_a = 0.15 * len(sentences) // 1
test_b = len(sentences) - train - test_a
train, test_a, test_b = sentences[0:train], sentences[train:train + test_a], sentences[train + test_a:]
write_conll(train, 'hin.train')
write_conll(test_a, 'hin.test_a')
write_conll(test_b, 'hin.test_b')