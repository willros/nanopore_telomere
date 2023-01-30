rule run_seqkit_stats_telomeres:
    input:
        fastq=rules.run_extract_telomere_from_fastq.output.telomeres
    output:
        telomere_stats=f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomere_stats.tsv"
    message:
        """
        Running seqkit stats on the telomere file {input.fastq}
        """
    shell:
        """
        seqkit stats -a --threads 10 {input.fastq} -T > {output.telomere_stats}
        """


