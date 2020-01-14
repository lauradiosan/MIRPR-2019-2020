"""Time utils."""
from dateutil.parser import _timelex
import dateutil.parser as dparser


def timesplit(input_string):
    """Helper method used by __extract_dates."""
    batch = []
    for token in _timelex(input_string):
        if token in ['to', 'and']:
            yield " ".join(batch)
            batch = []
            continue
        if timetoken(token):
            if dparser.parser().info.jump(token):
                continue
            batch.append(token)
        else:
            if batch:
                yield " ".join(batch)
                batch = []
    if batch:
        yield " ".join(batch)


def timetoken(token):
    """Helper method used by __timesplit."""
    try:
        float(token)
        return True
    except ValueError:
        pass

    info = dparser.parser().info
    return any(f(token) for f in (info.jump, info.weekday, info.month, \
                                  info.hms, info.ampm, info.pertain, \
                                  info.utczone, info.tzoffset))
