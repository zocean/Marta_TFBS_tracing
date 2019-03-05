#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 30 May 2017 14:28:26

import os,sys,argparse

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('--input',type=str,dest="input",help="input file")
    p.add_argument('--output',type=str,dest="output",help="output file")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

def Main():
    global args
    args=ParseArg()
    fin = open(args.input, 'r')
    header = {}
    for line in fin:
        row = line.strip().split()
        if line.strip().startswith('#'):
            for nn in range(len(row)):
                header[row[nn]] = nn
        elif 'total' in line:
            A = float(row[header['A']])
            C = float(row[header['C']])
            G = float(row[header['G']])
            T = float(row[header['T']])
            N = float(row[header['N']])
        else:
            pass
    fin.close()
    fout = open(args.output, 'w')
    total = A + C + G + T
    AT = (A+T)/2
    CG = (C+G)/2
    print >>fout, "A\t%.6f" % (AT/total)
    print >>fout, "C\t%.6f" % (CG/total)
    print >>fout, "G\t%.6f" % (CG/total)
    print >>fout, "T\t%.6f" % (AT/total)
    fout.close()

if __name__=="__main__":
    Main()
