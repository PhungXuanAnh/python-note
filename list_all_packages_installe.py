import pip, json
installed_packages = pip.get_installed_distributions()
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
     for i in installed_packages])
print json.dumps(installed_packages_list, indent=4, sort_keys=True)
