'''
  Function:
    Add new labels to Spacy pretrain ner model
  Input:
    spacy model (str): name of spacy models to update
  Output:
    new spacy model 
'''
# Import Libs
import scispacy
import spacy
import argparse
import re

# Import modules

# Constants

def readLabel(label_file):
    tmp_list = open(label_file,'r',encoding='utf-8').read().split('\n')
    tmp_list = [label.strip() for label in tmp_list]
    label_list = []
    for label in tmp_list:
        if label != '':
            tmp = re.sub('[BLIOU]\-','',label)
            label_list.append(tmp)
    return label_list

def process(model,labels_file,output_path):
  label_list = readLabel(labels_file)
  nlp = spacy.load(model)
  ner = nlp.get_pipe('ner')
  for label in label_list:
    ner.add_label(label)
  nlp.to_disk(output_path)


def main():
  parser = argparse.ArgumentParser(description='Add new ner label into a spacy model')
  parser.add_argument('--model',type=str, metavar='', required=True, help='Name of the spacy model')
  parser.add_argument('--labels',type=str, metavar='', required=True, help='path to the label list file')
  parser.add_argument('--output',type=str, metavar='', required=True, help='Path of the output model')

  args = parser.parse_args()
  model = args.model
  labels_file = args.labels
  output_path = args.output

  process(model,labels_file,output_path)

if __name__ == '__main__':
    main()
