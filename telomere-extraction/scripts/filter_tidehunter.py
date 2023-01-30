import pyfastx
import fire

def reverse_complement(pattern: str) -> str:
    """
    Returns reverse complement of string.
    """
    lookup = {"A": "T", "G": "C", "T": "A", "C": "G"}
    return "".join([lookup[x] for x in pattern])[::-1]

def filter_tidehunter_out(
    tidehunter_out: str, fastq_file: str, sequence_of_interest: str, filtered_out: str
) -> None:
    """
    Writes a new fastq file containing the reads with telomeric regions and telotag.
    :param tidehunter_out: str. Path to tidehounter out file
    :param fastq: str. Path to fastq file.
    :param sequence_of_interest: str. Sequence of interest to search the tidehunter file for.
    :param filtered_out: str. Path  and name of suffix for the new file.
    :returns: Writes a new file with the reads containing telomeres and telotags (A * 10 | T * 10)
    """
    reverse_complement_seq = reverse_complement(sequence_of_interest)
    
    with open(tidehunter_out, "r", encoding="UTF-8") as file:
        telomere_id = set(
            [x.split()[0] for x in file.readlines() if sequence_of_interest in x
             or reverse_complement_seq in x]
        )

    fastq = pyfastx.Fastq(fastq_file, build_index=False)

    with open(filtered_out, "w+", encoding="UTF-8") as filtered:
        for read in fastq:
            if read[0] in telomere_id:
                if "A" * 10 in read[1][-100:] or "T" * 10 in read[1][:100]:
                    print(f"@{read[0]}", file=filtered)
                    print(read[1], file=filtered)
                    print("+", file=filtered)
                    print(read[2], file=filtered)


if __name__ == "__main__":
    fire.Fire(filter_tidehunter_out)