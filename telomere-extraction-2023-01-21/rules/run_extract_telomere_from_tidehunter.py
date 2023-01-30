rule run_extract_telomere_from_tidehunter:
    input:
        tidehunter=rules.run_tidehunter.output.tidehunter
    output:
        left_telomere=f"{OUT_DIR}/{{sample}}/tidehunter/left_telomeres.csv",
        right_telomere=f"{OUT_DIR}/{{sample}}/tidehunter/right_telomere.csv",
        telomere_ids=f"{OUT_DIR}/{{sample}}/tidehunter/telomere_ids.txt",
    message: 
        """
        Extracting telomeres from Tidehunter
        """
    shell:
        """
        python3 \
        scripts/extract_telomere_from_tidehunter.py \
        --tidehunter {input.tidehunter} \
        --left_telomere_file {output.left_telomere} \
        --right_telomere_file {output.right_telomere} \
        --telomere_ids {output.telomere_ids}
        """