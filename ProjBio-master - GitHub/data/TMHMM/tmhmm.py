import tmhmm
import Utils.utils as Utils
import Utils.messages as Messages
from data.TMHMM.TmhmmResult import TmhmmResult
import warnings

MODEL_PATH = "data/TMHMM/TMHMM2.0.model"

# TMHMM process sequence
def process(sequence):
    
    try:
        warnings.filterwarnings("ignore")

        Messages.tmhmm_start()

        # TMHMM library processing
        annotation, _ = tmhmm.predict(sequence, "", MODEL_PATH)

        tmhs = Utils.count_group_char(annotation, 'M', 20)

        # Construct TMHMM result object
        tmhmm_result = TmhmmResult(False, tmhs)

        Messages.tmhmm_result(tmhmm_result)

        return tmhmm_result
    except:
        Messages.tmhmm_error()
        return TmhmmResult(True)


