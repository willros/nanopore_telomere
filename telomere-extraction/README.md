# Extraction and analysis of telomeres for Nanopore data

### IMPLEMENT

1. concatenation of fastq files
2. filter out reads with 10 * T in the first 100 bp
3. filter out reads with 10 * A in the last 100 bp
4. concatenate A and T tail
5. remove duplicates from concatenated A and T tail file (seqkit rmdup [flags])
4. look for the TeloTag in reads
5. filtering out reads with telomere sequences (TTAGG| CCTAAA)
6. align with wf-alignment

# TODO:
* make snakemake rule that filters out polyT and polyA and plots


### seqkit
* use seqkit fish to look for short sequences in larger sequences using local alignment
	* cat FAV30870_pass_9aed0d00_b60ee94e_9.fastq.gz | seqkit fish -a -F TTAGGGTTAGGG -g
	* cat FAV30870_pass_9aed0d00_b60ee94e_9.fastq.gz | seqkit fish -F TTAGGGTTAGGGTTAGGG -a -g
* use seqkit `locate` to look for short sequences
* cat fastq.fastq | seqkit grep -s -p AAAAAAAAAAGACGTGTGCTCTTCCGATCT -m 2 > out.fastq.gz

# DEPENDENCIES

### Porechops
```bash
git clone https://github.com/rrwick/Porechop.git
cd Porechop
make
```
Need to replace the adapters.py file with another with updated sequences.
```bash
# removed the following from the file:
 Adapter('G_strand_adapter',
             	    start_sequence=('Start_G_adapter_L', 'CAGTCTACACATATTCTCTGTTTTT'),
             	    end_sequence=('End_G_adapter_R', 'AAAAACAGAGAATATGTGTAGACTG')),

            Adapter('Ligation_adapter',
                    start_sequence=('Start_Ligation_adapter_L', 'TATATATACAGTGACATAACGTACGACCTACCACAATCTGTTCCGG'),
                    end_sequence=('End_Ligation_adapter_R', 'ATATATATGTCACTGTATTGCATGCTGGATGGTGTTAGACAAGGCC')),

# added the following instead:
 Adapter('telotag_adapter',
             	    start_sequence=('Start_telotag_adapter', 'AGATCGGAAGAGCACACGTCTTTTT'),
             	    end_sequence=('End_telotag_adapter', 'AAAAAGACGTGTGCTCTTCCGATCT')),
```
### Seqkit
```bash
mamba install -c bioconda seqkit
```
### Tidehunter
```bash
wget https://github.com/yangao07/TideHunter/releases/download/v1.5.4/TideHunter-v1.5.4.tar.gz
tar -zxvf TideHunter-v1.5.4.tar.gz && cd TideHunter-v1.5.4
sudo apt install libz-dev
make
```

# IDEAS
* Need a better way to identify telomeres...
    * More lenient in the minimap2 rule to not throw away data

### algorithm
* How to identify the length of the telomere?
    * regex?
 
#### Look at C content for the 5' and G content for the 3'.
* if C or G content is > 40% then telomere
* sliding window?

#### Alignment
* Trim of the telomere part and only align the subtelomeric part to the genome
* mask the sequence with Readmasker?



# New workflow
## Use the data called with the `sup` model

### QC
* [x] Look at QC data and compare betwwen fast model and sup model
    * NanoPlot

### All reads (raw reads)
* [x] merge fastqfiles
* [x] extract raw stats
* [x] count how many contains telotag
    * seqkit grep extract both sides
    * maybe this can be extracted from tidehunter out?
* [x] count how many contains polyA and polyT
    * fiddle with the parameters of the regex!
* [x] Extract mean value of polyA and polyT
    * [x] make plots of those
* [x] trim reads
    * add the right adapters to porechop (v14 kit)
* [x] align to reference
    * wf-alignment

### Telomere reads
* [x] Extract telomere with tidehunter
    * [x] play with input parameters:
        * -p --min-period  INT    minimum period size of tandem repeat (>=2) [30]
            * change this to 12? 30 now 
                * The default parameter was better
    * count length of telomeres
* [x] extraxt telomeric reads from fastqfile
    * use seqkit?
    * [x] look at the QC of the telomeric reads
* remove the telomere region
    * use the end|start values from the tidehunter output
* align to reference
    * [x] "raw" telomeres
        * porechop first
    // the below is perhaps not needed!
    * "filtered telomeres"
        * remove the telomere region by end|start values from tidehunter output
    * more lenient parameters in minimap2
* align to the alternative subtelomeric regions
* See how long the telomeres are 

# 2022-12-09
### add --no_split to Porechop to not split the reads based on middle adapter


# 2022-12-13
* The new sequencing round is done with the TagTel3 adapter:
"5´-AGATCGGAAGAGCACACGTCCCCTAACCCTAACCCTAA-3´"

* Use this when looking for reads with adapters instead of the first one
* Exclude the polyA and polyT steps

### Copied the first Snakefile:
* The first is named Snakefile_telotag
* The new one is named Snakefile_tag_tel_3


When searching for adapter, search only in the beginning of the read. -R 1:200


### It find very few reads with the ADAPTER using grep.
When I use `cat TagTelo3_221206_merged.fastq.gz | seqkit locate -p AGATCGGAAGAGCACACGTCCCCTAACCCTAACCCTAA -m 5`, it also finds very few reads... WHY???

#### used seqkit grep with only the TruSeq sequence, allowing 8 mismatches, still I cant find many reads with the adapter... 

### Of course! The TagTel3 only binds to telomeric motifs! Thats why??

Try https://github.com/bonsai-team/Porechop_ABI


# 2022-12-14

Updated the `extract_telomere_from_tidehunter` to filter out consseq from tidehunter with 4 motifs of telomere (4 * TTAGGG) etc.
Also added:
```python
    .groupby("id")
    .agg(start=("start", lambda x: x.min()),
         end=("end", lambda x: x.max()),
         read_len=("read_len", lambda x: x.max()),
         cons_seq=("cons_seq", lambda x: x.values[0])
        )
    .reset_index()
    .assign(region_length=lambda x: x.end - x.start)
```

### rewrite the minimap2 and other fucntions to take variables from the main Snakefile so it is easier to change the input... Or is that possible?


# 2022-12-19

* Dowload the hg38 genome and align towards that.

* Trye the alignoth to plot reads for chromosome ends
* Set up IGV on the nanopore comp
* Look for reads with pure telomere sequence that cannot be aligned to reference genome

# 2022-12-20

* Rewrite the function that extract telomeres from the tidehunter file:
    * Include where in the read the contig sits
    * Include read len from the tidehunter file
   
### Make FASTA file from all telomere sequences. 

### Make QC plot for all telomere reads that align to the ends
* For the basecalling and the alignment