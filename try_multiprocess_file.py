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
# Import modules

# Constants

#function

def process(line):
    n = json.loads(line)
    print(n['doc_id'])

def process_wrapper(input_file, chunkStart, chunkSize):
    with open(input_file,'r') as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            process(line)

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

def main():
    #init objects
    pool = mp.Pool(64)
    jobs = []
    input_file = './data/CORD-NER-ner.json' 
    #create jobs
    for chunkStart,chunkSize in chunkify(input_file):
        jobs.append( pool.apply_async(process_wrapper,(input_file,chunkStart,chunkSize)) )

    #wait for all jobs to finish
    for job in jobs:
        job.get()

    #clean up
    pool.close()
if __name__ == '__main__':
    main()
