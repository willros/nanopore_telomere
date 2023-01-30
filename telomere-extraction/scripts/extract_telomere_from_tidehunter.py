import pandas as pd
import fire
from pathlib import Path


def extract_telomere_from_tidehunter(tidehunter: str,
                                     left_telomere_file: str,
                                     right_telomere_file: str,
                                     telomere_ids: str
) -> None:
    """
    Extract telomere sequences from Tidehunter
    :param tidehunter str: path to tidehunter outfile
    :param telomere_file str: path to file names
    """
    
    names=[
        "id", "rep_number", "copy_number", "read_len", 
        "start", "end", "conslen",
        "avematch", "full_len", "subpos", "cons_seq"
    ]
    
    tidehunter = (
        pd.read_csv(tidehunter,
        sep="\t",
        header=None,
        names=names
        )
       #.assign(region_length=lambda x: x.end - x.start) 
       .drop(columns=["rep_number", "copy_number", "full_len", "subpos"])
    )
    
    # CCCTAA telomere (how can telomere NOT start at the beginning of read?)
    left_telomere = (
      tidehunter
     # adding one more motif to each filtering (4 motifs CCCTAA and TTAGGG)
     # Also added the "groupby functions"
     .loc[lambda x: x.cons_seq.str.contains("CCCTAACCCTAACCCTAACCCTAA")]
     .groupby("id")
     .agg(start=("start", lambda x: x.min()),
         end=("end", lambda x: x.max()),
         read_len=("read_len", lambda x: x.max()),
         cons_seq=("cons_seq", lambda x: x.values[0])
        )
     .reset_index()
     .assign(region_length=lambda x: x.end - x.start)
     .sort_values("region_length", ascending=False)
    )
    left_telomere.to_csv(left_telomere_file, index=False)
    
    # TTAGGG telomere (how can telomere NOT be at the end of read?)
    right_telomere = (
      tidehunter
     .loc[lambda x: x.cons_seq.str.contains("TTAGGGTTAGGGTTAGGGTTAGGG")]
     .groupby("id")
     .agg(start=("start", lambda x: x.min()),
         end=("end", lambda x: x.max()),
         read_len=("read_len", lambda x: x.max()),
         cons_seq=("cons_seq", lambda x: x.values[0])
        )
     .reset_index()
     .assign(region_length=lambda x: x.end - x.start)
     .sort_values("region_length", ascending=False)
    )
    right_telomere.to_csv(right_telomere_file, index=False)
    
    # save the IDs to a file
    (
        pd.concat([left_telomere, right_telomere])
        # do not drop the duplicates
        #.drop_duplicates("id")
        ["id"]
        .to_csv(telomere_ids, header=False, index=False, sep="\n")
    )
    


if __name__ == "__main__":
    fire.Fire(extract_telomere_from_tidehunter)