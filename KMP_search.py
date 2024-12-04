import sys
import os
import multiprocessing
import numpy as np
import pandas as pd
from multiprocessing import Process, Lock

# Define function needed to compute the prefix table used in the KMP search algorithm
def compute_prefix_table(sequence):
    m = len(sequence)
    pi = np.zeros(m, dtype=int)
    k = 0
    for q in range(1, m):
        while k > 0 and sequence[k] != sequence[q]:
            k = pi[k - 1]
        if sequence[k] == sequence[q]:
            k += 1
        pi[q] = k
    return pi

# Define search function (calls the function that computes the prefix table)
def kmp_search(text, sequence):
    n = len(text)
    m = len(sequence)
    pi = compute_prefix_table(sequence)
    k = 0
    indices = []
    for i in range(n):
        while k > 0 and sequence[k] != text[i]:
            k = pi[k - 1]
        if sequence[k] == text[i]:
            k += 1
        if k == m:
            indices.append(i - m + 1)
            k = pi[k - 1]
    return indices

# Define function that reads the files and calls the search function, outputs the results to the
# output file with a lock. The function also removes the first line of the genome (FASTA) file, as it doesn't
# contain the sequence.
def search_sequence(sequence_file, sequence, output_file, lock):
    with open(sequence_file, 'r') as f:
        lines = f.readlines()
        if lines[0].startswith(">"):
            lines = lines[1:]
        genome = ''.join(lines)
    indices = kmp_search(genome, sequence)
    
    # Define the function so that it uses a lock to open the output file:
    with lock:
        with open(output_file, 'a') as f:
            f.write(f"Sequence: {sequence}, Matches at indices: {indices}\n")

# Define what happens when the script is executed, with the parameters provided on the command line:
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py sequence_file genome_file output_file")
        sys.exit(1)

    sequence_file = sys.argv[1]
    genome_file = sys.argv[2]
    output_file = sys.argv[3]

    # Check if files exist / paths are specified correctly:
    if not os.path.isfile(sequence_file) or not os.path.isfile(genome_file):
        print("Error: Sequence file or Genome file not found.")
        sys.exit(1)

    # Check if the genome file starts with ">":
    with open(genome_file, 'r') as f:
        first_line = f.readline()
        if not first_line.startswith(">"):
            print("Please provide a FASTA file.")
            sys.exit(1)

    # Create Lock object that will be passed to all child processes:
    lock = Lock()

    # Read in file of provided short query sequences (I set separator=tab in case the file has more columns)
    # and put all the sequences into a string array:
    seqs_df = pd.read_csv(sequence_file, header=None, sep = "\t")
    seqs = np.array(seqs_df[0], dtype=str)

    # Start as many child processes as there are sequences, use a lock to prevent writing to the output file
    # at the same time, and wait for all the processes to finish (Pool could also be used here):
    processes = []
    for sequence in seqs:
        sequence = sequence.strip()
        p = Process(target=search_sequence, args=(genome_file, sequence, output_file, lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("Search for query sequences complete. Results written to", output_file)
