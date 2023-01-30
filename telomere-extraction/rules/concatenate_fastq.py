from pathlib import Path

def get_fastq(wildcards):
    in_folder = Path(f"{SAMPLE_DIR}/{wildcards.sample}")
    fastq_files = [x for x in in_folder.rglob("fastq_pass/*fastq.gz")]
    if not fastq_files:
        fastq_files = [x for x in in_folder.rglob("pass/*fastq.gz")]
    return fastq_files

rule concatenate_fastq:
    input:
        fastq_files=get_fastq
    output:
        concatenated=f"{SAMPLE_DIR}/{{sample}}/merged_fastq/{{sample}}_merged.fastq.gz"
    message:
        """
        Concatenating fastq files: {input.fastq_files}
        """
    shell:
        """
        cat {input.fastq_files} > {output.concatenated}
        """
    

