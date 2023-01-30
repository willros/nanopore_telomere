import pandas as pd
import fire
import pyfastx

def remove_telomeres_from_read(
    fastq_file: str,
    tidehunter_left: str,
    tidehunter_right: str,
    filtered_file: str,
) -> None:

    """
    Removes telomere sequences from reads in a FASTQ file.
    
    This function reads a FASTQ file and two TideHunter output files containing
    information about the telomere sequences found in the reads. It then uses
    this information to remove the telomere sequences from the reads and saves
    the resulting reads to a new file.

    Args:
        fastq_file: The path to the FASTQ file containing the reads.
        tidehunter_left: The path to the TideHunter output file containing
            information about the left telomere sequences found in the reads.
        tidehunter_right: The path to the TideHunter output file containing
            information about the right telomere sequences found in the reads.
        filtered_file: The path to the file where the resulting reads should be
            saved.

    Returns:
        None
    """ 

    fastq = pyfastx.Fastq(fastq_file, build_index=False)
    left = pd.read_csv(tidehunter_left)
    right = pd.read_csv(tidehunter_right)
    both = pd.concat([left, right], ignore_index=True).drop_duplicates("id")


    with open(filtered_file, "a+", encoding="UTF-8") as filtered:
        for read in fastq:
            if read[0] in both.id.values:
                start = both.loc[lambda x: x.id == read[0]].start.squeeze()
                end = both.loc[lambda x: x.id == read[0]].end.squeeze()
                first_part = read[1][:start]
                second_part = read[1][end + 1:]
                telomere_removed = first_part + second_part
                print(f"@{read[0]}", file=filtered)
                print(telomere_removed, file=filtered)
                print("+", file=filtered)
                print(read[2], file=filtered)

                
                
if __name__ == "__main__":
    fire.Fire(remove_telomeres_from_read)


