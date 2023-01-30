import pandas as pd
import fire

def telomeres_from_bed_file(
    tidehunter_left: str,
    tidehunter_right: str,
    bedfile: str,
    telomeres_out: str,
) -> None:

    """
    Merges the left and right telomeres from TideHunter with the bed file and save only the
    reads that are not duplicated
    :param tidehunter_left: str. Path to tidehunter left
    :param tidehunter_right: str. Path to tidehunter right
    :param bedfile: str. Path to bed file
    :param telomeres_out: str. Path to out file
    :returns: Writes a new file with the reads containing telomeres
    """
    
    def wrangle_telomeres(csv) -> pd.DataFrame:
        return (
            pd.read_csv(csv)
            [["id", "region_length", "read_len", "start", "end"]]
            .assign(telomere_type="CCCTAA")
            .rename(columns={"start": "telomere_pattern_start",
                     "end": "telomere_pattern_end"})
        )
    
    left_telomeres = wrangle_telomeres(tidehunter_left)
    right_telomeres = wrangle_telomeres(tidehunter_right)
    
    bed = (
        pd.read_csv(bedfile,
                      sep="\t",
                      header=None,
                      names=["chr", "align_start", "align_end", "id", "x", "strand"])
        .drop(columns=["x"])
    )
    
    left_bed = bed.merge(left_telomeres, on="id")
    right_bed = bed.merge(right_telomeres, on="id")
    left_and_right = (
        pd.concat([left_bed, right_bed])
        .drop_duplicates((["id", "align_start", "align_end"]))
        .sort_values("region_length", ascending=False)
    )
    
    left_and_right.to_csv(telomeres_out, index=False)

if __name__ == "__main__":
    fire.Fire(telomeres_from_bed_file)