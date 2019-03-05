#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 30 May 2017 13:09:47

import os,sys,argparse

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('--maf',type=str,dest="maf",help="multiz maf file")
    p.add_argument('--folder',type=str,dest="folder",help="folder")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

def Main():
    global args
    args=ParseArg()
    fin = open(args.maf, 'r')
    buffer_list = []
    fout = None
    for line in fin:
        if line.strip().startswith('#'):
            if 'eof' in line:
                print >>fout, line,
                fout.close()
                fout = None
            elif 'chr' in line:
                out_file = line.strip().split('/')[-1].replace('.all.maf','')
                fout = open(args.folder +'/' + out_file+'.maf', 'w')
                buffer_list.append(line)
            else:
                if fout is None:
                    buffer_list.append(line)
        if fout is not None and len(buffer_list) > 0:
            print >>fout, ''.join(buffer_list), 
            buffer_list = []
        elif line.strip() == "" and fout is None:
            continue
        elif fout is None:
            continue
        else:
            print >>fout, line,
    if fout is not None:
        fout.close()
    fin.close()
    
if __name__=="__main__":
    Main()
