import pathlib

configfile: "/home/nanopore/sequencing-analysis/automatisation/basecalling/config.yaml"

MODEL = config['GUPPY_MODEL']

SAMPLE_DIR = pathlib.Path(config['SAMPLE_DIR'])

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
SAMPLE_NAMES = [x.stem for x in Path(SAMPLE_DIR).iterdir() if x.is_dir() 
                and x.stem not in BLACK_LIST
                and not x.stem.startswith(".")]

OUT_DIR = pathlib.Path(config['OUT_DIR'])

# rules are imported in cronological order 
include: "rules/run_guppy.py"

rule all:
    input:
        expand(f"{OUT_DIR}/{{sample}}/{MODEL}/{{sample}}_model.txt", sample=SAMPLE_NAMES)