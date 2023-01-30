rule run_telomeres_from_bed_file:
    input:
        left_telomere=rules.run_extract_telomere_from_tidehunter.output.left_telomere,
        right_telomere=rules.run_extract_telomere_from_tidehunter.output.right_telomere,
        bed=rules.run_minimap_bedtools_telomeres_raw.output.bed,
    output:
        final_telomeres=f"{OUT_DIR}/{{sample}}/results/{{sample}}_telomere_results.csv"
    message: 
        """
        Filtering out telomeres from tidehunter file and bed file
        """
    shell:
        """
        python3 \
        scripts/telomeres_from_bed_file.py \
        --tidehunter_left {input.left_telomere} \
        --tidehunter_right {input.right_telomere} \
        --bedfile {input.bed} \
        --telomeres_out {output.final_telomeres}
        """