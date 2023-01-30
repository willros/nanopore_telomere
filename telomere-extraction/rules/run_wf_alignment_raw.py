from pathlib import Path

def fast5_pass_files(wildcards):
    in_folder = Path(f"{SAMPLE_DIR}/{wildcards.sample}")
    fastq_folder = list(in_folder.rglob("*fastq_pass"))
    if fastq_folder:
        return fastq_folder[0]
    else:
        return list(in_folder.rglob("*pass"))[0]
    
rule run_wf_alignment_raw:
    input:
        in_folder=rules.run_porechop_raw.output.chopped
    output:
        report=f"{OUT_DIR}/{{sample}}/raw_report/{{sample}}_raw_wf-alignment-report.html"
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
        --out_dir {params.outdir} 
        mv {params.outdir}/wf-alignment-report.html {output.report}
        rm -rf {params.outdir}
        """