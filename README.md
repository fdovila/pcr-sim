# PCR-Sim

PCR Product Generator (given primers)

By: Austin Davis-Richardson
<harekrishna@gmail.com>

---

PCR SIM simulates an amplicon given a database (fasta file) and primers
(5'-3' and 3'-5'). It does this by performing a simple, ungapped alignment:

    AAT
    AAA

Would have an alignment score of `2+2-2=4` based on the score table:

	nucleotides = {
	 'A': ('A', 2),          # Adenosine
	 'C': ('C', 3),          # Cytidine
	 'G': ('G', 3),          # Guanine
	 'T': ('T', 2),          # Thymidine
	 'U': ('U', 2),          # Uridine
	 'R': ('AG', 2.5),       # Purine
	 'Y': ('TC', 2.5),       # Pyrimidine
	 'K': ('GT', 2.5),       # Keto
	 'M': ('AC', 2.5),       # Amino
	 'S': ('GC', 3),         # Strong Interaction (3H)
	 'W': ('AT', 2),         # Weak Interaction (2H)
	 'B': ('CGTU', 8/3),     # Not Adenine
	 'D': ('ATGU', 7/3),     # Not Cytosine
	 'H': ('ACTU', 7/3),     # Not Guanine
	 'V': ('ACG', 8/3),      # Neither Thymidine nor Uridine
	 'N': ('GATCU', 0),      # Any nucleotide
	}

You can adjust this by editing `/pcrsim/search.py`. The scores are multiplied
by `-1` or `-1` depending on match or mismatch, respectively

## Testing

I've tested this script on the Ribosomal Database Project using 515F and 806R
primers and found that the amplicon isn't that good. I haven't compared this
script to a real PCR. For my experiment this was acceptable as the bias didn't
matter and I was able to filter out "good" amplified sequences (by length).

## License

This program is licensed under the GNU GPL 3 license:
http://www.gnu.org/licenses/gpl-3.0.txt

This software is distributed with *ABSOLUTELY NO WARRANT*

## How-To

### Installation

Is pretty easy:

    cd pcr-sim/
    python setup.py install

If you get an error that means you should('nt) use `sudo`.

### Usage

PCR-Sim works like this:

    pcrsim -i input.fasta -f <Forward: 5'->3'> -r <Reverse: 3'->5'> -o out.fa

The script will print a table to `STDOUT` so if you want to save it do:

    pcrsim ... > table.txt

The table is useful for post-processing (filtering out products based on
start, stop and length). The scripts to do this aren't included.

### Output

Headers have the start and stop appended, sequences are truncated from the
beginning of where the forward primer annealed to the end of where the reverse
primer annealed (just like in a real PCR!).

    > sequence1 (515-806)
		gatc...ctag

