import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


# Usage:
d = Decimal("42.5")
print(json.dumps(d, cls=DecimalEncoder))
