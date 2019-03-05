#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 07 Jun 2017 18:12:11

import os,sys,argparse
from TFBS_Evo.maf_utility import MafFile

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('--maf',type=str,dest="maf",help="maf file folder")
    p.add_argument('--spe',type=str,dest="spe",help="target species")
    p.add_argument('--tree',type=str,dest="tree",help="tree file")
    p.add_argument('--motif',type=str,dest="motif",help="motif pwm file")
    p.add_argument('--motif_id',type=str,dest="motif_id",help="motif id")
    p.add_argument('--motif_cutoff',type=str,dest="motif_cutff",help="motif cutoff")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

def Main():
    global args
    args=ParseArg()
    # load maf
    maf_file = MafFile(args.spe, args.maf)
    # load tree
    tree = LoadTree(args.tree)
    # load motif
    pwm = LoadPWM(args.motif, args.motif_id, args.motif_cutoff)
    # visualization module
    while(True):
        pos = raw_input("Go to?")
        pos = ParsePos(pos, args.width)
        if pos is not None:
            maf_file.see(pos, pwm)
        else:
            pass
 
if __name__=="__main__":
    Main()
