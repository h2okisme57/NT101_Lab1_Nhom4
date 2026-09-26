from test_data import *
from policy import POLICY


def json_search(key, input_object, role=None):
    '''Recursively collect every {key: value} pair found in a nested
    dict/list structure (input_object) and return them as a list.

    Access control is enforced here and is deny-by-default (SR-1..SR-4):
    when ``key`` is protected by ``POLICY`` the caller must pass a role
    that is explicitly allow-listed for that key. ``role=None``
    (unauthenticated) or any role that is not allow-listed returns an
    empty list, so a sensitive value can never leak - not even when it
    is buried deep inside nested dicts/lists.
    '''
    # Deny by default: protected keys require an explicitly granted role.
    if key in POLICY and role not in POLICY[key]:
        return []

    ret_val = []

    def _search(target_key, obj):
        # Inner function: each json_search() call builds its own ret_val in
        # this closure, so nested/parallel calls never share or leak state
        # (fixes the recursion bug of the original implementation).
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
    print(json_search("issueSummary", data, role="admin"))
