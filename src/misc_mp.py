#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : zocean
# Date: 
# Last-modified: 06 Jun 2017 14:03:30

import os,sys,argparse
from time import clock
from multiprocessing import Pool

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('-i','--input',type=str,dest="input",help="input script")
    p.add_argument('--np',type=int,dest="np",help="number of process")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

def SecondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],[(t*1000,),1000,60,60])

def Main():
    global args
    args=ParseArg()
    cmd_list = []
    fin = open(args.input, 'r')
    for line in fin:
        if line.strip().startswith('#') or line.strip() == '':
            continue
        cmd_list.append(line.strip())
    fin.close()
    # 
    result_list = []
    def log_result(result):
        result_list.append(result)
        if len(result_list) % 100 == 0:
            print >>sys.stderr, "%d run done" % (len(result_list))

    start = clock()
    pool = Pool(processes = args.np)
    for cmd in cmd_list:
        pool.apply_async(SingleRun, [cmd], callback=log_result)
    pool.close()
    pool.join()
    stop = clock()
    print >>sys.stderr, "program done, takes %s" % (SecondsToStr(stop-start))

def SingleRun(cmd):
    try:
        os.system(cmd)
    except:
        print cmd
    return 1
    
if __name__=="__main__":
    Main()
