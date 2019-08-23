recheck = True

html = splash:html()
splash:wait(0.5)
while recheck = True:
    splash:wait(0.5)
    html2 = splash:html()
    if html != html2:
       pass
    elif:
       recheck = False
       return {
          html = splash:html(),
         }