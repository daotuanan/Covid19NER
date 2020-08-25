'''
Run Error Analysis on NER task.

Input: test_label file and test_predict file in BIO format:
    Example in test_predict:
        Gab B-ORG
        appears O
        to O
        be O
        losing O
        investors O
        after O
        Pittsburgh B-ORG
        shooting O

Output:
    + Boundary Errors: Unrecognized or partial recognized NE
    + Type Errors: fully recognize but miss-classified type.
    + Misclassified NE
    + Partial Recognized NE
    + UnRecognized NE
'''
# Import Libs
import argparse
from seqeval.metrics import classification_report
import pandas as pd
# Import parkages
from ner_evaluation.ner_eval import Evaluator, collect_named_entities
from nervaluate import Evaluator
# Constants
baselines_path_prefix = '../CoNLL_NER/'
baseline_path_postfix = '/test_prediction.txt'
baselines = [ 'multidomain_engeval-roberta_10epoch-model',\
    'multidomain_engeval-roberta-model',\
    'multidomain_engeval-roberta_5epoch-model',\
    'engeval-roberta_cased-model']
baseline_path = [baselines_path_prefix+baseline+baseline_path_postfix for baseline in baselines]
result_path_prefix = './results/'

def read_ner_file(input_file):
    '''
    Function:
        Read NE file and convert into list of list
    Input:
        input_file(str): the path to the input file
    Output:
        ner_list(list of list)
    '''
    fin = open(input_file,'r',encoding='utf-8').read()
    ner_list = []
    word_list = []
    sents = fin.split('\n\n')
    for sent in sents:
        sent_tags = []
        sent_words = []
        if sent == '':
            break
        words = sent.split('\n')
        for word in words:
            if word == '':
                break
            tmp = word.split(' ')
            tag = tmp[1]
            word= tmp[0]
            sent_tags.append(tag)
            sent_words.append(word)
        ner_list.append(sent_tags)
        word_list.append(sent_words)
        
    return word_list , ner_list

def print_report(label_file,predict_file,output_file):
    fout = open(output_file,'w',encoding='utf-8')
    _ , y_true = read_ner_file(label_file)
    _ , y_pred = read_ner_file(predict_file)
    print('=========== Classification Report ===========',file=fout)
    print(classification_report(y_true,y_pred,digits=4),file=fout)
    evaluator = Evaluator(y_true, y_pred, tags=['LOC', 'PER','ORG','MISC'], loader="list")
    results, results_by_tag = evaluator.evaluate()
    print('=========== Overall Results ===========',file=fout)
    print(results,file=fout)
    print('=========== Tags Detail Results ===========',file=fout)
    print(results_by_tag,file=fout)
    
def print_combine_file(label_file,predict_file,output_file):
    word_true, y_true = read_ner_file(label_file)
    word_pred, y_pred = read_ner_file(predict_file)
    fout = open(output_file,'w',encoding='utf-8')
    if (len(word_true) != len(word_pred)):
        print('Errors! Labels and predicts have different length!',file=fout)
        print('Errors! Labels and predicts have different length!')
    for i in range(len(word_true)):
        for j in range(len(word_true[i])):
            if (word_true[i][j]!=word_pred[i][j]):
                print('Errors! Labels and predicts are different at !',i,file=fout)
                print('Errors! Labels and predicts are different at !',i,)
            else:
                print(word_true[i][j]+' '+y_true[i][j]+' '+y_pred[i][j]+' '+str(y_true[i][j]==y_pred[i][j]),file=fout)
        print('',file=fout)

def print_compare_file(label_file,baseline_path,output_file):
    fout = open(output_file,'w',encoding='utf-8')
    word_true, y_true = read_ner_file(label_file)
    list_y_pred = []
    for baseline in baseline_path:
        y_pred = read_ner_file(baseline)
        list_y_pred.append(y_pred)
    for i in range(len(y_true)):
        for j in range(len(y_true[i])):
            cur_pred = []
            for t in range(len(list_y_pred)):
                cur_pred.append(list_y_pred[t][i][j])
            print(word_true[i][j]+' '+y_true+' '.join(cur_pred)+' '+str(all(cur_pred)),file=fout)
        print('',file=fout)


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description='Do Error Analysis on NER')
    parser.add_argument('--label',type=str, metavar='', required=True, help='Path to input label file (ground-truth)')
    parser.add_argument('--output',type=str, metavar='', required=True, help='Path to output file to print label and predict')

    args = parser.parse_args()
    label_file = args.label
    output_file = args.output
    # print_report(label_file,predict_file,report_file)
    # print_combine_file(label_file,predict_file,output_file)
    print_compare_file(label_file,baseline_path,output_file)
if __name__ == '__main__':
    main()

