import os
import Utils.utils as Utils

COLUMN_SEPARATOR = '\t'
POS_FILE = "_output.txt"

# Generate result file based on results processed
def generate(file_path, process_results):
    path_splited = os.path.split(file_path) # For different separators of different systems
    file_name = f"{path_splited[-1]}{POS_FILE}"
    ouput_file_path = os.path.join("output", file_name)

    ficheiro = Utils.safe_open_w(ouput_file_path)

    header = generate_header()
    ficheiro.writelines(header)

    # sort list
    # sorted_list = sorted(process_results, key=lambda x:-1 if x.get_final_score() is None else x.get_final_score(), reverse=True)

    # Output list
    for data in process_results:
        name = data.get_sequence_name()
        score = generate_score(data.get_final_score())
        tmhmm = generate_tmhmm(data.get_tmhmm())
        tmbb = generate_tmbb(data.get_tmbb())
        prosite = generate_prosite(data.get_prosite())
        cdd = generate_cdd(data.get_cdd())

        line = generate_line(name, score, tmhmm, tmbb, prosite, cdd)

        ficheiro.writelines(line)

    ficheiro.close()

# Generate table header
def generate_header():
    header = f"NAME{COLUMN_SEPARATOR}SCORE{COLUMN_SEPARATOR}TMHMM{COLUMN_SEPARATOR}TMBB{COLUMN_SEPARATOR}PROSITE{COLUMN_SEPARATOR}CDD\n"
    return header

# Generate line with received parameters
def generate_line(name, score, tmhmm, tmbb, prosite, cdd):
    line = f"{name}{COLUMN_SEPARATOR}{score}{COLUMN_SEPARATOR}{tmhmm}{COLUMN_SEPARATOR}{tmbb}{COLUMN_SEPARATOR}{prosite}{COLUMN_SEPARATOR}{cdd}\n"
    return line

# Generate score format to file
def generate_score(score):
    result = ""
    if score == None:
        result = "Error"
    else:
        x = "{:.0f}".format(round(score, 2))
        result = f"{x}%"

    return result

# Generate tmhmm result format to file
def generate_tmhmm(tmhmm):
    result = ""

    if tmhmm.is_error():
        result = "Error"

    else:
        tmhs = tmhmm.get_tmhs()
        is_alfa = "No"

        if tmhmm.has_helix():
            is_alfa = "Yes"

        result = f"{tmhs}:{is_alfa}"

    return result

# Generate tmbb result format to file
def generate_tmbb(tmbb):
    result = ""

    if tmbb.is_error():
        result = "Error"
    else:
        result = "No"

        if tmbb.is_beta():
            result = "Yes"

    return result

# Generate prosite result format to file
def generate_prosite(prosite):
    result = ""

    if prosite.is_error():
        result = "Error"
    else:
        hits = prosite.get_hits()
        result_hits = []

        for h in hits:
            score = h.get_score()
            prof = h.get_profile_code()
            kws = h.get_keywords()
            pkws = h.get_penalty_keywords()

            s = f"{prof}:{score}:{kws}:{pkws}"
            result_hits.append(s)

        result = "; ".join(result_hits)

    return result

# Generate cdd result format to file
def generate_cdd(cdd):
    result = ""

    if cdd.is_error():
        result = "Error"
    else:
        hits = cdd.get_hits()
        result_hits = []

        for h in hits:
            evalue = h.get_evalue()
            name = h.get_name()
            kws = h.get_keywords()
            pkws = h.get_penalty_keywords()

            s = f"{name}:{evalue}:{kws}:{pkws}"
            result_hits.append(s)

        result = "; ".join(result_hits)

    return result