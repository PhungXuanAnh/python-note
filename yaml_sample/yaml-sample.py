import yaml
import json

# read
with open('input.yaml', 'r') as f:
    doc = yaml.safe_load(f)
    print(json.dumps(doc, indent=4, sort_keys=True))

# write to yaml file
with open('output.yaml', 'w') as out_file:
    yaml.safe_dump(doc, out_file)

# write to json file
with open('output.json', 'w') as out_file:
    json.dump(doc, out_file, indent=4)
