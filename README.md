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

## Pipeline Explanation

- TMHMM: número de TMHs, estrutura α-hélice ou não
- Pred-TMBB: score da sequência, estrutura β-folha ou não
- Prosite: número de hits e para cada hit: keywords e penalty keywords encontradas, código da familia e score
- CDD: número de hits e para cada hit: keywords e penalty keywords encontradas, código da familia e score
- Final result (FR): percentagem final atribuída para possibilidade de ser transportador.

FR = 20% × structure + 20% × Prosite + 60% × CDD

structure - Valor do TMHMM ou Pred-TMBB 
CDD - valor do maior hit com keywords 
Prosite - valor do maior hit com keywords

### TMHMM e Pred-TMBB

Permitem retirar informação acerca da estrutura secundária da proteína, condição necessária para o veredicto. No FR, tem de se verificar uma das condições, ser α-héice, β-folha ou ambos.

### Prosite e CDD

Indicam-nos quais os hits e os respetivos scores/e-value, bem como, através da descrição da família obtida podemos filtrar os domínios funcionais que se referem a transportadores, através de uma pesquisa por keywords. Dependendo da janela de valores dos scores (no caso do Prosite) e e-values (no caso do CDD), foi atribuída uma percentagem ao melhor hit de 100%, 70%, 30% ou 0%.

### Penalizações e bonificações 

- TMHMM e Pred-TMBB - incremento de 5% à parcela "structure" na presenca de ambas (α-hélice e β-folha) e penalização de 5% se faltar alguma.
- TMHMM - 6 ou mais TMH’s é atribuída a totalidade dos 20%, referentes à "structure". Já no caso de obter um resultado entre 3 e 5 TMH’s, atribui-se apenas (10%).
- Prosite e CDD - keywords "sensor" e "transfer" aplica-se uma penalização de 20%, "enzyme" e "transferase" aplica-se uma penalização de 40%, estes termos excluem a possibilidade da proteína ser um transportador. Na presença de "antiporter", "symporter" e "permease", é aplicado um incremento de 15%.

