rule run_minimap_bedtools_all_reads_hg38:
    input:
        fastq=rules.run_porechop_raw.output.chopped
    output:
        bam=f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_hg38_all_reads.bam",
        bed=f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_hg38_all_reads.bed"
    params:
        reference=HG38
    message:
        """
        Mapping chopped raw reads from the whole run with minimap2 to hg38 and extract regions with bedtools
        """
    shell:
        """
        minimap2 -ax map-ont -Y {params.reference} {input.fastq} | \
        samtools view -h -F 4 256 -q 15 | samtools sort -o {output.bam}
        
        # bedtools
        samtools index {output.bam}
        
        bedtools bamtobed -i {output.bam} > {output.bed}
        """

# removing:
# -F 2048 -F256