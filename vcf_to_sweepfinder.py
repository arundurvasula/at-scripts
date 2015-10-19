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

with open(vcf_in,'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    sweep_out = csv.writer(open(sample_name+".sf.txt", 'w'), delimiter='\t', lineterminator="\n")
#    sweep_out = open(sample_name+".sf.txt", 'w')
    sweep_out.writerow(["position","x","n","folded"])
    for line in tsvin:
        if line[0] == "1":
            position = line[1]
            x = line[7].split(";")[0].split("=")[1]
            if "," in x:
                x=x.count(",")
            n = line[7].split(";")[1].split("=")[1]
            folded = 0
            sweep_out.writerow([position,x,n,folded])
