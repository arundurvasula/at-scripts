# this script will change genotypes to diploid (1 -> 1|1)
# and will check masks for filling in missing data 
# usage python vcf_haploid file.vcf [masks.txt]
# masks should be in same order as vcf file samples
import sys
import csv

try:
    #vcf_in = open(sys.argv[1])
    vcf_in = sys.argv[1]
except IOError:
    print "Sample not found!"
    sys.exit(1)
except IndexError:
    print "Need to supply a sample!"
    sys.exit(1)

sample_name = vcf_in.split("/")[-1]+".diploid.vcf"

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
for  maskfile in sys.argv[2:]:
    mask_list.append(read_fasta(maskfile))

with open(vcf_in,'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    vcf_out = csv.writer(open(sample_name, 'w'), delimiter='\t', lineterminator="\n")
    
    for _ in xrange(7):
        next(tsvin)
    header=next(tsvin)
    vcf_out.writerow(header)
    for row in tsvin:
        chr,pos,id,ref,alt,qual,filter,info,format=row[0:9]
        out = [chr,pos,id,ref,alt,qual,filter,info,format]
        haplotypes = row[9:]
        if "." in haplotypes:
            for call in haplotypes:
                mask_val="NA"
                indices = [i for i, x in enumerate(haplotypes) if x == "."]
                if call == ".":
                    for mask_to_check in indices:
                        try:
                            mask_val = mask_list[mask_to_check]['Chr'+chr][0][int(pos)-1]
                        except IndexError:
                            out.append(".|.")
                        if mask_val == "0":
                            out.append(".|.")
                        elif mask_val == "1":
                            out.append("0|0")
                elif call == "1":
                    out.append("1|1")
                else:
                    out.append(".|.")

        vcf_out.writerow(out)
