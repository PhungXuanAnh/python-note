import json
from jsonpath_rw import jsonpath, parse

json_str = """
{
    "foo": 
        [
            {
                "baz": 11
            }, 
            {
                "baz": 22
            }
        ]
}
"""

dict_t = json.loads(json_str)

jsonpath_expr = parse('foo[*].baz')

for match in jsonpath_expr.find(dict_t):
    print('match.value: ', match.value)

for match in jsonpath_expr.find(dict_t):
    print('match.full_path: ', match.full_path)



