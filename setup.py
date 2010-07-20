from setuptools import setup
import os

DOC = 'See README.md'

setup(
    name="pcr-sim",
    version="0.0.1",
    author="Austin G. Davis-Richardson",
    author_email="harekrishna@gmail.com",
    description="Simulates PCR on a FASTA file given primers",
    url="http://www.github.com/audy/pcr-sim",
    license="GPLv3",
    long_description=DOC,
    
    install_requires = [],
    
    packages = ["pcrsim"],
    
    entry_points = {
        'console_scripts': [ 
            'pcrsim' = 'pcrsim.pcrsim:main'
            ]
    }

)
