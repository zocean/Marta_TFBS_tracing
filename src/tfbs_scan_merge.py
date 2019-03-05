#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 31 Jul 2017 23:04:18

import os,sys,argparse

def parse_arg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('--filelist',type=str,dest="filelist",nargs="+",help="filelist")
    p.add_argument('--out',type=str,dest="out",help="output filename")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

def main():
    global args
    args = parse_arg()
    fout = open(args.out, 'w')
    first_file = True
    for filename in args.filelist:
        fin = open(filename, 'r')
        num = 0
        for line in fin:
            if first_file and num == 0:
                print >>fout, line.strip()
                first_file = False
            elif num ==0:
                pass
            else:
                print >>fout, line.strip()
            num += 1
        fin.close()
 
if __name__=="__main__":
    main()
