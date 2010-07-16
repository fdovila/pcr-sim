# PCR-Sim

PCR Product Generator (given primers)

By: Austin Davis-Richardson
<harekrishna@gmail.com>
	
## PCR-Sim...

 - ...searches templates for matches to primer sequences.
 - ...understands ambiguous nucleotides.
 - ...uses Python 2.6.
 - ...is not a substitute for a girlfriend.

## License

This program is licensed under the GNU GPL 3 license:
http://www.gnu.org/licenses/gpl-3.0.txt

This software is distributed with *ABSOLUTELY NO WARRANT*

## How-To

PCR-SIM prints contigs out to Standard Output so you just pipe to a file

    pcrsim.py -i input.fasta -f <Forward: 5'->3'> -r <Reverse: 5'->3' > pcr_products.fasta

Take note that the reverse primer is still written 5'->3',
the script will reverse-complement for you.