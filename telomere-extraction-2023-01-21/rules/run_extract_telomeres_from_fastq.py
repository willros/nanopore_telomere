rule run_extract_telomere_from_fastq:
    input:
        ids=rules.run_extract_telomere_from_tidehunter.output.telomere_ids,
        fastq=rules.run_porechop_raw.output.chopped
    output:
        telomeres=f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres.fastq.gz",
    message: 
        """
        Extracting telomeric reads from filtered porechop fastq file
        """
    shell:
        """
        seqkit grep --threads 10 -f {input.ids} {input.fastq} -o {output.telomeres}
        """