from hmac import trans_36
from Bio import SeqIO
import pandas as pd
import Utils.calc as Calculate

def get_sequence_by_id(seq_id, sequence_list):
    for s in sequence_list:
        if str(s.id) == str(seq_id):
            return s

def get_sequence_id(st):
    res = ""
    for s in st:
        if s == ' ':
            return res
        res+=s
    return res

def is_transporter(sequence, protein_tcdb_sequences):
    for psequence in protein_tcdb_sequences:
        if sequence.seq == psequence.seq:

            return True

    return False

def get_score(score):
    try:
        return float(score.strip('%'))
    except:
        return 0

FILE = "../Data/transpredict/s_cerevisiae_final.txt"
ORIGINAL_FILE = "Cere/cere.faa"
NAME = "Cere"
THRESHOLD = 60.0

data = pd.read_csv(FILE, sep='\t').to_numpy()
fasta_sequences = list(SeqIO.parse(ORIGINAL_FILE, 'fasta'))
protein_tcdb_sequences = list(SeqIO.parse('/Users/marcelo/Desktop/Rita/Tese/tese.nosync/Data/Positive/positive-filtered.fasta', 'fasta'))

trans = 0
not_trans = 0

true_positive = 0
true_negative = 0
false_positive = 0
false_negative = 0

false_positive_ids = []
false_negative_ids = []

for item in data:
    seq_id = get_sequence_id(item[0])
    sequence = get_sequence_by_id(seq_id, fasta_sequences)
    is_current_transporter = is_transporter(sequence, protein_tcdb_sequences)
    score = get_score(item[1])

    has_score_to_consider_transporter = score >= THRESHOLD

    if is_current_transporter:
        trans+=1
    else:
        not_trans += 1

    if is_current_transporter and has_score_to_consider_transporter:
        true_positive += 1
    elif is_current_transporter and not has_score_to_consider_transporter:
        false_negative += 1
        false_negative_ids.append(seq_id)
    elif not is_current_transporter and has_score_to_consider_transporter:
        false_positive += 1
        false_positive_ids.append(seq_id)
    else:
        true_negative += 1
    

Calculate.calculate_data(NAME, true_positive, true_negative, false_positive, false_negative)

print(false_negative_ids)