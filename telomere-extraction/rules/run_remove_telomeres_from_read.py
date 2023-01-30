rule run_remove_telomeres_from_read:
    input:
        left_telomere=rules.run_extract_telomere_from_tidehunter.output.left_telomere,
        right_telomere=rules.run_extract_telomere_from_tidehunter.output.right_telomere,
        fastq=rules.run_porechop_telomeres.output.chopped,
    output:
        filtered=f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_removed_telomeres.fastq.gz"
    message: 
        """
        Removing telomere sequences from reads
        """
    shell:
        """
        python3 \
        scripts/remove_telomeres_from_read.py \
        --fastq_file {input.fastq} \
        --tidehunter_left {input.left_telomere} \
        --tidehunter_right {input.right_telomere} \
        --filtered_file {output.filtered} 
        """