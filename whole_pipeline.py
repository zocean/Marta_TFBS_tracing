#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 02 Aug 2017 22:01:28

import os,sys,argparse
from os.path import join

def parse_arg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('--mode',type=str,dest="mode",help="mode")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

class Exp(object):
    def __init__(self, region_file, bg_file, motif_file, result_folder):
        self.region = region_file
        self.bg = bg_file
        self.motif = motif_file
        ## check file
        try:
            assert os.path.isfile(self.region) 
            assert os.path.isfile(self.motif)
        except AssertionError:
            print >>sys.stderr, "%s or %s does not exists" % (self.region, self.motif)
            pass
        ## result folder
        self.result_motif_cutoff = join(result_folder, 'pwm_cutoff.txt')
        self.result_tfbs_scan = join(result_folder, 'tfbs_scan')
        self.result_tfbs_evo = join(result_folder, 'tfbs_evo')
        self.result_tfbs_merge = join(result_folder, 'tfbs_merge')
        for folder in [result_folder, self.result_tfbs_scan, self.result_tfbs_evo]:
            if not os.path.isdir(folder):
                os.makedirs(folder)

class Run(object):
    def __init__(self):
        self.home = "/usr0/home/yangz6/bighive/TFBS_Marta"
        self.src = join(self.home, 'code')
        self.data = join(self.home, 'data')
        self.multiz = join(self.home, 'multiz')
        self.annotation = join(self.home, 'annotation')
        self.result = join(self.home, 'result')
        self.tree = join(self.annotation, 'tree_correct.sh')
        self.tree_branchname = join(self.annotation, 'branch_name.txt')
        self.tree_branchtime_ratio = '{:.6f}'.format(96/0.15161)
        ## parameter
        self.spe = 'bosTau6'
        self.pval = "0.0001"
        self.win = 100
        ## region list
        self.exp_list = {}
        self.exp_list['cattle'] = Exp(join(self.data, 'region', 'cattleEnhanc.bed'), join(self.data, 'region', 'cattleEnhanc.bg'), join(self.data, 'motif', 'TFBS_liver_jaspar2016.txt'), join(self.result, 'cattle'))
        self.exp_list['cattle'].bg_ori = join(self.data, 'region', 'NuclFreq_cattleEnhanc.txt')
        self.exp_list['cetartio'] = Exp(join(self.data, 'region', 'cetartioEnhanc.bed'), join(self.data, 'region', 'cetartioEnhanc.bg'), join(self.data, 'motif', 'TFBS_liver_jaspar2016.txt'), join(self.result, 'cetartio'))
        self.exp_list['cetartio'].bg_ori = join(self.data, 'region', 'NuclFreq_cetartioEnhanc.txt')
        self.exp_list['mammal'] = Exp(join(self.data, 'region', 'mammalEnhanc.bed'), join(self.data, 'region', 'mammalEnhanc.bg'), join(self.data, 'motif', 'TFBS_liver_jaspar2016.txt'), join(self.result, 'mammal'))
        self.exp_list['mammal'].bg_ori = join(self.data, 'region', 'NuclFreq_mammalEnhanc.txt')
        ## merge all the region together
        self.exp_merge = Exp(join(self.data, 'region', 'mergeEnhanc.bed'), join(self.data, 'region', 'mergeEnhanc.bg'), join(self.data, 'motif', 'TFBS_liver_jaspar2016.txt'), join(self.result, 'merge'))
        ## motif file
        #self.motif_file = join(self.data, 'motif', 'TFBS_liver_jaspar2016.txt')
        self.motif_file = join(self.data, 'motif', 'pwm_vertebrates14March2017.txt')
        ## report
        self.report_folder = join(self.result, 'report')
        if not os.path.isdir(self.report_folder):
            os.makedirs(self.report_folder)

def run_prep(fout):
    print >>fout, "# split multiz into separata maf"
    print >>fout, "python %s/split_maf.py --maf %s/boreoMafChinese_May2015.maf --folder %s" % (args.src, args.multiz, args.multiz)
    print >>fout, ""
    print >>fout, "# prepare nucleotide freq"
    print >>fout, "python %s/get_bg.py --input %s --output %s" % (args.src, args.exp_list['cattle'].bg_ori, args.exp_list['cattle'].bg)
    print >>fout, "python %s/get_bg.py --input %s --output %s" % (args.src, args.exp_list['cetartio'].bg_ori, args.exp_list['cetartio'].bg)
    print >>fout, "python %s/get_bg.py --input %s --output %s" % (args.src, args.exp_list['mammal'].bg_ori, args.exp_list['mammal'].bg)
    print >>fout, ""
    print >>fout, "# calculate motif pwm cutoff"
    print >>fout, "python %s/get_pwm_cutoff.py --pwm %s --pwm_format %s --pvalue %s --background %s --output %s >%s 2>&1 &" % (args.src, args.motif_file, 'jaspar', args.pval, args.exp_list['cattle'].bg, args.exp_list['cattle'].result_motif_cutoff, args.exp_list['cattle'].result_motif_cutoff.replace('.txt', '.log'))
    print >>fout, "python %s/get_pwm_cutoff.py --pwm %s --pwm_format %s --pvalue %s --background %s --output %s >%s 2>&1 &" % (args.src, args.motif_file, 'jaspar', args.pval, args.exp_list['cetartio'].bg, args.exp_list['cetartio'].result_motif_cutoff, args.exp_list['cetartio'].result_motif_cutoff.replace('.txt', '.log'))
    print >>fout, "python %s/get_pwm_cutoff.py --pwm %s --pwm_format %s --pvalue %s --background %s --output %s >%s 2>&1 &" % (args.src, args.motif_file, 'jaspar', args.pval, args.exp_list['mammal'].bg, args.exp_list['mammal'].result_motif_cutoff, args.exp_list['mammal'].result_motif_cutoff.replace('.txt', '.log'))
    print >>fout, ""

def get_motif_cutoff(file_name):
    fin = open(file_name, 'r')
    table = {}
    for line in fin:
        row = line.strip().split()
        table[row[0]] = (row[1], row[2])
    fin.close()
    return table

def run_evo(folder, is_merge_exp):
    # scan tfbs in region
    for group in args.exp_list.keys():
        fout = open(join(folder, 'run_evo_scan_%s.sh' % (group)), 'w')
        exp = args.exp_list[group]
        motif_table = get_motif_cutoff(exp.result_motif_cutoff)
        for motif in sorted(motif_table.keys()):
            motif_name,motif_cutoff = motif_table[motif]
            out_file = join(exp.result_tfbs_scan, "%s_%s.txt" % (motif, motif_name))
            log_file = join(exp.result_tfbs_scan, "%s_%s.log" % (motif, motif_name))
            print >>fout, "python %s/tfbs_scan_beta.py --maf %s --region %s --rescan --w %d --pwm %s --motifformat %s --background %s --motifid %s --cutoff %s -s %s -t %s -o %s >%s 2>&1" % (args.src, args.multiz, exp.region, args.win, args.motif_file, 'jaspar', exp.bg, motif, motif_cutoff, args.spe, args.tree, out_file, log_file)
        fout.close()
    # merge all the exp
    if is_merge_exp:
        fout = open(join(folder, 'run_evo_scan_merge.sh'), 'w')
        for motif in sorted(motif_table.keys()):
            motif_name,motif_cutoff = motif_table[motif]
            scan_file_list = []
            for group in args.exp_list.keys():
                exp = args.exp_list[group]
                scan_file = join(exp.result_tfbs_scan, "%s_%s.txt" % (motif, motif_name))
                scan_file_list.append(scan_file)
            merge_scan_file = join(args.exp_merge.result_tfbs_scan, "%s_%s.txt" % (motif, motif_name))
            print >>fout, "python %s/tfbs_scan_merge.py --filelist %s --out %s" % (args.src, ' '.join(scan_file_list), merge_scan_file)
        fout.close()
        # predict tfbs branch-of-origin
        fout = open(join(folder, 'run_evo_predict_merge.sh'), 'w')
        for motif in sorted(motif_table.keys()):
            motif_name, motif_cutoff = motif_table[motif]
            count_file = join(args.exp_merge.result_tfbs_scan, "%s_%s.txt" % (motif, motif_name))
            out_file = join(args.exp_merge.result_tfbs_evo, "%s_%s.txt" % (motif, motif_name))
            log_file = join(args.exp_merge.result_tfbs_evo, "%s_%s.log" % (motif, motif_name))
            print >>fout, "python %s/TFBS_Evo_beta.py --np 4 --maf %s --count %s --tree %s --species %s --name %s --branchtime user --branchtime_ratio %s --win %d --output %s --outorder maf >%s 2>&1" % (args.src, args.multiz, count_file, args.tree, args.spe, args.tree_branchname, args.tree_branchtime_ratio, args.win, out_file, log_file)
        fout.close()
        # report summary statistic
        fout = open(join(folder, 'run_evo_summary_merge.sh'), 'w')
        print >>fout, "python %s/TFBS_Evo_merge.py --evo_folder %s --scan_folder %s --species %s --motif %s --prefix %s" % (args.src, args.exp_merge.result_tfbs_evo, args.exp_merge.result_tfbs_scan, args.tree_branchname, args.motif_file, args.exp_merge.result_tfbs_merge)
        fout.close()
    else:
        # remove duplicate rows # close TFBS may generate duplicate rows
        # predict tfbs branch-of-origin
        for group in args.exp_list.keys():
            fout = open(join(folder, 'run_evo_predict_%s.sh' % (group)), 'w')
            exp = args.exp_list[group]
            motif_table = get_motif_cutoff(exp.result_motif_cutoff)
            for motif in sorted(motif_table.keys()):
                motif_name, motif_cutoff = motif_table[motif]
                count_file = join(exp.result_tfbs_scan, "%s_%s.txt" % (motif, motif_name))
                out_file = join(exp.result_tfbs_evo, "%s_%s.txt" % (motif, motif_name))
                log_file = join(exp.result_tfbs_evo, "%s_%s.log" % (motif, motif_name))
                print >>fout, "python %s/TFBS_Evo_beta.py --np 4 --maf %s --count %s --tree %s --species %s --name %s --branchtime user --branchtime_ratio %s --win %d --output %s --outorder maf >%s 2>&1" % (args.src, args.multiz, count_file, args.tree, args.spe, args.tree_branchname, args.tree_branchtime_ratio, args.win, out_file, log_file)
            fout.close()
        # report summary statistic
        # also merge tfbs into one big file, sorted
        # e.g. number of tfbs and fraction of different branch-of-origin
        for group in args.exp_list.keys():
            fout = open(join(folder, 'run_evo_summary_%s.sh' % (group)), 'w')
            exp = args.exp_list[group]
            print >>fout, "python %s/TFBS_Evo_merge.py --evo_folder %s --scan_folder %s --species %s --motif %s --prefix %s" % (args.src, exp.result_tfbs_evo, exp.result_tfbs_scan, args.tree_branchname, args.motif_file, exp.result_tfbs_merge)
            fout.close()

def get_motif_list(motif_file):
    fin = open(motif_file, 'r')
    table = {}
    for line in fin:
        if line.strip().startswith('#'):
            continue
        if line.strip().startswith('>'):
            row = line.strip().split()
            table[row[0].replace('>','')] = row[1]
    fin.close()
    return table

def run_report():
    label_list = ['cattle', 'cetartio', 'mammal']
    bed_list = [args.exp_list[label].region for label in label_list]
    cmd = "%s/misc_report.py --input %s --bedlist %s --labellist %s --folder %s " % (args.src, args.exp_merge.result_tfbs_merge+'_merge.txt', ' '.join(bed_list), ' '.join(label_list), args.report_folder) 
    print cmd

def main():
    global opt
    opt = parse_arg()
    global args
    args = Run()
    if opt.mode == 'prep':
        fout = open('run_prep.sh', 'w')
        run_prep(fout)
    elif opt.mode == 'evo':
        if not os.path.isdir('run_evo'):
            os.makedirs('run_evo')
        run_evo('run_evo', True)
    elif opt.mode == 'report':
        run_report()
    else:
        print >>sys.stderr, "Unknown mode: %s" % (mode)
    
if __name__=="__main__":
    main()
