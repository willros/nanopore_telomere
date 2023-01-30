import pyfastx
import fire
import re


def reverse_complement(pattern: str) -> str:
    """
    Returns reverse complement of string.
    """
    lookup = {"A": "T", "G": "C", "T": "A", "C": "G"}
    return "".join([lookup[x] for x in pattern])[::-1]


def find_telomeric_reads(
    fastq_file: str,
    filtered_file: str,
    telomere_pattern: str = "TTAGGG",
    repeat_n: int = 2,
    occurancies: int = 2,
    telotag: bool = False,
) -> None:

    """
    Writes a new fastq file containing the reads with telomeric regions and polyA or polyT.
    :param fastq_file: str. Path to fastq file.
    :param filtered_file: str. Path to new file with filtered sequences.
    :param telomere_pattern: str. Telomeric pattern. Default: TTAGGG
    :param occurancies: int. How many times the telomeric pattern must exist to be called a telomere
    :returns: Writes a new file with the reads containing telomeres and telotags (A * 10 | T * 10)
    """

    fastq = pyfastx.Fastq(fastq_file, build_index=False)
    telomere_forward = re.compile(telomere_pattern * repeat_n)
    telomere_reverse = re.compile(reverse_complement(telomere_pattern) * repeat_n)

    with open(filtered_file, "a+", encoding="UTF-8") as f:
        for x in fastq:
            if (
                len(re.findall(telomere_forward, x[1])) >= occurancies
                or len(re.findall(telomere_reverse, x[1])) >= occurancies
            ):
                # does the read contain telotag?
                if telotag:
                    if "A" * 10 in x[1][-100:] or "T" * 10 in x[1][:100]:
                        print(f">{x[0]}", file=f)
                        print(f"{x[1]}", file=f)
                else:
                    print(f">{x[0]}", file=f)
                    print(f"{x[1]}", file=f)


#    # if no telomere sequence is found in the fastq file, remove the filtered file.
#    if os.path.getsize(filtered_file) <= 0:
#        os.remove(filtered_file)


if __name__ == "__main__":
    fire.Fire(find_telomeric_reads)