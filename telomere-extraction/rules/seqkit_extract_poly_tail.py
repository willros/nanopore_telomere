rule seqkit_extract_poly_tail:
    input:
        fastq=rules.concatenate_fastq.output.concatenated
    output:
        A_tail_stats=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_A_tail.tsv",
        T_tail_stats=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_T_tail.tsv",
        both=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_A_and_T_tail.fastq.gz",
        both_stats=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_A_and_T_tail.tsv",
        duplication_log=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_duplicated.txt",
        duplicated_reads=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_duplicated.fastq.gz",
    params:
        A_tail=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_A_tail.fastq.gz",
        T_tail=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_T_tail.fastq.gz",
    message:
        """
        Extracting A and T tail from fastq
        """
    shell:
        """
        # T-tail
        seqkit grep -s -R 1:100 -r -p TTTTTTTTTT {input.fastq} > {params.T_tail}

        # A-tail
        seqkit grep -s -R -100:-1 -r -p AAAAAAAAAA {input.fastq} > {params.A_tail}

        # Statistics
        seqkit stats {params.T_tail} -T > {output.T_tail_stats}
        seqkit stats {params.A_tail} -T > {output.A_tail_stats}

        # Merge fastq with tails and remove duplicates from the concatenated file
        cat {params.T_tail} {params.A_tail} | seqkit rmdup --by-name -o {output.both} --dup-num-file {output.duplication_log} --dup-seqs-file {output.duplicated_reads}

        # Statistics on the merged file
        seqkit stats {output.both} -T > {output.both_stats}

        # Remove T and A tail
        rm {params.T_tail} {params.A_tail}
        """
        