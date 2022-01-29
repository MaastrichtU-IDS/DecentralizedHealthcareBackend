from matplotlib.cbook import flatten
import json



def get_initial_response():
    STANDARD_RESPONSE = {
                            "error": {
                                "code":200,
                                "message":"message",
                                "status":"ERROR",
                                "details":[
                                    {
                                        "reason":"reason"
                                    }
                                ]
                            },
                            "data":{}
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
    error["when"]= errors[1]
    final = error["message"]+" when "+error["when"]
    return [final]
