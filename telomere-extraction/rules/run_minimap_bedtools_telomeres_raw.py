rule run_minimap_bedtools_telomeres_raw:
    input:
        fastq=rules.run_porechop_telomeres.output.chopped
    output:
        bam=f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres_raw.bam",
        bed=f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres_raw.bed"
    params:
        reference=config["REFERENCE"]
    message:
        """
        Mapping chopped raw telomeres with minimap2 and extract regions with bedtools
        """
    # Removed the quality score filtering. Dont know how to feel about that??
    shell:
        """
        minimap2 -ax map-ont -Y {params.reference} {input.fastq} | \
        samtools view -h -F 4 | samtools sort -o {output.bam}
        
        # bedtools
        samtools index {output.bam}
        
        bedtools bamtobed -i {output.bam} > {output.bed}
        """
        
#### TRYING TO REMOVE: ####
#-F 2048 -F 256
# -F 2048 -F 256
# skip supplementary alignment and non primary alignment
# -F 4 : skip unaligned reads
# -h : include header

# -q x
# changed to 15
# skip alignment under x quality score 

# -Y
# In SAM output, use soft clipping for supplementary alignments.