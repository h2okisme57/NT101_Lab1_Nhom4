from test_data import *

def json_search(key, input_object):
    ret_val = []

    def _search(target_key, obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == target_key:
                    temp = {k: v}
                    ret_val.append(temp)
                if isinstance(v, (dict, list)):
                    _search(target_key, v)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    _search(target_key, item)

    _search(key, input_object)
    return ret_val

if __name__ == '__main__':
    print(json_search("issueSummary", data))
