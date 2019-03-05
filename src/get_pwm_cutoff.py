#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 30 May 2017 16:43:59

import os,sys,argparse
import subprocess
import tempfile
import numpy as np
from TFBS_Evo.PWM import *
from TFBS_Evo.my_utility import *

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('-p','--pwm',type=str,dest="pwm",help="motif pwm file")
    p.add_argument('--pwm_format',type=str,dest="pwm_format",help="motif pwm format")
    p.add_argument('--pvalue',type=str,dest="pval",help="pval cutoff eg. 0.0001")
    p.add_argument('-b','--background',type=str,dest="background",help="given background nucleotide frequency")
    p.add_argument('--output',type=str,dest="output",help="output file")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

def GetCutoff(pwm, bg_table, pvalue_cutoff):
    # convert pwm to pfm, TFMpvalue can only recognize pfm
    pfm_fin = tempfile.NamedTemporaryFile(delete=False)
    print >>pfm_fin, pwm.save('pfm')
    pfm_fin.flush()
    # run TFMpvalue-pv2sc
    try:
        result = subprocess.check_output("TFMpvalue-pv2sc -a %.6f -t %.6f -c %.6f -g %.6f -m %s -p %s" % (bg_table['A'], bg_table['T'], bg_table['C'], bg_table['G'], pfm_fin.name, pvalue_cutoff), shell=True)
        print >>sys.stderr, "TFMpvalue-pv2sc raw output file"
        print >>sys.stderr, result
        cutoff = float(result.split()[1])
    except:
        error("TFMpvalue-pv2sc cannot found or not run properly")
        exit(1)
    # correct cutoff
    cutoff = cutoff/np.log(2)
    # remove temp file
    os.unlink(pfm_fin.name)
    return cutoff

def Main():
    global args
    args=ParseArg()
    # prepare output
    fout = open(args.output, 'w')
    # load bg
    bg_table = Loadbg(args.background)
    # calculate cutoff
    pwmlist = PWMLIST()
    pwmlist.read(args.pwm, args.pwm_format)
    for pwm in pwmlist:
        cutoff = GetCutoff(pwm, bg_table, args.pval)
        print >>fout, "%s\t%s\t%.6f" % (pwm.id, pwm.name, cutoff)
    fout.close()
 
if __name__=="__main__":
    Main()
