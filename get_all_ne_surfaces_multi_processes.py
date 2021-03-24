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
import multiprocessing as mp
import os
import functools
# Import modules

# Constants
parser = argparse.ArgumentParser(description='Get all entity surfaces of one entity type')
parser.add_argument('--json',type=str, metavar='', required=True, help='path to the json file')
parser.add_argument('--labels',type=str, metavar='', required=True, help='path to the label list file')
parser.add_argument('--report',type=str, metavar='', required=True, help='path to the report folder')

args = parser.parse_args()
json_file = args.json
labels_file = args.labels
report_folder = args.report

def chunkify(fname,size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname,'rb') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

def readLabel(label_file):
    tmp_list = open(label_file,'r',encoding='utf-8').read().split('\n')
    tmp_list = [label.strip() for label in tmp_list]
    label_list = []
    for label in tmp_list:
        if label != '':
            tmp = re.sub('[BLIOU]\-','',label)
            label_list.append(tmp)
    return label_list

label_list = readLabel(labels_file)
zero_dict = dict()
for label in label_list:
    zero_dict[label] = set()

# Functions
def update_count_dict(dict_b,dict_a=zero_dict):
    for k in dict_a.keys():
        dict_a[k] = dict_a[k] | dict_b[k]
    return dict_a

def process_sent(sent,count_dict):
    entities = sent['entities']
    for entity in entities:
        text = entity['text']
        ent_type = entity['type']
        count_dict[ent_type].add(text)
    return count_dict

def join_count_dict(ents):
    if len(ents) == 1:
        return ents[0]
    elif len(ents) == 2:
        return update_count_dict(ents[0],ents[1])
    elif len(ents) > 64:
        res = []
        arg = [ents[n:n+64] for n in range(0, len(ents), 64)]
        for element in arg:
            res.append(join_count_dict(element))
        return join_count_dict(res)
    else:
        arg = [ents[n:n+2] for n in range(0, len(ents), 2)]
        with mp.Pool(64) as pool:
            res = pool.starmap(update_count_dict,arg)
            print(len(res))
        return join_count_dict(res)

def join_count_dict2(ents):
    res = zero_dict
    for ent in ents:
        res = update_count_dict(res,ent)
    return res

def process_multi_line(doc_sents): 
    count_dict = zero_dict
    tmp_dict = zero_dict
    for sent in doc_sents:
        sent_ent = process_sent(sent,tmp_dict)
        count_dict = update_count_dict(count_dict,sent_ent)
    return count_dict

def process_doc(doc_sents):
    count_dict = zero_dict
    tmp_dict = zero_dict
    res = []
    if len(doc_sents) > 100000:
        arg = [doc_sents[n:n+256] for n in range(0, len(doc_sents), 256)]
        with mp.Pool(64) as pool:
            res = pool.map(process_multi_line,arg)
        count_dict = join_count_dict2(res)
    else: 
        count_dict = process_multi_line(doc_sents)
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

def process_multi_doc(sents):
    res = []
    for sent in sents:
        n = json.loads(sent)
        res.append(process_doc(n))
    return join_count_dict(res)

def process_wrapper(input_file, chunkStart, chunkSize):
    res = []
    count_dict = zero_dict
    with open(input_file,'r') as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            # print(line)
            n = json.loads(line)
            res.append(process_doc(n['sents']))
        count_dict = join_count_dict2(res)
    return count_dict

def process(json_file,labels_file,report_folder):
    tmp_dict = zero_dict
    i = 0
    doc_ents= []
    tmp = [(json_file,chuckStart,chunkSize) for chuckStart, chunkSize in chunkify(json_file)]
    with mp.Pool(64) as pool:
        doc_ents = pool.starmap(process_wrapper,tmp)
            
    count_dict = join_count_dict(doc_ents)
    print_report_file(report_folder+'report.out',count_dict)
    print_dict(report_folder,count_dict)


def main():
    process(json_file,labels_file,report_folder)

if __name__ == '__main__':
    main()
