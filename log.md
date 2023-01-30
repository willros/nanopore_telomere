# Log for automatisation process for nanopore data

## 2022-11-23

* Setting up an automated process with snakemake and cron
* Folder structure of analysed data:
	* raw data --> sequencing-data
	* analyzed data --> analyzed-data/sample
	* basecalled data --> analyzed-data/sample/fastq
	* Report of run and basecalling -> analyzed/sample/raw_report/

* The model in the config file is now: dna_r10.4.1_e8.2_260bps_sup.cfg (the super accuracy model)

* install seqkit:
````bash
mamba install -c bioconda seqkit
```

