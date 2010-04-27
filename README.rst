=========
 PCR-SIM
=========

By: Austin Davis-Richardson
harekrishna@gmail.com
	
DESCRIPTION
===========

PCR-SIM is a Polymerase Chain Reaction Simulator.  It uses BLAST to predict
where two primers will anneal on a template.

It's currently in development therefore this README is tentative.

LICENSE
=======

This program is licensed under the GNU GPL 3 license:
http://www.gnu.org/licenses/gpl-3.0.txt

REQUIREMENTS
============

pcr-sim requires the following

* Python 2.6.5
* NCBI Blast+ 2.2.23 (specifically, bl2seq and blastn)
* A UNIX-like operating system.  Tested on Mac OS 10.6 and Ubuntu 9.04


USAGE
=====

Invoke thusly::

	Usage: pcr-sim.py [options]

	pcr-sim.py - Simulates PCR on a given input FASTA file using BLAST.

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

