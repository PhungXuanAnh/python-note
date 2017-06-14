'''
Created on Mar 27, 2017

@author: xuananh
'''
import yaml, json

# with open('/media/xuananh/data/Dropbox/Viosoft/Eclipse_workspace/Validium-nfv-mano3/samples/heat-validium1.yaml', 'r') as f:
#     doc = yaml.load(f)
#     print(json.dumps(doc, indent=4, sort_keys=True))
#     
# with open('sample.json', 'w') as out_file:    
#     json.dump(doc,out_file, indent=4)
#     
# with open('sample.yaml', 'w') as out_file:
#     yaml.dump(doc, out_file)

with open('/media/xuananh/data/Dropbox/Viosoft/Eclipse_workspace/Validium-nfv-mano3/samples/heat-validium1.yaml', 'r') as f:
    doc = yaml.load(f)
#     doc = yaml.safe_load(f)
    print(json.dumps(doc, indent=4, sort_keys=True))
    
with open('sample1.json', 'w') as out_file:    
    json.dump(doc,out_file, indent=4)
    
with open('sample1.yaml', 'w') as out_file:
    yaml.dump(doc, out_file)
    
    