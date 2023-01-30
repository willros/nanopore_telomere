rule run_porechop_telomeres:
    input:
        fastq=rules.run_extract_telomere_from_fastq.output.telomeres
    output:
        chopped=f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres_porechop.fastq.gz",
        log=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_porechop_telomeres_stats.txt",
    params:
        porechop=config["PORECHOP"],
        adapter_file=config["ADAPTER_FILE"]
    shell:
        """
        # copy the adapter file with the telotag to the porechop folder
        cp {params.adapter_file} {params.porechop}/porechop
        
        {params.porechop}/porechop-runner.py \
        -i {input.fastq} \
        --no_split \
        -o {output.chopped} \
        | tee {output.log}
        """
