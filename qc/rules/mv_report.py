from pathlib import Path

def summary_file(wildcards):
    in_path = Path(f"{SAMPLE_DIR}/{wildcards.sample}")
    summary_file = [x for x in in_path.rglob("*.html")][0]
    return summary_file
rule mv_report:
    input:
        summary_file=summary_file
    output:
        report=f"{OUT_DIR}/{{sample}}/raw_report/minknow-sequencing_report.html"
    shell:
        """
        cp {input.summary_file} {output.report}
        """
