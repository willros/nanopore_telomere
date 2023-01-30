from pathlib import Path

def get_summary(wildcards):
    in_folder = Path(f"{SAMPLE_DIR}/{wildcards.sample}")
    summary = [x for x in in_folder.rglob("sequencing_summary*.txt")][0]
    return summary


rule run_nanoplot:
    input:
        summary_file=get_summary
    output:
        out_file=f"{OUT_DIR}/{{sample}}/raw_report/NanoPlot-report.html"
    params:
        out_folder=f"{OUT_DIR}/{{sample}}/raw_report/nanoplot"
    shell:
        """
        NanoPlot --summary {input.summary_file} -o {params.out_folder}

        mv {params.out_folder}/NanoPlot-report.html {output.out_file} 

        rm -rf {params.out_folder}
        """


