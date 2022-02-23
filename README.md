# TransPredict

The TransPredict is a python tool capable of performing an identifier of possible transporters, given the developed or inferred proteome. To do that, it's used a several bioinformatic tools acessions, such as TMHMM, PredTMBB, CDD and Prosite. With the first two tools we extract structural information and with the last two motifs and conserved domains.

The general pipeline is shown below:
![Imagem1](https://user-images.githubusercontent.com/63756398/155417798-39602888-3154-4687-9ec4-cc4e5233a22a.png)

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

## Results
The results of the references genomes, E. coli and S. cerevisiae, are presented in "output" folder.
