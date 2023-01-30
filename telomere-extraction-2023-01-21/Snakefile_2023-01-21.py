# Workflow from 2023-01-23. Reads basecalled with Dorado

from pathlib import Path

configfile: "/home/nanopore/sequencing-analysis/automatisation/telomere-extraction-2023-01-21/config-2023-01-21.yaml"

OUT_DIR = config['OUT_DIR']
SAMPLE_DIR = config['SAMPLE_DIR']

# Exclude the control experiments (named Lambda) and other directories in the default folder
# Start with only looking at TelR30_longer_time_230116
BLACK_LIST = [
        "intermediate",
        "pings",
        "queued_reads",
        "user_scripts",
        "core-dump-db",
        "persistence",
        "reads",
        "2022-11-17_Lambda_test",
        #"PolyA_2022-11-23",
        #"TeloR30",
        #"TagTelo3_221206",
]

SAMPLE_NAMES = [
        x.stem for x in Path(SAMPLE_DIR).iterdir() 
        if x.is_dir() 
        and x.stem not in BLACK_LIST
        and not x.stem.startswith(".")
]

REFERENCE = config["REFERENCE"]

# rules are imported in cronological order 
include: "rules/run_porechop_raw.py"
include: "rules/run_minimap2_bedtools_all_reads.py"
include: "rules/run_tidehunter.py"
include: "rules/run_extract_telomere_from_tidehunter.py"
include: "rules/run_extract_telomeres_from_fastq.py"
include: "rules/run_seqkit_stats_telomeres.py"
include: "rules/run_minimap_bedtools_telomeres_raw.py"
include: "rules/run_telomeres_from_bed_file.py"

# Workflow
rule all:
    input:
        # run_porechop_raw.py
        expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_raw_porechop.fastq.gz", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_raw_porechop_stats.txt", sample=SAMPLE_NAMES),
        
        # run_minimap2_bedtools_all_reads.py
        # no Q value filtering, extract all reads that aligned
        expand(f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_all_reads.bam", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_all_reads.bed", sample=SAMPLE_NAMES),
        
        # run_tidehunter.py
        expand(f"{OUT_DIR}/{{sample}}/tidehunter/{{sample}}_raw_tidehunter.out", sample=SAMPLE_NAMES),
        
        # run_extract_telomeres_from_tidehunter.py
        expand(f"{OUT_DIR}/{{sample}}/tidehunter/left_telomeres.csv", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/tidehunter/right_telomere.csv", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/tidehunter/telomere_ids.txt", sample=SAMPLE_NAMES),
        
        # run_extract_telomeres_from_fastq.py
        # using the filtered porechop fastq file
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_seqkit_stats_telomeres.py
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomere_stats.tsv", sample=SAMPLE_NAMES),
        
        # run_minimap_bedtools_telomeres_raw.py
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres_raw.bam", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres_raw.bed", sample=SAMPLE_NAMES),
        
        # run_telomeres_from_bed_file.py
        expand(f"{OUT_DIR}/{{sample}}/results/{{sample}}_telomere_results.csv", sample=SAMPLE_NAMES),
