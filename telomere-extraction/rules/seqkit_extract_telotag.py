rule seqkit_extract_telotag:
    input:
        fastq=rules.concatenate_fastq.output.concatenated
    output:
        telotag_stats=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_telotag.tsv",
        telotag=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_telotag.fastq.gz",
    params:
        telotag=ADAPTER,
        threads=5
    message:
        """
        Extracting reads with adapter: {ADAPTER}
        """
    shell:
        """
        # Extract telotag
        seqkit grep --threads {params.threads} -s -R 1:200 -p {params.telotag} -m 3 {input.fastq} -o {output.telotag}

        # Statistics on the telotag file
        seqkit stats --threads {params.threads} {output.telotag} -T > {output.telotag_stats}
        """
