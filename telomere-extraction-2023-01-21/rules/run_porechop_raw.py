from pathlib import Path

def get_fastq(wildcards):
    in_folder = Path(f"{SAMPLE_DIR}/{wildcards.sample}")
    fastq_files = [x for x in in_folder.rglob("*.fastq")]
    return fastq_files

rule run_porechop_raw:
    input:
        fastq=get_fastq
    output:
        chopped=f"{OUT_DIR}/{{sample}}/filtered-fastq/{{sample}}_raw_porechop.fastq.gz",
        log=f"{OUT_DIR}/{{sample}}/read_statistics/{{sample}}_raw_porechop_stats.txt",
    params:
        porechop=config["PORECHOP"],
    message:
        """
        Running porechop on {input.fastq}
        """
    shell:
        """
        {params.porechop}/porechop-runner.py \
        -i {input.fastq} \
        -o {output.chopped} \
        | tee {output.log}
        """

# Porechop split the reads with internal adapters (chimeras)