'''
  Function:
    Split a CoNLL format NER labelled file into train dev test.
  Input:
    --ratio: ratio of train(default=0.8) => test = dev = 100% - train
    --input: path to the input file
  Output:
    train.txt
    dev.txt
    test.txt
    
'''
# Import Libs
import argparse
from sklearn.model_selection import train_test_split
# Import modules

# Constants
train_ratio = 0.8

def calculateRatio(train_ratio):
    return (1.0-train_ratio)/2.0 , (1.0-train_ratio)/2.0

def writeFile(input_file,data):
    with open(input_file,'w',encoding='utf-8') as fout:
        for d in data:
            fout.write(d+'\n')

def splitData(input_file,train_ratio,dev_ratio,test_ratio):
    text = open(input_file,'r',encoding='utf-8').read()
    sents = text.split('\n\n')
    train,dev_test = train_test_split(sents,test_size=(dev_ratio+test_ratio))
    dev,test = train_test_split(dev_test,test_size=test_ratio)
    writeFile('train.txt',train)
    writeFile('dev.txt',dev)
    writeFile('test.txt',test)


def main():
    parser = argparse.ArgumentParser(description='Split CoNLL NER format file into train dev test')
    parser.add_argument('--ratio',type=float, metavar='', required=False, help='Ratio of train in data (default = 0.8)')
    parser.add_argument('--input',type=str, metavar='', required=True, help='Path to the input file')

    # parse args
    args = parser.parse_args()
    if args.ratio is not None:
        train_ratio = args.ratio
    input_file = args.input

    dev_ratio, test_ratio = calculateRatio(train_ratio)
    splitData(input_file,train_ratio,dev_ratio,test_ratio)


if __name__ == '__main__':
    main()