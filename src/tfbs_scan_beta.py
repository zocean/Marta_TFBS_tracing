#!/home/yangz6/Software/Python-2.7.5/python
# Programmer : zocean
# Date: 
# Last-modified: 02 Jun 2017 00:44:28

import os,sys,argparse
from operator import itemgetter,attrgetter
from ete2 import Tree
from TFBS_Evo.my_utility import *
from TFBS_Evo.PWM import PWM,PWMLIST
from TFBS_Evo.maf_utility import *

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s beta.20150728')
    p.add_argument('--maf',type=str,dest="maf",help="multize maf file folder")
    p.add_argument('-r','--region',type=str,dest="region",help="chip-seq peak region")
    p.add_argument('--rescan',dest="rescan",action="store_true",help="scan tfbs within each peak and recreate new search window for each tfbs identified")
    p.add_argument('--summit',dest="summit",action="store_true",help="the region file is in narrowPeak format, use summit information")
    p.add_argument('--threshold',type=int,dest="thres",help="threshold to filter peak region")
    p.add_argument('--threscol',type=int,dest="threscol",help="the column number of threshold (0-base), if not set, will use the fourth column and assume the fourth column is this format XXX.<score>")
    p.add_argument('-w','--win',type=int,dest="win",help="peak window size (half!!!) extended from the center of peak region")
    p.add_argument('-p','--pwm',type=str,dest="pwm",help="motif pwm file")
    p.add_argument('--motifformat',type=str,dest="motifformat",help="motif format, jaspar, tab, freq, freq_vert and consensus")
    p.add_argument('--background',type=str,dest="background",help="motif background file")
    p.add_argument('--motifid',type=str,dest="motifid",help="motif used in given motif pwm file")
    p.add_argument('--cutoff',type=float,dest="cutoff",help="log-odds score cutoff to call a sequence TFBS")
    p.add_argument('-k','--kmer',type=str,dest="kmer",help="kmder list, --pwm and --kmer is mutually exclusive")
    p.add_argument('--rc',action="store_true",dest="rc",help="whether allow reverse complement of kmer as match, default is False")
    p.add_argument('-s','--species',type=str,dest="spe",help="target species name")
    p.add_argument('-t','--tree',type=str,dest="tree",help="same phylogenetic tree used in maf file")
    p.add_argument('-o','--output',type=str,dest="output",help="output file name")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

def LoadPWM(pwm_file,motifformat,motifid,fname_bg):
    """LoadPWM file"""
    pwmlist = PWMLIST()
    pwmlist.read(pwm_file,motifformat)
    pwm = pwmlist[motifid]
    if fname_bg is not None:
        bg_table = Loadbg(fname_bg)
        pwm.updatebg(bg_table)
    pwm.getlll()
    return pwm

def LoadKmer(kmerfile,is_rc):
    """Read kmer from file, this is the interface to support BOO input"""
    kmer_list = []
    for line in ReadFromFile(kmerfile):
        if line.strip().startswith('#') or line.strip() == '':
            continue
        row = line.strip().split()
        kmer = row[0]
        kmer_list.append(kmer.upper())
        if is_rc:
            kmer_list.append(rcDNA(kmer).upper())
    return list(set(kmer_list))

def RescanRegion(file_name, pwm, cutoff, region_win, target_spe):
    '''
    rescan tfbs in regions from file_name
    report peak location based on region_win
    '''
    # load maf index
    maf_index = LoadMafIndex(target_spe)
    tfbs_list = []
    fin = ReadFromFile(file_name)
    for line in fin:
        if line.strip().startswith('#') or line.strip() == '':
            continue
        row = line.strip().split()
        chrom = row[0]
        start = int(row[1])
        stop = int(row[2])
        idx = maf_index[chrom]
        maf_result = idx.search([start], [stop])
        tfbs_list += Scan_pwm_from_target_maf(maf_result, start, stop, pwm, cutoff, target_spe)
    fin.close()
    #
    region_list = []
    for tfbs in tfbs_list: 
        chrom,start,stop = tfbs
        new_start = max(0, (start+stop)/2 - region_win)
        new_stop = (start+stop)/2 + region_win
        region_list.append(Bed(chrom, new_start, new_stop))
    return region_list

def LoadRegion(file_name,thres,threscol,win,issummit):
    """Read peak region file"""
    regionlist = []
    for line in ReadFromFile(file_name):
        if line.strip().startswith('#') or line.strip() == '':
            continue
        row = line.strip().split()
        chrom = row[0]
        start = int(row[1])
        stop = int(row[2])
        if thres is not None:
            if threscol is not None:
                score = int(row[threscol])
            else:
                score = int(row[3].split('.')[-1])
            if score < thres:
                continue
        if win is not None:
            if issummit:
                summit = int(row[9])
                new_start = start + summit - win
                new_stop = start + summit + win
            else:
                new_start = (start+stop)/2-win
                new_stop = (start+stop)/2+win
        else:
            new_start = start
            new_stop = stop
        regionlist.append(Bed(chrom,new_start,new_stop))
    return regionlist

def LoadMafIndex(spe):
    """Load maf index file into dictionary"""
    index_table = {}
    LoadAllMafIndex(index_table,maf_path,spe)
    return index_table 

def LoadTree(filename):
    t = Tree(filename)
    return t

def GetPos(seqrec):
    """get chrom,start,stop from maf seqrec object"""
    if seqrec.annotations['size'] > 0:
        chrom = seqrec.id.split('.')[1]
        if seqrec.annotations['strand'] == '+1':
            start = seqrec.annotations['start']
            stop = seqrec.annotations['start'] + seqrec.annotations['size']
            strand = '+'
        else:
            start = seqrec.annotations['srcSize'] - seqrec.annotations['start'] - seqrec.annotations['size']
            stop = start + seqrec.annotations['size']
            strand = '-'
        return chrom, start, stop, strand
    return None,None,None,None

def MergeSeq(alignment):
    """merge adjacent Seq object"""
    merged = []
    chrom = None
    start = None
    stop = None
    dna = None
    for seq in sorted(alignment,key=attrgetter('chrom','start')):
        if chrom != seq.chrom:
            if stop is not None:
                merged.append(Seq(chrom,start,stop,dna))
            start = seq.start
            chrom = seq.chrom
            stop = seq.stop
            dna = seq.seq
        else:
            if stop == seq.start:
                stop = seq.stop
                dna += seq.seq
            else:
                merged.append(Seq(chrom,start,stop,dna))
                start = seq.start
                stop = seq.stop
                dna = seq.seq
    if chrom is not None and start is not None and stop is not None:
        merged.append(Seq(chrom,start,stop,dna))
    return merged

def GetMotifPosKmer(alignment,kmerlist,tree,target_spe):
    """find the exact location of motif in seq"""
    motif_list = {'pos':[],'count':{}}
    for kmer in kmerlist:
        kmer_len = len(kmer)
        for spe in alignment.keys():
            if not spe in tree:
                continue
            for seq in alignment[spe]:
                if len(seq.seq) < kmer_len:
                    continue
                else:
                    for nn in range(len(seq.seq) - kmer_len+1):
                        if seq.seq[nn:nn+kmer_len] == kmer:
                            try:
                                motif_list['count'][spe] += 1
                            except KeyError:
                                motif_list['count'][spe] = 1
                            if spe == target_spe:
                                motif_chrom = seq.chrom
                                motif_start = seq.start + nn
                                motif_stop = seq.start + nn + kmer_len
                                motif_list['pos'].append(motif_chrom+':'+str(motif_start)+'-'+str(motif_stop))
    for spe in tree.get_leaf_names():
        if spe not in motif_list['count'].keys():
            motif_list['count'][spe] = 0
    return motif_list

def GetMotifPosPWM(alignment,pwm,cutoff,tree,target_spe):
    motif_list = {'pos':[], 'count':{}}
    for spe in tree.get_leaf_names():
        motif_list['count'][spe] = 0
    tfbs_len = pwm.length
    for spe in alignment.keys():
        if spe not in tree:
            continue
        for seq in alignment[spe]:
            if len(seq.seq) < tfbs_len:
                continue
            else:
                for nn in range(len(seq.seq)-tfbs_len+1):
                    if 'N' in seq.seq[nn:nn+tfbs_len]:
                        continue
                    if pwm.calscore(seq.seq[nn:nn+tfbs_len]) > cutoff or pwm.calscore(rcDNA(seq.seq[nn:nn+tfbs_len])) > cutoff: # check both seq and its reverse complementary seq
                        motif_list['count'][spe] += 1
                        if spe == target_spe:
                            motif_chrom = seq.chrom
                            motif_start = seq.start + nn
                            motif_stop = seq.start + nn + tfbs_len
                            motif_list['pos'].append(motif_chrom+':'+str(motif_start)+'-'+str(motif_stop))
    return motif_list

def Scan_kmer_from_maf(maf_result,start,stop,kmer_list,target_spe,tree):
    """get tfbs position from maf file"""
    alignment = {}
    for multiple_alignment in MafQuery(maf_result,target_spe,start,stop):
        for nn in range(len(multiple_alignment)):
            seqrec = multiple_alignment[nn]
            spe_name = seqrec.id.split('.')[0]
            spe_chrom,spe_start,spe_stop,spe_strand = GetPos(seqrec)
            spe_seq = str(seqrec.seq).replace('-','').upper()
            if spe_strand != '+': # convert minus strand seq to plus strand sequence
                spe_seq = rcDNA(spe_seq)
            if spe_chrom is None or spe_start is None or spe_stop is None:
                continue
            try:
                alignment[spe_name].append(Seq(spe_chrom,spe_start,spe_stop,spe_seq))
            except KeyError:
                alignment[spe_name] = [Seq(spe_chrom,spe_start,spe_stop,spe_seq)]
    for spe in alignment.keys():
        merge_seq = MergeSeq(alignment[spe])
        alignment[spe] = merge_seq
    return GetMotifPosKmer(alignment,kmer_list,tree,target_spe)

def Scan_kmer(region_file,kmer_list,target_spe,tree_file,output_file):
    """report tfbs count using kmer list"""
    out = WriteToFile(output_file)
    region_list = LoadRegion(region_file,args.thres,args.threscol,args.win,args.summit)
    tree = LoadTree(tree_file)
    # load maf index
    maf_index = LoadMafIndex(target_spe)
    # search tfbs
    print >>out, "pos" + '\t' + '\t'.join([name for name in tree.get_leaf_names()])
    num = 1
    for peak in region_list:
        if num % 1000 == 0:
            logging("Process: %d peak done" % (num))
        num += 1
        idx = maf_index[peak.chrom]
        maf_result = idx.search([peak.start],[peak.stop])
        motif_list = Scan_kmer_from_maf(maf_result,peak.start,peak.stop,kmer_list,target_spe,tree)
        if len(motif_list['pos']) > 0 and motif_list['count'][target_spe] > 0:
            print >>out, ','.join(motif_list['pos']) + '\t' + '\t'.join(str(motif_list['count'][name]) for name in tree.get_leaf_names())

def Scan_pwm_from_target_maf(maf_result, start, stop, pwm, cutoff, target_spe):
    alignment = []
    for multiple_alignment in MafQuery(maf_result,target_spe,start,stop):
        for nn in range(len(multiple_alignment)):
            seqrec = multiple_alignment[nn]
            spe_name = seqrec.id.split('.')[0]
            if spe_name != target_spe:
                continue
            spe_chrom,spe_start,spe_stop,spe_strand = GetPos(seqrec)
            spe_seq = str(seqrec.seq).replace('-','').upper()
            if spe_strand != '+': # bug found in 0728, MergeSeq will report wrong order of maf blocks if the blocks are in minus strand. solution, convert sequence in minus strand to plus strand by reverse complement
                spe_seq = rcDNA(spe_seq)
            if spe_chrom is None or spe_start is None or spe_stop is None:
                continue
            try:
                alignment.append(Seq(spe_chrom, spe_start, spe_stop, spe_seq))
            except KeyError:
                alignment = [Seq(spe_chrom, spe_start, spe_stop, spe_seq)]
    merge_seq = MergeSeq(alignment)
    # get tfbs location
    tfbs_list = []
    tfbs_len = pwm.length
    for seq in merge_seq:
        if seq.seq < pwm.length:
            pass
        else:
            for nn in range(len(seq.seq)-tfbs_len+1):
                if 'N' in seq.seq[nn:nn+tfbs_len]:
                    continue
                if pwm.calscore(seq.seq[nn:nn+tfbs_len]) > cutoff or pwm.calscore(rcDNA(seq.seq[nn:nn+tfbs_len])) > cutoff: # check both seq and its reverse complementary seq
                    motif_chrom = seq.chrom
                    motif_start = seq.start + nn
                    motif_stop = seq.start + nn + tfbs_len
                    tfbs_list.append((motif_chrom, motif_start, motif_stop))
    return tfbs_list

def Scan_pwm_from_maf(maf_result,start,stop,pwm,cutoff,target_spe,tree):
    alignment = {}
    for multiple_alignment in MafQuery(maf_result,target_spe,start,stop):
        for nn in range(len(multiple_alignment)):
            seqrec = multiple_alignment[nn]
            spe_name = seqrec.id.split('.')[0]
            spe_chrom,spe_start,spe_stop,spe_strand = GetPos(seqrec)
            spe_seq = str(seqrec.seq).replace('-','').upper()
            if spe_strand != '+': # bug found in 0728, MergeSeq will report wrong order of maf blocks if the blocks are in minus strand. solution, convert sequence in minus strand to plus strand by reverse complement
                spe_seq = rcDNA(spe_seq)
            if spe_chrom is None or spe_start is None or spe_stop is None:
                continue
            try:
                alignment[spe_name].append(Seq(spe_chrom,spe_start,spe_stop,spe_seq))
            except KeyError:
                alignment[spe_name] = [Seq(spe_chrom,spe_start,spe_stop,spe_seq)]
    for spe in alignment.keys():
        merge_seq = MergeSeq(alignment[spe])
        alignment[spe] = merge_seq
    return GetMotifPosPWM(alignment,pwm,cutoff,tree,target_spe)

def Scan_pwm(region_file, rescan, pwm, cutoff, target_spe, tree_file, output_file):
    """report tfbs count using pwm"""
    out = WriteToFile(output_file)
    if rescan:
        region_list = RescanRegion(region_file, pwm, cutoff, args.win, target_spe)
    else:
        region_list = LoadRegion(region_file,args.thres,args.threscol,args.win,args.summit)
    tree = LoadTree(tree_file)
    # load maf index
    maf_index = LoadMafIndex(target_spe)
    # search tbs
    print >>out, "pos" + '\t' + '\t'.join([name for name in tree.get_leaf_names()])
    num = 1
    for peak in region_list:
        if num % 1000 == 0:
            logging("Process: %d peak done" % (num))
        num += 1
        idx = maf_index[peak.chrom]
        maf_result = idx.search([peak.start],[peak.stop])
        motif_list = Scan_pwm_from_maf(maf_result,peak.start,peak.stop,pwm,cutoff,target_spe,tree)
        if len(motif_list['pos']) > 0 and motif_list['count'][target_spe] > 0:
            print >>out, ','.join(motif_list['pos']) + '\t' + '\t'.join(str(motif_list['count'][name]) for name in tree.get_leaf_names())

def ReportOptions():
    text = "### TFBS_Scan_in_peak version: beta.20150728\n"
    if args.maf is not None:
        text += "# maf folder path: %s\n" % (args.maf)
    else:
        text += "# maf folder path: %s\n" % (maf_path)
    if args.rescan:
        text += "# search all the binding sites within regions\n"
    text += "# peak region file: %s\n" % (args.region)
    if args.summit:
        text += "# the 10th column is summit: True\n"
    if args.thres is not None:
        text += "# peak threshold: %d\n" % (args.thres)
        if args.threscol is not None:
            text += "# peak threshold column: %d\n" % (args.threscol)
    if args.win is not None:
        text += "# extension size from peak center: %dbp\n" % (args.win)
    if args.pwm is not None:
        text += "## motif scan method: pwm\n"
        text += "# motif pwm file: %s\n" % (args.pwm)
        text += "# motif format: %s\n" % (args.motifformat)
        if args.background is not None:
            text += "# motif background freq file: %s\n" % (args.background)
        text += "# motif id: %s\n" % (args.motifid)
        text += "# log-odds score cutoff: %f\n" % (args.cutoff)
    if args.kmer is not None:
        text += "## motif scan method: kmer\n"
        text += "# motif kmer file: %s\n" % (args.kmer)
        if args.rc is True:
            text += "# use both kmer and reverse complement as match: True\n"
        else:
            text += "# use both kmer and reverse complement as match: False\n"
    text += "# target species: %s\n" % (args.spe)
    text += "# phylogenetic tree file: %s\n" % (args.tree)
    text += "# output file name: %s\n" % (args.output)
    print >>sys.stderr, text

def Main():
    global args
    args=ParseArg()
    if args.maf is not None:
        maf_path = args.maf
        global maf_path
    ReportOptions()
    if args.pwm is not None and args.kmer is not None:
        error("'--pwm' and '--kmer' are mutually exclusive")
        exit(1)
    if args.pwm is not None:
        motif = LoadPWM(args.pwm, args.motifformat, args.motifid, args.background)
        Scan_pwm(args.region, args.rescan, motif, args.cutoff, args.spe, args.tree, args.output)
    elif args.kmer is not None:
        motif = LoadKmer(args.kmer,args.rc)
        Scan_kmer(args.region,motif,args.spe,args.tree,args.output)
    else:
        error("either '--pwm' or '--kmer' should be set")
        exit(1)
    
if __name__=="__main__":
    Main()
