#TELO_R_30
from pathlib import Path

configfile: "/home/nanopore/sequencing-analysis/automatisation/telomere-extraction/config.yaml"

OUT_DIR = config['OUT_DIR']
SAMPLE_DIR = config['SAMPLE_DIR']
ADAPTER = config["TEL_R_30"]
HG38 = config["HG38"]

# Exclude the control experiments (named Lambda) and other directories in the default folder
# Including TagTelo3_221206
BLACK_LIST = [
        "intermediate",
        "pings",
        "queued_reads",
        "user_scripts",
        "core-dump-db",
        "persistence",
        "reads",
        "2022-11-17_Lambda_test",
        "PolyA_2022-11-23",
        "TagTelo3_221206",

]

SAMPLE_NAMES = [
        x.stem for x in Path(SAMPLE_DIR).iterdir() 
        if x.is_dir() 
        and x.stem not in BLACK_LIST
        and not x.stem.startswith(".")
]

REFERENCE = config["REFERENCE"]

# rules are imported in cronological order 
include: "rules/concatenate_fastq.py"
include: "rules/seqkit_raw_stats.py"
include: "rules/seqkit_extract_telotag.py"
include: "rules/run_porechop_raw.py"
include: "rules/run_wf_alignment_raw.py"
include: "rules/run_tidehunter_raw.py"
include: "rules/run_extract_telomere_from_tidehunter.py"
include: "rules/run_extract_telomeres_from_fastq.py"
include: "rules/run_seqkit_stats_telomeres.py"
include: "rules/run_porechop_telomeres.py"
include: "rules/run_minimap_bedtools_telomeres_raw.py"
include: "rules/run_telomeres_from_bed_file.py"

# new rules for removing telomere sequence from the reads
#include: "rules/run_remove_telomeres_from_read.py"
include: "rules/run_minimap_bedtools_all_reads.py"

# hg38
include: "rules/run_minimap_bedtools_all_reads_hg38.py"

rule all:
    input:
        # concatenate_fastq.py
        expand(f"{SAMPLE_DIR}/{{sample}}/merged_fastq/{{sample}}_merged.fastq.gz", sample=SAMPLE_NAMES),
        
        # seqkit_raw_stats.py
        expand(f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_raw.tsv", sample=SAMPLE_NAMES),
        
        # seqkit_extract_telotag.py
        # Changed mismath (-m) to 3
        # Use ADAPTER for the telotag param
        expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_telotag.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_porechop_raw
        # Change adapter in the adapter.py file
        # Removing --no_split
        expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_raw_porechop.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_wf_alignment_raw.py
        #expand(f"{OUT_DIR}/{{sample}}/raw_report/{{sample}}_raw_wf-alignment-report.html", sample=SAMPLE_NAMES),
        
        # run_tidehunter_raw.py
        expand(f"{OUT_DIR}/{{sample}}/tidehunter/{{sample}}_raw_tidehunter.out", sample=SAMPLE_NAMES),
        
        # run_extract_telomeres_from_tidehunter.py
        expand(f"{OUT_DIR}/{{sample}}/tidehunter/left_telomeres.csv", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/tidehunter/right_telomere.csv", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/tidehunter/telomere_ids.txt", sample=SAMPLE_NAMES),
        
        # run_extract_telomeres_from_fastq.py
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_seqkit_stats_telomeres.py
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomere_stats.tsv", sample=SAMPLE_NAMES),
        
        # run_porechop_telomeres.py
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres_porechop.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_minimap_bedtools_telomeres_raw.py
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres_raw.bam", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_telomeres_raw.bed", sample=SAMPLE_NAMES),
        
        # run_telomeres_from_bed_file.py
        expand(f"{OUT_DIR}/{{sample}}/results/{{sample}}_telomere_results.csv", sample=SAMPLE_NAMES),
        
        
        # Perhaps this is not needed if I use more lenient parameters in filtering mapped reads from minimap
        # new rules
        # run_remove_telomeres_from_read.py
        #expand(f"{OUT_DIR}/{{sample}}/telomeres/{{sample}}_removed_telomeres.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_minimap_bedtools_all_reads.py
        # Q value > 15
        expand(f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_all_reads.bam", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_all_reads.bed", sample=SAMPLE_NAMES),
       
        # run_minimap_bedtools_all_reads_hg38.py
        # aligning to hg38
        # Q value > 15
        #expand(f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_hg38_all_reads.bam", sample=SAMPLE_NAMES),
        #expand(f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_hg38_all_reads.bed", sample=SAMPLE_NAMES),
    
    
