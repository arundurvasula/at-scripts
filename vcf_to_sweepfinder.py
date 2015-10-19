#!/usr/bin/python
# should be python 2
# usage: python vcf_to_sweepfinder.py <sample.vcf>
# use to create a sweepfinder format file from a multisample VCF. before this, you need:
# python vcf_add_sample.py t1.vcf; python vcf_add_sample.py t2.vcf; bgzip -c t1.vcf > t1.vcf.gz; tabix -p vcf t1.vcf.gz; #(same for t2); vcf-merge t1.vcf.gz t2.vcf.gz > all_t.vcf.gz; unzip all_t.vcf.gz; python vcf_to_sweepfinder.py all_t.vcf.gz
import sys
import csv

try:
    vcf_in = sys.argv[1]
except IndexError:
    print "Need to supply a sample!"
    sys.exit(1)

sample_name = vcf_in.split("/")[-1].split(".")[0]

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

with open(vcf_in,'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    sweep_out = csv.writer(open(sample_name+".sf.txt", 'w'), delimiter='\t', lineterminator="\n")
    sweep_out.writerow(["position","x","n","folded"])
    for line in tsvin:
        if line[0] == "1": #only do chromosome 1, change this later
            position = line[1]
            x = line[7].split(";")[1].split("=")[1] #the AN field
            n = x
            if "." in line[9:]: # if there's missing data in any genotype field
                genotypes = line[9:] # iterate over the genotypes
                    for idx, genotype in enumerate(genotypes):
                        if genotype == ".":
                            mask = read_fasta(sys.argv[2+idx]) #use sample index to find mask file (provided by input)
                            try:
                                mask_val = mask['Chr'+"1"][0][int(position)-1]
                            except IndexError:
                                print "IndexError when assigning mask_val. Position may not exist in mask. Assigning N to that position."
                            if mask_val == "1":
                                n = n + 1
                
            folded = 1
            sweep_out.writerow([position,x,n,folded])
