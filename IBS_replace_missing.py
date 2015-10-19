#!/usr/bin/python
# usage: python IBS_replace_missing.py <pop.popdata> <mask1> [mask2] ... [maskN]
# where N=number of individuals in the popdata file
# supplied masks must be in the same order as the haplotypes in the popdata file
# this script will take a lot of memory (loads each mask into memory, each mask is ~100 Mb)
import sys
import csv

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

popdata = open(sys.argv[1], 'rb')
try:
    reader = csv.reader(popdata, delimiter="\t")
    writer = csv.writer(open(sys.argv[1]+"_missing_fixed.popdata", "wb"), delimiter="\t")
    mask_list = []
    for maskfile in sys.argv[2:]:
        mask_list.append(read_fasta(maskfile))
    for row in reader:
        chr = row[0]
        pos = row[1]
        ref = row[2]
        hap = row[3]

        if "." in hap:
            mask_val="NA"
            list_of_haps = list(hap)
            mask_to_check = list_of_haps.index('.')
            try:
                mask_val = mask_list[mask_to_check]['Chr'+chr][0][int(pos)-1]
            except IndexError:
                print "IndexError when assigning mask_val. Position may not exist in mask.\n\t-> Chrom: "+chr+ " Pos: "+pos+" mask: "+sys.argv[2+mask_to_check]+"\n\t-> Assigning N to that position."
                list_of_haps[mask_to_check] = "N"
                hap="".join(list_of_haps)

            if mask_val == "0": #replace with N
                list_of_haps[mask_to_check] = "N"
                hap="".join(list_of_haps)
            if mask_val == "1": #replace with ref
                list_of_haps[mask_to_check] = ref
                hap="".join(list_of_haps)

        writer.writerow([chr, pos, ref, hap])
finally:
    popdata.close()


#test = read_fasta("/Users/arundurvasula/Documents/Science/AtCanary/MoroccanVCFs/MA-40632.27150_CTTGTA_C71EHANXX_3_20150612B_20150612.bam.mpileup.mask.txt")
#print test['Chr1'][0][0] #gives first character of chromosome 1
