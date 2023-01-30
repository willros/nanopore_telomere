from pathlib import Path

# if only fast5_pass folder, use `input: fast5=fast5_pass_files` in rule
def fast5_pass_files(wildcards):
    in_folder = Path(f"{SAMPLE_DIR}/{wildcards.sample}")
    return list(in_folder.rglob("*fast5_pass/"))[0]

rule run_guppy:
    input:
        fast5=fast5_pass_files
    output:
        run_info=f"{OUT_DIR}/{{sample}}/{MODEL}/{{sample}}_model.txt"
    params:
        folder=f"{OUT_DIR}/{{sample}}/{MODEL}/fastq",
    shell:
        """
        guppy_basecaller \
        -i {input.fast5} \
        -s {params.folder} \
        -c {MODEL} \
        -x auto \
        --recursive \
        --compress_fastq
        echo "Basecalling done with {MODEL}" > {output.run_info}
        """
