#!/bin/bash
# usage: vcf_zip.sh <sample.vcf>
set -e
set -u

SAMPLE_NAME=`basename "${1}"`
bgzip -c $1 > ${SAMPLE_NAME}.vcf.gz
tabix -p vcf ${SAMPLE_NAME}.vcf.gz