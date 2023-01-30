rule run_tidehunter:
    input:
        fastq=rules.run_porechop_raw.output.chopped
    output:
        tidehunter=f"{OUT_DIR}/{{sample}}/tidehunter/{{sample}}_raw_tidehunter.out"
    params:
        tidehunter=config["TIDEHUNTER"]
    shell:
        """
        {params.tidehunter} -f 2 {input.fastq} > {output.tidehunter}
        """