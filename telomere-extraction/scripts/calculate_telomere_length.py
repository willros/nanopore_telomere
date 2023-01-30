import pandas as pd
import fire
import re
import numpy as np


def caluclate_telomere_length(
    telomere_starts: str, bed_file: str, out_file: str, coverage: int = 1
) -> None:
    """
    Calculates telomere lengts from the input files.
    :param telomere_starts: str. Path to the bed file of where telomere starts.
    :param bed_file: str. Path to the bed file of the aligned telomeres.
    :param coverage: int. Default = 1. Number of times the chromosome arm must be represented to be included.
    :param out_file: str. Path to where the csv file should be saved.
    :returns: None. Saves a csv file with the final dataframe.
    """
    telomere_starts = (
        pd.read_csv(telomere_starts)
        .assign(
            chromosome=lambda x: [
                int(re.findall("(\d+)", y)[0]) for y in x.chromosome_arm
            ]
        )
        .assign(
            chromosome_side=lambda x: [
                re.findall("(\D+)", y)[0] for y in x.chromosome_arm
            ]
        )
        .drop(columns=["chromosome_arm"])
        .pivot(
            index="chromosome", columns="chromosome_side", values="telomere_position"
        )
        .reset_index()
    )

    bed = (
        pd.read_csv(
            bed_file,
            sep="\t",
            header=None,
            names=["chromosome", "start", "end", "qname", "score", "strand"],
        )
        .drop_duplicates("qname")
        .assign(
            chromosome=lambda x: np.select(
                [x.chromosome == "chrX", x.chromosome == "chrY"],
                [23, 34],
                default=x.chromosome.str.replace("chr", ""),
            )
        )
        .assign(chromosome=lambda x: x.chromosome.astype(int))
        .merge(telomere_starts, on="chromosome")
        .assign(
            telomere_length=lambda x: np.select(
                [x.start < x.L, x.end > x.R],
                [-(x.L - x.start), x.end - x.R],
                default=pd.NA,
            )
        )
        .dropna()
        .assign(
            arm=lambda x: np.select(
                [x.telomere_length < 0, x.telomere_length > 0],
                ["L", "R"],
                default=pd.NA,
            ),
            chromosome=lambda x: [f"{y.chromosome}{y.arm}" for y in x.itertuples()],
            telomere_length=lambda x: np.abs(x.telomere_length),
        )
        .assign(coverage=lambda x: x.groupby("chromosome")["chromosome"].transform(np.size))
        .loc[lambda x: x.coverage >= coverage]
        .loc[:, ["chromosome", "start", "end", "telomere_length", "qname", "coverage"]]
    )

    bed.to_csv(out_file, index=False)


if __name__ == "__main__":
    fire.Fire(caluclate_telomere_length)
