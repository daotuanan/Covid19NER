'''
  Function:
    Try multiproces file
  Input:
    
  Output:
    
'''
# Import Libs
import multiprocessing as mp
import os
import json
import functools
import numpy
# Import modules

# Constants

#function

def process(line):
    n = json.loads(line)
    return n['doc_id']

def process_wrapper(input_file, chunkStart, chunkSize):
    res = []
    with open(input_file,'r') as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            tmp = process(line)
            res.append(tmp)
        print(res)
    return res

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
def numpy_flat(a):
    return list(numpy.array(a).flat)


def main():
    #init objects
    res = []
    pool = mp.Pool()
    jobs = []
    input_file = './data/CORD-NER-ner.json' 
    #create jobs
    tmp = [(input_file,chuckStart,chunkSize) for chuckStart, chunkSize in chunkify(input_file)]
    
    res = pool.starmap(process_wrapper,tmp)
        
    #wait for all jobs to finish

    #clean up
    # pool.close()
    # res2 = numpy_flat(res)
    res2 = [item for sublist in res for item in sublist]
    print(len(res2))
if __name__ == '__main__':
    main()
