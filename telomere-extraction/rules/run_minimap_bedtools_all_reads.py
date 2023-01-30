rule run_minimap_bedtools_all_reads:
    input:
        fastq=rules.run_porechop_raw.output.chopped
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
        samtools view -h -F 4 -F 2048 -F 256 -q 5 | samtools sort -o {output.bam}
        
        # bedtools
        samtools index {output.bam}
        
        bedtools bamtobed -i {output.bam} > {output.bed}
        """
        
# changed -q to 5