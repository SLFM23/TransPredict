from Utils.Color import Color

def no_arguments():
    print(Color.red("Please, indicate fasta files to execute"))

def file_not_exist():
    print(Color.red("File does not exist."))

def generic_error():
    print(Color.red("An error occured on script execution."))

def process_intro(seq, seqname, filename, size, i, total):
    print()
    print(Color.green(f"Process start for sequence: {seqname} - {filename}", True))
    print(Color.green(f"Sequence {i} of {total}"))
    print()
    # prefix = Color.blue("Sequence -")
    # print(f"{prefix} {seq}")
    # print()

def invalid_sequence():
    print(Color.red("Current sequence is invalid."))

# TMHMM execution messages
def tmhmm_error():
    print(Color.red("An error occured on TMHMM processing."))
    print()

def tmhmm_start():
    print(Color.blue(f"TMHMM PROCESS SEQUENCE", True))

def tmhmm_result(tmhmm_result):
    tmhs = tmhmm_result.get_tmhs()

    prefix = Color.blue(f"TMHMM - ")

    prefix += f"{tmhs} TMHs;"

    if tmhmm_result.has_helix():
        print(f"{prefix} Alfa Helix structure")
    else:
        print(f"{prefix} No Alfa Helix structure")
    print()

# TMBB execution messages
def tmbb_start():
    print(Color.blue(f"PRED-TMBB PROCESS SEQUENCE", True))

def tmbb_error():
    print(Color.red("An error occured on PRED-TMBB processing."))
    print()

def tmbb_result(tmbbresult):
    prefix = Color.blue(f"PRED-TMBB -")

    print(f"{prefix} Sequence score: {tmbbresult.get_score()}")

    if tmbbresult.is_beta():
        print(f"{prefix} The score is lower than the threshold value of {tmbbresult.get_reference_score()}; Beta Barrel structure.")
    else:
        print(f"{prefix} The score is higher than the threshold value of {tmbbresult.get_reference_score()}; No Beta Barrel structure.")

    print()

# Prosite execution messages
def prosite_start():
    print(Color.blue(f"PROSITE PROCESS SEQUENCE", True))

def prosite_error():
    print(Color.red("An error occured on PROSITE processing."))
    print()

def prosite_hits(hits):
    prefix = Color.blue(f"Prosite -")
    print(f"{prefix} Number of hits: {hits}")

def prosite_hits_data(hits):
    prefix = Color.blue(f"Prosite -")

    for h in hits:
        hit_code = Color.bold(h.get_profile_code())
        hit_kws = h.get_keywords()
        score = h.get_score()
        pkws = h.get_penalty_keywords()

        print(f"{prefix} Keywords matches / Penalty keywords matches for hit {hit_code} (Score: {score}): {hit_kws} / {pkws}")

    print()

# CDD execution messages
def cdd_start():
    print(Color.blue(f"CDD NCBI PROCESS SEQUENCE", True))

def cdd_error():
    print(Color.red("An error occured on CDD NCBI processing."))
    print()

def cdd_no_hits():
    prefix = Color.blue(f"CDD NCBI -")
    
    print(f"{prefix} No hits found for this sequence.")

def cdd_hits(counthits, hits):
    prefix = Color.blue(f"CDD NCBI -")
    
    print(f"{prefix} Number of hits: {counthits}")

    for h in hits:
        hit_accession = Color.bold(h.get_accession())
        hit_name = Color.bold(h.get_name())
        evalue = h.get_evalue()
        kws = h.get_keywords()
        pkws = h.get_penalty_keywords()

        print(f"{prefix} Keywords matches / Penalty keywords matches for hit {hit_name} - {hit_accession} (E-Value: {evalue}): {kws} / {pkws}")

    print()

# Results

def error_on_pre_process():
    print(Color.red("An error occured on previous processing, so can't calculate final score."))
    print()

def final_result(final_score):
    x = "{:.0f}".format(round(final_score, 2))
    print(Color.green(f"Final Result: {x}%", True))
    print()
    