'''
  Function:
    Convert CORD_19 NER data format to CoNLL format for training NER
  Input:
    corpus_file(str): path to the corpus file.
    ner_file(str): path to ner label file
    output(str): path to the output CoNLL format NER file
  Output:
    CoNLL format training NER file
    
'''
# Import Libs
import argparse
import json
import itertools  

# Import modules

# Constants

# Functions
def process_sent(doc_sent,ner_sent):
    tokens = doc_sent['sent_tokens']
    labels = ['O']*len(tokens)
    entities_list = ner_sent['entities']
    for entity in entities_list:
        start = entity['start']
        end   = entity['end']
        en_type = entity['type']
        labels[start] = 'B-' + en_type
        for i in range(start+1,end):
            labels[i] = 'I-' + en_type
    return tokens, labels

def write_ner(tokens,labels,fout):
    for (token, label) in zip(tokens, labels):
        fout.write(token+' '+label+'\n')
    fout.write('\n')


def process_doc(d,n,fout):
    doc_sents = d['sents']
    ner_sents = n['sents']
    if len(doc_sents) != len(ner_sents):
        print('Error: Different number of sents!')
    i = 0
    for (doc_sent, ner_sent) in zip(doc_sents,ner_sents):
        tokens, labels = process_sent(doc_sent,ner_sent)
        write_ner(tokens,labels,fout)

def process(corpus_file,ner_file,output):
    fout = open(output,'w',encoding='utf-8')
    with open(corpus_file,'r',encoding='utf-8') as corpus:
        with open(ner_file,'r',encoding='utf-8') as ner:
            for ner_line,corpus_line in zip(ner,corpus):
                d = json.loads(corpus_line)
                n = json.loads(ner_line)
                process_doc(d,n,fout)

    fout.close()


def main():
    parser = argparse.ArgumentParser(description='Convert CORD_19 NER data format to CoNLL format for training NER')
    parser.add_argument('corpus_file',type=str, metavar='', required=True, help='path to the corpus file')
    parser.add_argument('ner_file',type=str, metavar='', required=True, help='path to the ner label corpus_file')
    parser.add_argument('output',type=str, metavar='', required=True, help='path to the output CoNLL format file')

    args = parser.parse_args()
    corpus_file = args.corpus_file
    ner_file = args.ner_file
    output = args.output
    process(corpus_file,ner_file,output)

if __name__ == '__main__':
    main()