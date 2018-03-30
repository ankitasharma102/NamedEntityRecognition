from wxconv import WXC
import random

wxc = WXC(order='utf2wx')

def tag_extract(string):
	tag_list = ['PERSON', 'ORGANIZATION', 'LOCATION', 'ENTERTAINMENT', 'FACILITIES', 'ARTIFACT', 'LIVTHINGS', 'LOCOMOTIVE', 'PLANTS', 'MATERIALS', 'DISEASE', 'O']
	for tag in tag_list:
		if tag in string:
			if tag=='PERSON':
				return 'I-PER'
			elif tag=='ORGANIZATION':
				return 'I-ORG'
			elif tag=='LOCATION':
				return 'I-LOC'
			elif tag=='O':
				return tag
			else :
				return 'I-MISC'

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
	if line.startswith('<Sentence'):
		sentence = []
	elif line.startswith('</Sentence'):
		sentences.append(sentence)
	elif line.startswith('<ENAMEX'):
		ner_tag = tag_extract(line)
		print("tag"+ner_tag)
	else:
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
train = int(0.6 * len(sentences)) // 1
test = int(0.2 * len(sentences)) // 1
dev = len(sentences)
train, test, dev = sentences[0:train], sentences[train:train + test], sentences[train+test:]
write_conll(train, 'train')
write_conll(test, 'test')
write_conll(dev, 'dev')