from matplotlib.cbook import flatten
import json
import logging
import os

def set_logger(file):
    logger = logging.getLogger(file)
    logger.setLevel(logging.DEBUG)

    # set two handlers
    log_file = "{}.log".format(file)
    cur_dir = os.path.abspath(file).rsplit("/", 1)[0]
    # rm_file(log_file)
    fileHandler = logging.FileHandler(os.path.join(cur_dir, log_file), mode = 'a')
    fileHandler.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # set formatter
    formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # add
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger


def get_initial_response():
    STANDARD_RESPONSE = {
        "error": {
            "code": 200,
            "message": "message",
            "status": "ERROR",
            "details": [
                {
                    "reason": "reason"
                }
            ]
        },
        "data": {}
    }
    return STANDARD_RESPONSE


def format_errors(errors):
    error = []
    keys = list(errors.keys())
    values = list(errors.values())
    for i in range(0, len(errors)):

        error.append((str(keys[i]))+": "+str(values[i][0]))
    return error


def format_error_blockchain(errors):

    error = str(errors[0]).replace("\'", "\"")
    print("====")
    print(error)
    error = json.loads(error)
    error["when"] = errors[1]
    final = error["message"]+" when "+error["when"]
    return [final]
