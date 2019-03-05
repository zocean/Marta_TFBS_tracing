#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 02 Aug 2017 22:15:03

import os,sys,argparse
import tabix

def parse_arg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('--input',type=str,dest="input",help="input file")
    p.add_argument('--bedlist',type=str,dest="bedlist",nargs="+",help="list of region file in bed format")
    p.add_argument('--labellist',type=str,dest="labellist",nargs="+",help="list of label")
    p.add_argument('--folder',type=str,dest="folder",help="output folder")
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

def create_tabix(filename):
    tabix_file = filename + '.gz'
    tabix_index_file = tabix_file + '.tbi'
    if not os.path.isfile(tabix_file) or not os.path.isfile(tabix_index_file):
        os.system("sort -k1,1 -k2,2n %s >%s" % (filename, filename+'.sort'))
        os.system("mv %s %s" % (filename+'.sort', filename))
        os.system("bgzip -c %s >%s" % (filename, tabix_file))
        os.system("tabix -p bed %s" % (tabix_file))

def intersect_region(region_file, label, dbi_file, output_folder):
    '''
    intersect dbi with region file (bed format) and write final file in the output folder
    '''
    fin = open(region_file, 'r')
    out_file = os.path.join(output_folder, label+'.bed')
    fout = open(out_file, 'w')
    try:
        dbi = tabix.open(dbi_file)
    except:
        print >>sys.stderr, "Can't load tabix file %s"% (dbi_file)
        exit(1)
    for line in fin:
        if line.strip().startswith('#') or line.strip() == '':
            continue
        row = line.strip().split()
        chrom = row[0]
        start = int(row[1])
        stop = int(row[2])
        result = dbi.query(chrom, start, stop)
        for x in result:
            print >>fout, '\t'.join(x)
    fin.close()
    fout.close()
    create_tabix(out_file)

def main():
    global args
    args = parse_arg()
    # check whether tabix file is existed
    create_tabix(args.input)
    # 
    assert len(args.bedlist) == len(args.labellist)
    for nn in range(len(args.bedlist)):
        region_file = args.bedlist[nn]
        label = args.labellist[nn]
        intersect_region(region_file, label, args.input+'.gz', args.folder)
 
if __name__=="__main__":
    main()
