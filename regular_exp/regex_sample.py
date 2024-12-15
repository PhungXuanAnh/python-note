import re

"""
reference: 
https://github.com/ziishaned/learn-regex 
https://dev.to/awwsmm/20-small-steps-to-become-a-regex-master-mpc#step11 
https://docs.python.org/3/library/re.html 
https://regex101.com/ 
"""
def re_match():
    line = "Cats are smarter than dogs"

    matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

    if matchObj:
        print("matchObj.groups() : ", matchObj.groups())
        print("matchObj.group()  : ", matchObj.group())
        print("matchObj.group(1) : ", matchObj.group(1))
        print("matchObj.group(2) : ", matchObj.group(2))
    else:
        print("No match!!")

    print('--------------------------------------------------------')

def re_search_and_find_all():
    str1 = """
    https://www.facebook.com/permalink.php?story_fbid=10155920035801729&id=20531316728
    https://www.facebook.com/vtvgiaitri/videos/279319469574649/?__xts__[0]=68.ARCQ67ZrgbOi3NKv6Tzvey1rez0f7ssLZDtUsrkHXJVgEwzizmUbj9HOb3Nx0ulDlLJb_9dqDxJfWPcdBZns-WuvWsAyw6W7-NmgCRX-Gx3ubPTxkax9fD6i6KRVsGUl1XdCM7hxe0snewh8e5ScY9plBGSxn5IPGxvq1x-80ZM8XRtwK3QL&__tn__=-R
    https://www.facebook.com/vtvgiaitri/posts/1685760434867209?__xts__[0]=68.ARDAlOMw7r_nCEFp4b-xcaBoMV1WkDjNM73noeveT1VGYkhE9dKYoilHml8tU8TO_zuy1QCgiuyJr5Z1GRVr94y8YxV-nOoQBKzTuzoTpOZutSx0zvkTViVCYZcfmVg3pyahtK1wyyFwbtq8Qc_7SSAgmS7RsJc2IgBrDRvzUNtiP9CFmOqRdw&__tn__=-R
    """
    print("search and return first match:  ", re.search(r'story_fbid=([0-9]+)&id|/(\d+)[/?]?', str1).group(1))
    print("search and return first match:  ", re.compile(r'story_fbid=([0-9]+)&id|/(\d+)[/?]?').search(str1).group(1))
    print("findall and return all matches: ", re.findall(r'story_fbid=([0-9]+)&id|/(\d+)[/?]?', str1))

def find_and_replace():
    str1 = '&unit_count=123&referrer'
    print("sub: ", re.sub(r'&unit_count=[0-9]+&', '&unit_count=100&', str1))

def find_and_replace_with_replace_func():
    a = 'foo'
    b = 'bar'
    text = 'find a replacement for me [[:a:]] and [[:b:]]'
    def repl(m):
        contents = m.group(1)
        if contents == 'a':
            return a
        if contents == 'b':
            return b
    print(re.sub('\[\[:(.+?):\]\]', repl, text)) # desired output: find a replacement for me foo and bar

re_match()
# re_search_and_findall()
# find_and_replace()
# find_and_replace_with_replace_func()
