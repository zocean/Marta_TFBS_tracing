#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 02 Aug 2017 10:37:01

import os,sys,argparse
from os.path import join

def parse_arg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('--evo_folder',type=str,dest="evo_folder",help="folder used to store result from tfbs_evo code")
    p.add_argument('--scan_folder',type=str,dest="scan_folder",help="folder used to store tfbs scan")
    p.add_argument('--species',type=str,dest="species",help="branch name file")
    p.add_argument('--motif',type=str,dest="motif",help="motif file")
    p.add_argument('--prefix',type=str,dest="prefix",help="result file prefix")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

class Result(object):
    def __init__(self,motif_id, motif_name, branch_list):
        self.motif_id = motif_id
        self.motif_name = motif_name
        self.scan_count = 0
        self.evo_count = None
        self.tfbs_scan_file = "%s_%s.txt" % (self.motif_id, self.motif_name)
        self.tfbs_evo_file = "%s_%s.txt" % (self.motif_id, self.motif_name)
        self.age_count_table = dict((branch, 0) for branch in branch_list)
        self.age_per_table = dict((branch, None) for branch in branch_list)
    def write(self, branch_list):
        if self.evo_count is None:
            self.evo_count = sum(self.age_count_table.values())
        return "%s\t%s\t%d\t%d\t%s" % (self.motif_name, self.motif_id, self.scan_count, self.evo_count, '\t'.join([str(self.age_count_table[branch]) for branch in branch_list]))
    @staticmethod
    def header(branch_list):
        return "motif_name\tmotif_id\tscan_count\tfinal_count\t" + '\t'.join([branch for branch in branch_list])

def get_motif_list(motif_file):
    fin = open(motif_file, 'r')
    motif_list = []
    for line in fin:
        if line.strip().startswith('#'):
            continue
        if line.strip().startswith('>'):
            row = line.strip().split()
            motif_list.append((row[1], row[0].replace('>','')))
    fin.close()
    return sorted(motif_list, key = lambda item: (item[0]))

def load_branch(branchname_file):
    branch_list = []
    fin = open(branchname_file)
    for line in fin: 
        if line.strip().startswith('#') or line.strip() == '':
            continue
        row = line.strip().split()
        branch_a = row[0]
        branch_b = row[1]
        name = row[2]
        if len(branch_list) == 0:
            branch_list.append(branch_a)
        branch_list.append(name)
    return branch_list

def count_tfbs_scan(filename):
    fin = open(filename, 'r')
    total = 0
    for line in fin:
        row = line.strip().split()
        if row[0] == 'pos':
            continue
        else:
            total += len(row[0].split(','))
    fin.close()
    return total

def parse_tfbs_evo(filename, result, fout, label):
    fin = open(filename, 'r')
    for line in fin:
        if line.strip().startswith('#') or line.strip() == '':
            continue
        row = line.strip().split()
        branch = row[3]
        result.age_count_table[branch] += 1
        print >>fout, line.strip() + '\t' + label
    fin.close()

def main():
    global args
    args = parse_arg()
    motif_list = get_motif_list(args.motif)
    branch_list = load_branch(args.species)
    # build result summary 
    result_list = []
    fout = open(args.prefix + '_merge.txt', 'w')
    fout_summary = open(args.prefix + '_summary.txt', 'w')
    print >>fout_summary, Result.header(branch_list)
    for motif in motif_list:
        motif_name = motif[0]
        motif_id = motif[1]
        result_list.append(Result(motif_id, motif_name, branch_list))
    for motif in result_list:
        tfbs_scan_file = join(args.scan_folder, motif.tfbs_scan_file)
        tfbs_evo_file = join(args.evo_folder, motif.tfbs_evo_file)
        tfbs_count = count_tfbs_scan(tfbs_scan_file)
        if tfbs_count < 1:
            continue
        motif.scan_count = tfbs_count
        parse_tfbs_evo(tfbs_evo_file, motif, fout, motif.motif_name+'_'+motif.motif_id)
        print >>fout_summary, motif.write(branch_list)
    fout.close()
    fout_summary.close()
    # sort tfbs
    os.system("sort -k1,1 -k2,2n %s >%s" % (args.prefix + '_merge.txt', args.prefix + '_merge.txt.sort'))
    os.system("mv %s %s" % (args.prefix + '_merge.txt.sort', args.prefix + '_merge.txt'))
 
if __name__=="__main__":
    main()
