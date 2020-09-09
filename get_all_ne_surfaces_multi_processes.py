'''
  Function:
    Get all entity surface of one entity types
  Input:
    CORD-NER-ner.json file
    label file
  Output:
    report file: number of surfaces for each entity type.
    entity_type_file: dictionary of all surfaces.
    
'''
# Import Libs
import argparse
import json
import re

# Import modules

# Constants

# Functions
def update_count_dict(dict_a,dict_b):
    res = {}
    for k in dict_a.keys():
        res[k] = dict_a[k] | dict_b[k]
    return res

def process_sent(sent,count_dict):
    entities = sent['entities']
    for entity in entities:
        text = entity['text']
        ent_type = entity['type']
        count_dict[ent_type].add(text)
    return count_dict

def process_doc(n,count_dict):
    tmp_dict = count_dict
    doc_sents = n['sents']
    for sent in doc_sents:
        sent_ent = process_sent(sent,tmp_dict)
        count_dict = update_count_dict(sent_ent,count_dict)
    
    return count_dict

def print_report_file(input_file, count_dict):
    fout = open(input_file,'w',encoding='utf-8')
    for key in count_dict.keys():
        tmp = key + '\t' + str(len(count_dict[key])) + '\n'
        fout.write(tmp)
    fout.close()

def print_dict(folder,count_dict):
    for key in count_dict:
        filename = folder + '/' + key + '.surface'
        fout = open(filename,mode='w',encoding='utf8')
        surfaces = count_dict[key]
        for surface in surfaces:
            fout.write(surface+'\n')
        fout.close()

def process(json_file,labels_file,report_folder):
    label_list = readLabel(labels_file)
    count_dict = dict()
    for label in label_list:
        count_dict[label] = set()
    
    print(count_dict)
    tmp_dict = count_dict
    i = 0
    with open(json_file,'r',encoding='utf-8') as ner:
        for ner_line in ner:
            i = i + 1
            n = json.loads(ner_line)
            doc_ent = process_doc(n,tmp_dict)
            count_dict = update_count_dict(doc_ent,count_dict)
            if (i%100)==0: 
                print('Processed {} lines'.format(i))

    print_report_file(report_folder+'report.out',count_dict)
    print_dict(report_folder,count_dict)

def readLabel(label_file):
    tmp_list = open(label_file,'r',encoding='utf-8').read().split('\n')
    tmp_list = [label.strip() for label in tmp_list]
    label_list = []
    for label in tmp_list:
        if label != '':
            tmp = re.sub('[BLIOU]\-','',label)
            label_list.append(tmp)
    return label_list

def main():
    parser = argparse.ArgumentParser(description='Get all entity surfaces of one entity type')
    parser.add_argument('--json',type=str, metavar='', required=True, help='path to the json file')
    parser.add_argument('--labels',type=str, metavar='', required=True, help='path to the label list file')
    parser.add_argument('--report',type=str, metavar='', required=True, help='path to the report folder')

    args = parser.parse_args()
    json_file = args.json
    labels_file = args.labels
    report_folder = args.report

    process(json_file,labels_file,report_folder)

if __name__ == '__main__':
    main()
