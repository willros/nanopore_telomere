rule run_tail_lengths:
    input:
        fastq=rules.concatenate_fastq.output.concatenated
    params:
        plots_folder=f"{OUT_DIR}/{{sample}}/read_statistics/"
    output:
        csv=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_tails.csv"
    message: 
        """
        Generating plots and statistics of tail lengths
        """
    shell:
        """
        python3 \
        scripts/tail_length.py \
        --fastq {input.fastq} \
        --out_file {output.csv} \
        --out_plots_path {params.plots_folder}
        """