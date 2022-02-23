import Utils.messages as Messages

# Score final = 20% para a estrutura (TMHMM ou Pred-TMBB) + 20% Prosite + 60% CDD

# No TMHMM: 5 ou mais TMH's atribuídos 100% dos 20%;  entre 3 a 5 TMH's 50% dos 20%

# Relativamente à estrutura da proteína no geral (TMHMM e Pred-TMBB): se se verificar ambas as estruturas => incremento de 5% dos 20%; se não tiver nenhuma das estruturas penalizar em 40% no Score final

# Keywords do CDD: 
#     sensor e binding leva a penalização de 20% no Score final
#     enzyme e transfer leva a penalização de 40% no Score final
#     antiporter, symporter e permease leva a incremento de 15% no Score final

# Verificamos também que será possível/desejável alterar os valores colocados para o e-value do CDD e prosite, uma vez que mesmo que tenha keywords ainda que os valores de e-value sejam baixos, já não obtemos nenhuma "pontuação" por esses parâmetros. Assim, eu e a Isabel, pensamos que poderíamos, dentro do CDD e do Prosite, atribuir, aos respetivos pesos do Score final, sub-pesos ao e-value e às keywords:
# CDD - 20% para e-value e 40% keywords   (prefaz os 60% do Score final)
# Prosite - 10% para cada     (prefaz os 20% do Score final)

# para calculo da percentagem final ter em conta apenas as keywords (percentagem total)
# scores e evalues servem para calcular quais os melhores hits e ficar com os máximos e é cumulativo
# as keywords nao são cumulativas no calculo final. assume so um 15% se tiver mais que uma de somar e assume a de maior penalização

def generate(tmhmm, tmbb, prosite, cdd):

    if tmhmm.is_error() or tmbb.is_error() or prosite.is_error() or cdd.is_error():
        Messages.error_on_pre_process()
        return None

    tmhmm_percentage = calculate_tmhmm_percentage(tmhmm)
    tmbb_percentage = calculate_tmbb_percentage(tmbb)
    structure_final_percentage = calculate_structure_final_percentage(tmhmm_percentage, tmbb_percentage)

    prosite_percentage = calculate_final_prosite_percentage(prosite)
    cdd_percentage = calculate_final_cdd_percentage(cdd)

    print(f"STRUCTURE: {structure_final_percentage}")
    print(f"PROSITE: {prosite_percentage}")
    print(f"CDD: {cdd_percentage}")
    final_score_perc = (structure_final_percentage + prosite_percentage + cdd_percentage) * 100

    if final_score_perc < 0:
        final_score_perc = 0

    if final_score_perc > 100:
        final_score_perc = 100

    Messages.final_result(final_score_perc)

    return final_score_perc

def calculate_structure_final_percentage(tmhmm_percentage, tmbb_percentage):
# Relativamente à estrutura da proteína no geral (TMHMM e Pred-TMBB): se se verificar ambas as estruturas => incremento de 5% dos 20%; se não tiver nenhuma das estruturas penalizar em 40% no Score final

    result = max(tmhmm_percentage, tmbb_percentage)
    
    if tmhmm_percentage > 0 and tmbb_percentage > 0:
        return 0.25
    elif tmhmm_percentage == 0 and tmbb_percentage == 0:
        return -0.2 # deve ter uma penalização de 40% sobre a FF

    return result * 0.2

# Calculate for tmhmm process, the current percentage - returned in decimal
def calculate_tmhmm_percentage(tmhmm):
    tmhs = tmhmm.get_tmhs()

    result = 0

    if tmhs >= 5:
        result = 1

    if tmhs < 5 and tmhs >= 3 :
        result = 0.5

    tmhmm.set_percentage(result)

    return result

# Check if is beta-barrel, return 100% if it is, 0 if not
def calculate_tmbb_percentage(tmbb):
    result = 0

    if tmbb.is_beta():
        result = 1

    tmbb.set_percentage(result)

    return result

# This calculate percentage for prosite processing
# For each hit, will calculate respective percentage, based on score
# After, returns the maximum percentage calculated on hits
def calculate_final_prosite_percentage(prosite):
    # total 20%
    percentage_final = 0.2

    prosite_hits = prosite.get_hits()
    keywords = []
    best_hit_perc = 0

    if len(prosite_hits) > 0:
        for hit in prosite_hits:
            
            # If no keywords - hit invalid (0%)
            if hit.has_keywords() or hit.has_penalty_keywords():
                keywords += hit.get_keywords()
                keywords += hit.get_penalty_keywords()
                score = hit.get_score()
                hit_perc = 0

                if score >= 18.3:
                    hit_perc = 1

                if score < 18.3 and score >= 14.3:
                    hit_perc = 0.7

                if score < 14.3 and score >= 9.3:
                    hit_perc = 0.3

                if hit_perc >= best_hit_perc:
                    if hit_perc > best_hit_perc:
                        keywords = []
                    best_hit_perc = hit_perc
                    keywords += hit.get_keywords()
                    keywords += hit.get_penalty_keywords()

            hit.set_percentage(best_hit_perc)
    
    percentage_final = percentage_final*best_hit_perc
    keywords = list(set(keywords))

    if len(keywords) > 0:
        penalty = 0
        if keywords.count("enzyme") or keywords.count("transferase"):
            penalty = -0.4
        elif keywords.count("sensor") or keywords.count("transfer"):
            penalty = -0.2

        percentage_final += penalty

        if keywords.count("antiporter") or keywords.count("symporter") or keywords.count("permease") :
            percentage_final += 0.15
    else:
        percentage_final = 0

    if percentage_final < 0:
        percentage_final = 0

    prosite.set_percentage(percentage_final)

    return percentage_final

# This calculate percentage for cdd processing
# For each hit, will calculate respective percentage, based on e-value
# After, returns the maximum percentage calculated on hits
def calculate_final_cdd_percentage(cdd):
    # total 60%
    percentage_final = 0.6
    
    cdd_hits = cdd.get_hits()
    keywords = []
    best_hit_perc = 0

    if len(cdd_hits) > 0:
        for hit in cdd_hits:
            # If no keywords - hit invalid (0%)
            if hit.has_keywords() or hit.has_penalty_keywords():
                evalue = hit.get_evalue()
                hit_perc = 0

                if evalue <= 1e-10:
                    hit_perc = 1

                if evalue > 1e-10 and evalue <= 1e-6:
                    hit_perc = 0.7

                if evalue > 1e-6 and evalue <= 1e-1:
                    hit_perc = 0.3

                if hit_perc >= best_hit_perc:
                    if hit_perc > best_hit_perc:
                        keywords = []
                    best_hit_perc = hit_perc
                    keywords += hit.get_keywords()
                    keywords += hit.get_penalty_keywords()

            hit.set_percentage(best_hit_perc)

    percentage_final = percentage_final*best_hit_perc

    keywords = list(set(keywords))

    if len(keywords) > 0:
        penalty = 0
        if keywords.count("enzyme") or keywords.count("transferase"):
            penalty = -0.4
        elif keywords.count("sensor") or keywords.count("transfer"):
            penalty = -0.2

        percentage_final += penalty

        if keywords.count("antiporter") or keywords.count("symporter") or keywords.count("permease") :
            percentage_final += 0.15
    else:
        percentage_final = 0

    if percentage_final < 0:
        percentage_final = 0

    cdd.set_percentage(percentage_final)

    return percentage_final
