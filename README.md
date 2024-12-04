# KMP_Search
## Overview
`KMP_Search` is a Python program I developed for the Scientific Programming course taught by prof. Rosario Piro at the Politecnico di Milano, as part of my MSc in Bioinformatics and Computational Genomics. The program uses the [Knuth-Morris-Pratt (KMP)](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm) algorithm to find a query sequence in a longer one such as a genome, and does so also using multiprocessing.

## Features: 
- Python script: `KMP_search.py`
- Example file containing random short query sequences: `random_sequences.txt`
- Example genome file: `GCA_000864765.1_ViralProj15476_genomic.fna`

## Usage:
```bash
python KMP_search.py sequence_file genome_file output_file
```

`sequence_file`: Provide path to file with 100 short sequences, each on a new line. I provided an example file (`random_sequences.txt`).

`genome_file`: Provide path to genome file. I provided an example file - I downloaded the reference genome of HIV-1 that is 9.7 kb long (`GCA_000864765.1_ViralProj15476_genomic.fna`). The filename starting with "GCA" indicates the sequence identifier is from the NCBI GenBank database (alternatively it could start with "GCF", if the identifier were from the NCBI RefSeq database).

`output_file`: Provide path to/name of output file. If only the name is provided, the output file is saved in the working directory. If the same filename already exists in the directory, the existing matches will be appended to the file.

## References:
http://jakeboxer.com/blog/2009/12/13/the-knuth-morris-pratt-algorithm-in-my-own-words/
https://stackoverflow.com/questions/13792118/kmp-prefix-table

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).