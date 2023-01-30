rule run_calculate_telomere_length:
    input:
        bed=rules.run_minimap_bedtools.output.bed,
        start=config["TELOMERE_START_FILE"]
    params:
        cov=config["COVERAGE"] 
    output:
        csv=f"{OUT_DIR}/{{sample}}/final_results/{{sample}}_telomere_lengths.csv"
    message: 
        """
        Calculating telomere lengths
        """
    shell:
        """
        python3 \
        scripts/calculate_telomere_length.py \
        --telomere_starts {input.start} \
        --bed_file {input.bed} \
        --coverage {params.cov} \
        --out_file {output.csv}
        """