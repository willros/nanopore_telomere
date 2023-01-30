rule seqkit_raw_stats:
    input:
        fastq=rules.concatenate_fastq.output.concatenated
    output:
        raw_stats=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_raw.tsv"
    params:
        threads=5
    message:
        """
        Running seqkit stats on the raw file {input.fastq}
        """
    shell:
        """
        seqkit stats -a --threads {params.threads} {input.fastq} -T > {output.raw_stats}
        """



