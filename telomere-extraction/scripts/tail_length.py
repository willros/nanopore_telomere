import fire
from pathlib import Path
import pyfastx
import pandas as pd
import re
import altair as alt
import numpy as np
from altair_saver import save
alt.data_transformers.disable_max_rows()


def tail_lengths(fastq: str, out_file: str, out_plots_path: str) -> None:
    """
    Extract lengths of polyA and polyT tails.
    Generates plots and mean values (pandas describe)
    :param fastq str: path to fastqfile.
    :param outfile str: path to outfile
    :param out_plot str: path to dir of out plots
    """
    out_dir = Path(out_file).parent
    
    fq = pyfastx.Fastq(fastq, build_index=False)
    poly_t = re.compile(r"(TTTTTTTTTTTTTTT*).")
    poly_a = re.compile(r"(AAAAAAAAAAAAAAA*).")
    
    t_lengths = []
    t_ids = []
    for read in fq:
        if "TTTTTTTTTTTTTTT" in read[1][:100]:
            match = re.findall(poly_t, read[1])
            t_lengths.append(len(match[0]))
            t_ids.append(read[0])
            
    a_lengths = []
    a_ids = []
    for read in fq:
        if "AAAAAAAAAAAAAAA" in read[1][-100:]:
            match = re.findall(poly_a, read[1])
            a_lengths.append(len(match[0]))
            a_ids.append(read[0])
            
    # dataframes and plotting
    df_t = pd.DataFrame({"ts": t_lengths, "id": t_ids})
    df_a = pd.DataFrame({"as": a_lengths, "id": a_ids})
    
    # statistics
    
    (pd.concat([df_t["ts"].to_frame().describe().T, df_a["as"].to_frame().describe().T])
     .to_csv(out_file, index=False)
    )
    
    # how many reads with both polyA and polyT?
    both = pd.concat([df_t, df_a])
    number_duplicated = both.shape[0] - both.drop_duplicates("id").shape[0]
    with open(f"{out_dir}/number_duplicated.txt", "w+") as f:
        print(f"Number of reads with both polyA and polyT tail: {number_duplicated}", file=f)
    
    # plots
    poly_t = alt.Chart(df_t).mark_area().encode(
     alt.X("ts:Q", bin=alt.Bin(extent=[15, 300], step=10), title="size (bp)"),
     alt.Y("count()", title="number of reads with this length")
    ).properties(width=600,
                 height=400,
                 title="Histogram of polyT-tail")
    
    poly_a = alt.Chart(df_a).mark_area(color="orange").encode(
     alt.X("as:Q", bin=alt.Bin(extent=[15, 300], step=10), title="size (bp)"),
     alt.Y("count()", title="number of reads with this length"),
    ).properties(width=600,
                 height=400,
                 title="Histogram of polyA-tail")
    
    save(poly_t, f"{out_plots_path}/polyT-plot.pdf")
    save(poly_a, f"{out_plots_path}/polyA-plot.pdf")
    
if __name__ == "__main__":
    fire.Fire(tail_lengths)