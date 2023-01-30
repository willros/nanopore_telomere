# PolyA-tail_telotag
from pathlib import Path

configfile: "/home/nanopore/sequencing-analysis/automatisation/telomere-extraction/config.yaml"

OUT_DIR = config['OUT_DIR']
SAMPLE_DIR = config['SAMPLE_DIR']
ADAPTER = config["TELO_TAG_5"]

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
        "TagTelo3_221206",
        "TeloR30",
        
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
include: "rules/seqkit_extract_poly_tail.py"
include: "rules/run_tail_lengths.py"
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

# all reads aligment
include: "rules/run_minimap_bedtools_all_reads.py"

#include: "rules/run_filter_tidehunter.py"
#include: "rules/run_porechop.py"
#include: "rules/run_minimap_bedtools.py"
#include: "rules/run_calculate_telomere_length.py"

rule all:
    input:
        # concatenate_fastq.py
        expand(f"{SAMPLE_DIR}/{{sample}}/merged_fastq/{{sample}}_merged.fastq.gz", sample=SAMPLE_NAMES),
        
        # seqkit_raw_stats.py
        expand(f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_raw.tsv", sample=SAMPLE_NAMES),
        
        # seqkit_extract_poly_tail.py
        # PROBABLY DROP THIS LATER
        expand(f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_A_tail.tsv", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_T_tail.tsv", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_A_and_T_tail.fastq.gz", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_A_and_T_tail.tsv", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_duplicated.txt", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_duplicated.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_tail_lengths.py
        expand(f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_tails.csv", sample=SAMPLE_NAMES),
        
        # seqkit_extract_telotag.py
        expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_telotag.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_porechop_raw
        expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_raw_porechop.fastq.gz", sample=SAMPLE_NAMES),
        
        # run_wf_alignment_raw.py
        ##### DO NOT RUN THIS!! #####
        #expand(f"{OUT_DIR}/{{sample}}/raw_report/{{sample}}_raw_wf-alignment-report.html", sample=SAMPLE_NAMES),
        
        # run_tidehunter.py
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
        
        # run_minimap_bedtools_all_reads.py
        # Q value > 5
        expand(f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_all_reads.bam", sample=SAMPLE_NAMES),
        expand(f"{OUT_DIR}/{{sample}}/all_reads_aligned/{{sample}}_all_reads.bed", sample=SAMPLE_NAMES),
       
    
    
    
    
    
    
    
        # old stuff
        # filter tidehunter
        #expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_filtered_tidehunter.fastq.gz", sample=SAMPLE_NAMES),

        # PORECHOP (Now running on the tidehunter filtered file)
        #expand(f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_porechop.fastq.gz", sample=SAMPLE_NAMES),
        
        # Minimap and bedtools (input from porechop)
        #expand(f"{OUT_DIR}/{{sample}}/aligned/{{sample}}_bam.bam", sample=SAMPLE_NAMES),
        
        # Calulcate telomere length
        #expand(f"{OUT_DIR}/{{sample}}/final_results/{{sample}}_telomere_lengths.csv", sample=SAMPLE_NAMES)
