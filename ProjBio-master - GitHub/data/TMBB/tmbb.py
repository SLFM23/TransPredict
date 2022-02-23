import Utils.messages as Messages
import requests
from data.TMBB.TmbbResult import TmbbResult
from bs4 import BeautifulSoup


PREPROCESS_URL = "http://bioinformatics.biol.uoa.gr/PRED-TMBB/preProcess.jsp"
RESULTS_URL = "http://bioinformatics.biol.uoa.gr/PRED-TMBB/process.jsp"

# TMBB process sequence
def process(sequence):
    Messages.tmbb_start()

    try:
        tmbb_result = tmbb_request(sequence)

        return tmbb_result

    except Exception as e:
        print(e)
        Messages.tmbb_error()
        return TmbbResult(True)

# TMBB process request
def tmbb_request(sequence):
    data = {'submit':'Submit', 'force': 'false', 'viterbi': 'on', 'formInput': sequence, 'wait.target': '/PRED-TMBB/process.jsp'}
    pre_req_headers = {'Content-type': 'application/x-www-form-urlencoded'}
    pre_req = requests.post(PREPROCESS_URL, data = data, headers= pre_req_headers)

    if not pre_req.ok:
        Messages.tmbb_error()
        return TmbbResult(True)

    session_cookie = pre_req.headers.get('Set-Cookie', default = None)

    if session_cookie == None:
        Messages.tmbb_error()
        return TmbbResult(True)
    
    params = {'submit': 'Submit', 'force': 'false', 'viterbi': 'on'}
    headers = {'Cookie': session_cookie}

    response = requests.get(RESULTS_URL, params = params, headers = headers)

    if not response.ok:
        Messages.prosite_error()
        return TmbbResult(True)

    html = response.text

    score = parse_request_result(html)
    
    if score == -1:
        Messages.tmbb_error()
        return TmbbResult(True)
    
    tmbbresult = TmbbResult(False, score)
    
    Messages.tmbb_result(tmbbresult)

    return tmbbresult

# Parse TMBB request response - returns score
def parse_request_result(html):
    res = -1

    bs = BeautifulSoup(html, features="html.parser")
    find_scores = bs.find_all('b')

    for f in find_scores:
        try:
            res = float(f.text)
            break
        except:
            continue

    return res
