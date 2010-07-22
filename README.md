# PCR-Sim

PCR Product Generator (given primers)

By: Austin Davis-Richardson
<harekrishna@gmail.com>
	
## PCR-Sim...

 - ...searches templates for matches to primer sequences.
 - ...understands ambiguous nucleotides.
 - ...uses Python 2.6.

## License

This program is licensed under the GNU GPL 3 license:
http://www.gnu.org/licenses/gpl-3.0.txt

This software is distributed with *ABSOLUTELY NO WARRANT*

## How-To

###Installation

Is pretty easy:

    cd pcr-sim/
    sudo python setup.py install

On windows, I'm not sure how to do this.  Probably something like:

    cd pcr-sim/
    python.exe setup.py install

###Usage

PCR-Sim works like this:

    pcrsim -i input.fasta -f <Forward: 5'->3'> -r <Reverse: 5'->3'> -o out.fa

###Output

Headers have the start and stop appended, sequences are truncated from the
beginning of where the forward primer annealed to the end of where the reverse
primer annealed.

    > sequence1 (515-806)
		gatc...ctag

