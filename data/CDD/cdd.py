import Utils.messages as Messages
import Utils.utils as Utils
from data.CDD.CddResult import CddResult
from data.CDD.CddHit import CddHit
import requests
import time
from bs4 import BeautifulSoup

CDD_URL = "https://www.ncbi.nlm.nih.gov/Structure/bwrpsb/bwrpsb.cgi"

CDD_HIT_DESCRIPTION_URL = "https://www.ncbi.nlm.nih.gov/Structure/cdd/cddsrv.cgi?ascbin=8&maxaln=10&seltype=2"

CDD_HIT_KEYWORDS = ['transport', 'channel', 'permease', 'pump', 'facilitator', 'symporter', 'uniporter', 'antiporter', 'porin', 'carrier', 'influx', 'eflux', 'import', 'export']

CDD_PENALTY_KEYWORDS = ['transfer', 'enzyme', 'sensor', 'transferase']

CDD_SPECIAL_KEYWORDS = ['atp binding', 'atp-binding']

# CDD Process
def process(sequence):
    Messages.cdd_start()

    try:
        cdd_result = cdd_request(sequence)

        return cdd_result

    except Exception as e:
        print(e)
        Messages.cdd_error()
        return CddResult(True)

# Request CDD process
# 3 Steps, 1- start sequence process, 2- Check processing sequence, 3- Get Process result (2 & 3 on same request)
def cdd_request(sequence):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    request_data = {
        'queries': sequence,
        'useid1': True,
        'maxhit': 250,
        'filter': True,
        'db': 'cdd',
        'evalue': 0.01,
        'cddefl': False,
        'qdefl': False,
        'dmode': 'rep',
        'clonly': False,
        'tdata': 'hits'
    }

    pre_req = requests.post(CDD_URL, data = request_data, headers= headers)

    if not pre_req.ok:
        Messages.cdd_error()
        return CddResult(True)

    cdsid = None

    for line in pre_req.text.split("\n"):
        if line.find("cdsid") > -1:
            cdsid = line.split("cdsid")[1].strip()
            break

    if cdsid == None:
        Messages.cdd_error()
        return CddResult(True)

    time.sleep(3) # wait 3 seconds
    i = 0
    params = {'cdsid': cdsid}
    result_data = None

    # For each status check request, wait seconds seconds
    seconds = 6
    while i<10:
        i += 1
        resp = requests.get(CDD_URL, params=params)

        # Check request status result
        process = cdd_req_status_process(resp)

        # Check process status is already done
        if process.isDone():
            result_data = process.getData()
            break
        
        # Check process status occurred an error
        if process.isError():
            break

        # By default process is still running

        time.sleep(seconds)

    if result_data == None:
        Messages.cdd_error()
        return CddResult(True)

    if len(result_data) == 0:
        return CddResult(False)

    # CDD result process
    hits = cdd_process_result(result_data)
    counthits = len(hits)

    Messages.cdd_hits(counthits, hits)

    return CddResult(False, counthits, hits)

# Process and parser cdd processing result
def cdd_process_result(data):
    indexes = []
    hits = []
    result = []

    for l in data:
        datal = l.split("\t")

        if datal[0][:5] == "Query":
            indexes = datal
        
        if datal[0][:2] == "Q#":
            hits.append(datal)

    # Construct hits objects with information
    for h in hits:
        evalue = 0.0
        accession = ""
        superfamily = ""
        name = ""

        for i,k in enumerate(h):
            
            if indexes[i] == "Short name":
                name = k

            if indexes[i] == "Accession":
                accession = k
            
            if indexes[i] == "Superfamily":
                superfamily = k

            if indexes[i] == "E-Value":
                evalue = float(k)

        cddHit = CddHit(evalue, name, accession, superfamily)
        
        cdd_hit_keywords(cddHit)

        result.append(cddHit)

    return result

# Request to fetch hit keywords match
def cdd_hit_keywords(cddHit):
    accession = cddHit.get_accession()
    match_keywords_list = []
    penalty_keywords_list = []
    cddHit.set_keywords(match_keywords_list)
    cddHit.set_penalty_keywords(penalty_keywords_list)

    params = {'uid': accession}
    resp = requests.get(CDD_HIT_DESCRIPTION_URL, params=params)

    if not resp.ok:
        return

    html = resp.text

    bs = BeautifulSoup(html, features="html.parser")
    description_section = bs.find("section", {"id": "description"})

    if description_section == None:
        return

    description_section = description_section.find("div", {"class": "inner"})

    keywords_text = description_section.parent.text.lower()

    keywords_match = Utils.search_keywords(CDD_HIT_KEYWORDS, keywords_text)
    penalty_keywords_match = Utils.search_keywords(CDD_PENALTY_KEYWORDS, keywords_text)

    # Remove 'binding' keyword from penalty keywords if some of the special keywords exists
    if Utils.has_substrings(keywords_text, CDD_SPECIAL_KEYWORDS) and 'binding' in penalty_keywords_match:
        penalty_keywords_match.remove('binding')

    cddHit.set_keywords(keywords_match)
    cddHit.set_penalty_keywords(penalty_keywords_match)

# Process CDD request current status of process
def cdd_req_status_process(req_result):
    result = CddStatusRequestResponse()
    
    if not req_result.ok:
        result.setError()
        return result

    text = req_result.text

    statuscode = '-1'
    lines = text.split("\n")

    for line in lines:
        if line.find("status") > -1:
                statuscode = line.split("\t")[1].strip()   #0 - success, 2 - no input, 3 - running, 1,4,5 are errors
                break

    if statuscode in ['-1', '1', '4', '5']:
        result.setError()
        return result

    if statuscode == '3':
        return result

    result.setDone()
    if statuscode == '2':
        return result

    result.setData(lines)

    return result


# Class to represent status of CDD process request
class CddStatusRequestResponse():
    Pending = "Pending"
    Error = "Error"
    Done = "Done"    

    def __init__(self, data = []):
        self.status = self.Pending
        self.data = data

    def getStatus(self):
        return self.status

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def isPending(self):
        return self.status == self.Pending
    
    def isDone(self):
        return self.status == self.Done

    def isError(self):
        return self.status == self.Error
    
    def setError(self):
        self.status = self.Error

    def setDone(self):
        self.status = self.Done