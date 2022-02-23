# TransPredict

This is a python script to process fasta sequences for multi platforms

The TransPredict is a tool capable of performing an identifier of possible transporters, given the developed or inferred proteome. To do that, it's used a several bioinformatic tools acessions, such as TMHMM, PredTMBB, CDD and Prosite. With the first two tools we extract structural information and with the last two motifs and conserved domains.

## Dependencies

**Pip** - [Pip page](https://pip.pypa.io/en/stable/)

**BioPython** - [BioPython page](https://biopython.org/)

**TmHmm** - [Tmhmm page](https://github.com/dansondergaard/tmhmm.py)

**Requests** - [Requests page](https://requests.readthedocs.io/en/master/)

**Beautiful Soup** - [BeautifulSoup page](https://www.crummy.com/software/BeautifulSoup/bs4)

## Installation

Install all previous dependencies using **pip** before execute script

## Usage

```bash
cd source_code_path
```

```bash
python main.py <fasta_sequence_file_1> <fasta_sequence_file_2> ...
```
