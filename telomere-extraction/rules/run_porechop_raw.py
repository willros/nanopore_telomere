rule run_porechop_raw:
    input:
        fastq=rules.concatenate_fastq.output.concatenated
    output:
        chopped=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_raw_porechop.fastq.gz",
        log=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_raw_porechop_stats.txt",
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
        # Removing --no_split and see what the difference is
        # --no_split \
        
