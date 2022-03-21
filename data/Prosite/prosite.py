import requests
import Utils.messages as Messages
import Utils.utils as Utils
from data.Prosite.PrositeResult import PrositeResult
from data.Prosite.PrositeHit import PrositeHit
from bs4 import BeautifulSoup

PROSITE_URL = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi"
PROSITE_PROFILES_URL = "https://prosite.expasy.org/cgi-bin/prosite/nicedoc.pl?"

PROSITE_HIT_KEYWORDS = ['transport', 'channel', 'permease', 'pump', 'facilitator', 'symporter', 'uniporter', 'antiporter', 'porin', 'carrier', 'influx', 'eflux', 'import', 'export', 'importer', 'exporter', 'uptake']

PROSITE_PENALTY_KEYWORDS = ['transfer', 'enzyme', 'sensor', 'transferase']

PROSITE_SPECIAL_KEYWORDS = ['atp binding', 'atp-binding']

# Prosite process sequence
def process(sequence):
    Messages.prosite_start()

    try:
        prosite_result = prosite_request(sequence)

        return prosite_result

    except Exception as e:
        print(e)
        Messages.prosite_error()
        return PrositeResult(True)

# Prosite request processing
def prosite_request(sequence):
    data = {'seq': sequence, 'output': 'json'}
    prosite_req_headers = {'Content-type': 'application/x-www-form-urlencoded'}

    prosite_response = requests.post(PROSITE_URL, data = data, headers=prosite_req_headers)

    if not prosite_response.ok:
        Messages.prosite_error()
        return PrositeResult(True)

    response_dict = prosite_response.json()

    number_hits = 0
    hits = []

    matchset = response_dict.get('matchset', [])

    for h in matchset:
        score = h.get('score', None)
        code = h.get('signature_ac', None)

        if score != None:
            number_hits += 1
            keywords,penalty_keywords = prosite_hit_keywords(code)
            hit = PrositeHit(score, code, keywords, penalty_keywords)
            hits.append(hit)

    Messages.prosite_hits(number_hits)
    
    Messages.prosite_hits_data(hits)

    return PrositeResult(False, number_hits, hits)

# Prosite keywords search
def prosite_hit_keywords(profile_code):
    result = []
    penalty_result = []

    url = PROSITE_PROFILES_URL + profile_code

    prosite_response = requests.get(url)

    if not prosite_response.ok:
        return result,penalty_result

    html = prosite_response.text

    bs = BeautifulSoup(html, features="html.parser")
    description_section = bs.find(property="schema:description")

    if description_section == None:
        return result,penalty_result

    description =  description_section.text.lower()

    keywords_match = Utils.search_keywords(PROSITE_HIT_KEYWORDS, description)
    penalty_keywords_match = Utils.search_keywords(PROSITE_PENALTY_KEYWORDS, description)

    # Remove 'binding' keyword from penalty keywords if some of the special keywords exists
    if Utils.has_substrings(description, PROSITE_SPECIAL_KEYWORDS) and 'binding' in penalty_keywords_match:
        penalty_keywords_match.remove('binding')


    return keywords_match,penalty_keywords_match
