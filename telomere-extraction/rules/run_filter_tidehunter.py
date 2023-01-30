rule filter_tidehunter:
    input:
        tidehunter_out=rules.run_tidehunter.output.tidehunter,
        fastq=rules.concatenate_fastq.output.concatenated
    output:
        filtered=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_filtered_tidehunter.fastq.gz"
    params:
        telomere=config["TELOMERE"]
    shell:
        """
        python3 \
        scripts/filter_tidehunter.py \
        --tidehunter_out {input.tidehunter_out} \
        --fastq_file {input.fastq} \
        --sequence_of_interest {params.telomere} \
        --filtered_out {output.filtered}
        """
