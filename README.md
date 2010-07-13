# PCR-Sim

PCR Product Generator (given primers)

By: Austin Davis-Richardson
    <harekrishna@gmail.com>
	
## What it does:

PCR-Sim matches primer sequence to a multifasta file of templates and prints
out products (including primers).  It does so by BLASTing each template
with each primer to find match.

## License

This program is licensed under the GNU GPL 3 license:
http://www.gnu.org/licenses/gpl-3.0.txt

This software is distributed with *ABSOLUTELY NO WARRANT*

## Pre-reqs

pcrsim requires the following

* Python 2.6.5
* NCBI Blast+ 2.2.23 (specifically, bl2seq and blastn)
* A UNIX-like operating system.  Tested on Mac OS 10.6 and Ubuntu 9.04


## How-To

Invoke thusly::

	Usage: pcrsim.py [options]

	pcrsim.py - Simulates PCR on a given input FASTA file using BLAST.

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -v, --verbose         Print Debugging Information
	  -i INFILE, --infile=INFILE
	                        Specify Input FASTA file
	  -f FORWARD, --forward=FORWARD
	                        Specify forward primer (5' to 3')
	  -r REVERSE, --reverse=REVERSE
	                        Specify reverse primer (5' to 3')
	
pcrsim will output directly to STDOUT so pipe it to a new FASTA file

	pcrsim.py -i input.fasta -f GA..TC -r GA..TC > pcr_products.fasta

## Testing

If you want to try it out, make a test.fasta with this record:

	>AB009457_Pseudomonas_plecoglossicida
	agagtttgatcatggctcagattgaacgctggcggcaggcctaacacatgcaagtcgagcggatgacgggagcttgct
	ccttgattcagcggcggacgggtgagtaatgcctaggaatctgcctggtagtgggggacaacgtttcgaaaggaacgc
	taataccgcatacgtcctacgggagaaagcaggggaccttcgggccttgcgctatcagatgagcctaggtcggattag
	ctagttggtggggtaatggctcaccaaggcgacgatccgtaactggtctgagaggatgatcagtcacactggaactga
	gacacggtccagac
	
and test with this command

	./pcrsim.py -i test.fasta -f agagtttgatcctggctcag -r gctgcctcccgtaggagt 
	
Get lengths of products

    ./pcrsim.py -i in.fa -f agagtttgatcctggctcag -r gctgcctcccgtaggagt | grep -v '^[>]' | awk '{ print length($0) }'


## Bugs

Uses BLAST