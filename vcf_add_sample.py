#!/usr/bin/python
# should be python 2
# usage: python vcf_add_sample.py <sample.vcf> 
# use to add the FORMAT column and sample to single sample VCFs from Andrea
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

sample_name = vcf_in.split("/")[-1]+"samp.vcf"

with open(vcf_in,'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    vcf_out = csv.writer(open(sample_name, 'w'), delimiter='\t', lineterminator="\n")
    
    vcf_out.writerow(["#CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT",sample_name])
    next(tsvin)
    for row in tsvin:
        row.append("GT")
        row.append("1")
        vcf_out.writerow(row)
