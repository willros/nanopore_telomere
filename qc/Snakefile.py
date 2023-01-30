from pathlib import Path

configfile: "/home/nanopore/sequencing-analysis/automatisation/qc/config.yaml"

OUT_DIR = config['OUT_DIR']
SAMPLE_DIR = config['SAMPLE_DIR']

# Exclude the control experiments (named Lambda) and other directories in the default folder
BLACK_LIST = [
        "intermediate",
        "pings",
        "queued_reads",
        "user_scripts",
        "core-dump-db",
        "persistence",
        "reads",
        "2022-11-17_Lambda_test",
]

SAMPLE_NAMES = [
        x.stem for x in Path(SAMPLE_DIR).iterdir() 
        if x.is_dir() 
        and x.stem not in BLACK_LIST
        and not x.stem.startswith(".")
]

REFERENCE = config["REFERENCE"]

# rules are imported in cronological order 
#include: "rules/mv_report.py"
include: "rules/run_nanoplot.py"
include: "rules/run_wf-alignment.py"

rule all:
    input:
        #expand(f"{OUT_DIR}/{{sample}}/raw_report/minknow-sequencing_report.html", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/raw_report/NanoPlot-report.html", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/raw_report/wf-alignment-report.html", sample=SAMPLE_NAMES)
        
