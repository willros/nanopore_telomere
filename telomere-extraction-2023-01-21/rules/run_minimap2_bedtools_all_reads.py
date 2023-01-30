rule run_minimap2_bedtools_all_reads:
    input:
        fastq=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_raw_porechop.fastq.gz"
    output:
        bam=f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_all_reads.bam",
        bed=f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_all_reads.bed"
    params:
        reference=config["REFERENCE"]
    message:
        """
        Mapping chopped raw reads from the whole run with minimap2 and extract regions with bedtools
        """
    shell:
        """
        minimap2 -ax map-ont -Y {params.reference} {input.fastq} | \
        samtools view -h -F 4 -F 2048 -F 256 | samtools sort -o {output.bam}
        
        # bedtools
        samtools index {output.bam}
        
        bedtools bamtobed -i {output.bam} > {output.bed}
        """
        
# removing the q entirely (all reads that align are kept)