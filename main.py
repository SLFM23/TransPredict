from Bio import SeqIO
import sys
import Utils.messages as Messages
import Utils.utils as Utils
import data.TMHMM.tmhmm as Tmhmm
import data.TMBB.tmbb as Tmbb
import data.CDD.cdd as Cdd
import data.Prosite.prosite as Prosite
import process_results.results as Results
from process_results.ProcessResult import ProcessResult
import process_results.file_generator as FileGenerator
import re

def get_seqName(seq_description):
    m = re.search(r"^(.*)\[", seq_description)
    description = str(m.group())[:-1].strip()

    return description
    

# Main function
def main(argv):

    # check if receive arguments
    if len(argv) == 0:
        Messages.no_arguments()
        return

    # check if received files exists
    if not Utils.valida_ficheiros(argv):
        Messages.file_not_exist()
        return

    try:
        # Run for each received file
        for f in argv:

            # Parse fasta file
            fasta_sequences = list(SeqIO.parse(open(f), 'fasta'))

            i = 1
            total = len(fasta_sequences)

            process_results = []

            for fasta_sequence in fasta_sequences:
                sequence = str(fasta_sequence.seq)

                seq_name = get_seqName(fasta_sequence.description)
                process_result = ProcessResult(seq_name)

                Messages.process_intro(sequence, seq_name, f, len(sequence), i, total)

                # Check if sequence is valid to process
                if not Utils.validate_sequence(sequence):
                    Messages.invalid_sequence()
                    continue

                # Process current sequence
                process(sequence, process_result)

                # append process result object to list
                process_results.append(process_result)

                i+=1

                # Generate result file based on results processed
                FileGenerator.generate(f, process_results)

    except Exception as e:
        print(e)
        Messages.generic_error()


# Process sequence function
def process(sequence, process_result):
    tmhmm_result = Tmhmm.process(sequence)
    tmbb_result = Tmbb.process(sequence)
    prosite_result = Prosite.process(sequence)
    cdd_result = Cdd.process(sequence)

    final_result = Results.generate(tmhmm_result, tmbb_result, prosite_result, cdd_result)

    process_result.set_tmhmm(tmhmm_result)
    process_result.set_tmbb(tmbb_result)
    process_result.set_prosite(prosite_result)
    process_result.set_cdd(cdd_result)
    process_result.set_final_score(final_result)

if __name__ == "__main__":
    main(sys.argv[1:])