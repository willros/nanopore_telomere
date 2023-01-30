rule run_tidehunter_raw:
    input:
        fastq=rules.concatenate_fastq.output.concatenated
    output:
        tidehunter=f"{OUT_DIR}/{{sample}}/tidehunter/{{sample}}_raw_tidehunter.out"
    params:
        tidehunter=config["TIDEHUNTER"]
    shell:
        """
        {params.tidehunter} -f 2 {input.fastq} > {output.tidehunter}
        """