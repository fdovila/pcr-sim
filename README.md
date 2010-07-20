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

__Installation:__

Is pretty easy:

    cd pcr-sim/
    sudo python setup.py install

On windows, I'm not sure how to do this.  Probably something like:

    cd pcr-sim/
    python.exe setup.py install


__Usage:__

PCR-Sim works like this:

    pcrsim -i input.fasta -f <Forward: 5'->3'> -r <Reverse: 5'->3' -o out.fa

