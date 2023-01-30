def fastq_pass_files(wildcards):
    in_folder = Path(f"{SAMPLE_DIR}/{wildcards.sample}")
    return list(in_folder.rglob("*fastq_pass"))[0]

rule wf_alignment:
    input:
        # the workflow needs input folder which ONLY contains fastq files
        in_folder=fastq_pass_files
    output:
        report=f"{OUT_DIR}/{{sample}}/raw_report/wf-alignment-report.html"
    params:
        outdir=f"{OUT_DIR}//{{sample}}/wf-alignment",
        reference=f"{REFERENCE}"
    shell:
        """
        nextflow run epi2me-labs/wf-alignment \
        --fastq {input.in_folder} \
        --references {params.reference} \
        --concat_fastq false \
        --threads 4 \
        --out_dir {params.outdir} && \
        mv {params.outdir}/wf-alignment-report.html {output.report}
        """
