# import glob, os
# os.chdir("/media/xuananh/data/Temp/yardstick/yardstick/benchmark/scenarios/networking")
# for file in glob.glob("*.py"):
#     print(file)

# import os
# for file in os.listdir("/media/xuananh/data/Temp/yardstick/yardstick/benchmark/scenarios/networking"):
#     if file.endswith(".py"):
#         print(os.path.join("/mydir", file))

import os
import glob
import json

for root, dirs, files in os.walk("/media/xuananh/data/Downloads/plugin_tmp"):
    for file in files:
        if file.endswith(".zip"):
            print(os.path.join(root, file))
            
    print (root, dirs, files)
    
print (os.walk("/media/xuananh/data/Downloads/plugin_tmp"))
            
print("==========================================================================================")            
# scenario_bash_files = glob.glob(
#     os.path.join("/media/xuananh/data/Temp/yardstick/yardstick/benchmark/scenarios/networking", "*.bash"))
scenario_bash_files = glob.glob("/media/xuananh/data/Temp/yardstick/yardstick/benchmark/scenarios/networking/*.py")
print (json.dumps(scenario_bash_files, indent=4, sort_keys=True))         








