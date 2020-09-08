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
import re
# Import parkages
#from ner_evaluation.ner_eval import Evaluator, collect_named_entities
from nervaluate import Evaluator
# Constants

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

def print_report(label_list,true_file,predict_file,output_file):
    fout = open(output_file,'w',encoding='utf-8')
    _ , y_true = read_ner_file(true_file)
    _ , y_pred = read_ner_file(predict_file)
    # print(y_true[0:3])
    # print(y_pred[0:3])
    print('List of label: ',label_list,file=fout)
    print('=========== Classification Report ===========',file=fout)
    print(classification_report(y_true,y_pred,digits=4),file=fout)
    evaluator = Evaluator(y_true, y_pred, tags=label_list, loader="list")
    results, results_by_tag = evaluator.evaluate()
    print('=========== Overall Results ===========',file=fout)
    print(results,file=fout)
    print('=========== Tags Detail Results ===========',file=fout)
    print(results_by_tag,file=fout)
    
def print_combine_file(true_file,predict_file,output_file):
    word_true, y_true = read_ner_file(true_file)
    word_pred, y_pred = read_ner_file(predict_file)
    fout = open(output_file,'w',encoding='utf-8')
    if (len(word_true) != len(word_pred)):
        print('Errors! Labels and predicts have different length!',file=fout)
        print('Errors! Labels and predicts have different length!')
    else:
        for i in range(len(word_true)):
            for j in range(len(word_true[i])):
                if (len(word_true[i])!=len(word_pred[i])):
                    print('Errors! Sents have different length!',file=fout)
                    print('Errors! Sents have different length!')
                else:
                    if (word_true[i][j]!=word_pred[i][j]):
                        print('Errors! Labels and predicts are different at !',i,file=fout)
                        print('Errors! Labels and predicts are different at !',i,)
                    else:
                        print(word_true[i][j]+' '+y_true[i][j]+' '+y_pred[i][j]+' '+str(y_true[i][j]==y_pred[i][j]),file=fout)
                print('',file=fout)

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
    # Parse the arguments
    parser = argparse.ArgumentParser(description='Do Error Analysis on NER')
    parser.add_argument('--label',type=str, metavar='', required=True, help='Path to input label list file')
    parser.add_argument('--ground_truth',type=str, metavar='', required=True, help='Path to input ground_truth file')
    parser.add_argument('--predict',type=str, metavar='', required=True, help='Path to predicted file (predict)')
    parser.add_argument('--output',type=str, metavar='', required=True, help='Path to output file to print label and predict')
    parser.add_argument('--report',type=str, metavar='', required=True, help='Path to report file to print report')

    args = parser.parse_args()
    label_file = args.label
    true_file = args.ground_truth
    predict_file = args.predict
    output_file = args.output
    report_file = args.report
    label_list = readLabel(label_file)
    print_report(label_list,true_file,predict_file,report_file)
    print_combine_file(true_file,predict_file,output_file)
if __name__ == '__main__':
    main()

