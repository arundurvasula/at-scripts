# this script will change genotypes to diploid (1 -> 1|1)
# and will check masks for filling in missing data 
# usage python vcf_haploid file.vcf [masks.txt]
# masks should be in same order as vcf file samples
import sys
import csv
import argparse


parser = argparse.ArgumentParser(description="fills in missing genotype information in a merged haploid vcf")
parser.add_argument("-v", "--vcf", action="store", required=True, help="Input VCF file. Should be a merged vcf with haploid calls (i.e. vcf-merge 1.vcf 2.vcf > 1.2.vcf)")
parser.add_argument("-m", "--mask", action="store", required=True, help="A file containing paths to mask files. Mask files should come from Andrea's pipeline or Shore. Needs to be in the same order as the vcf samples. Will not produce an error if these are mismatched so you should check.")
parser.add_argument("-d", "--diploid", action="store_true", help="If set, will output genotypes as 1|1 instead of 1")

args = parser.parse_args()

try:
    #vcf_in = open(sys.argv[1])
#    vcf_in = sys.argv[1]
    vcf_in = args.vcf
except IOError:
    print "Sample not found!"
    sys.exit(1)
except IndexError:
    print "Need to supply a sample!"
    sys.exit(1)

sample_name = vcf_in.split("/")[-1]+".diploid.vcf"
#num_samples = len(sys.argv[2:])
def read_fasta(filename):
    fasta = {}
    with open(filename) as file_one:
        for line in file_one:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                active_sequence_name = line[1:]
                if active_sequence_name not in fasta:
                    fasta[active_sequence_name] = []
                    continue
            sequence = line
            fasta[active_sequence_name].append(sequence)
    return fasta

mask_list = []
with open(args.mask) as f:
    m = f.read().splitlines()
    for mask in m:
        mask_list.append(read_fasta(mask))
num_samples = len(mask_list)
#for maskfile in sys.argv[2:]:
#    mask_list.append(read_fasta(maskfile))

with open(vcf_in,'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    vcf_out = csv.writer(open(sample_name, 'w'), delimiter='\t', lineterminator="\n")
    
    for row in tsvin:
        if any('##' in strings for strings in row):
            continue
        if any('#CHROM' in strings for strings in row):
            print row
            vcf_out.writerow(row)
            continue
        
        chrom,pos,id,ref,alt,qual,filter,info,format=row[0:9]
        out = [chrom,pos,id,ref,alt,qual,filter,info,format]
        haplotypes = row[9:]
        if "." in haplotypes:
            for mask_to_check,call in enumerate(haplotypes):
                mask_val="NA"
                try:
                    mask_val = mask_list[mask_to_check]['Chr'+chrom][0][int(pos)-1]
                except IndexError:
                    mask_val = "0"
                if mask_val == "1" and call ==".":
                    out.append("0|0")
                elif call == "1":
                    out.append("1|1")
                elif call == "2":
                    out.append("2|2")
                elif call == "3":
                    out.append("3|3")
                elif mask_val == "0" and call == ".":
                    out.append(".|.")
        elif "." not in haplotypes:
            for hap in haplotypes:
                out.append("1|1")
        if len(out) == 9+num_samples:
            vcf_out.writerow(out)
        else:
            print "Wrong number of genotypes: "+ " ".join(out)
            sys.exit(0)
