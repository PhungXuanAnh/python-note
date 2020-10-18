import re

line = "Cats are smarter than dogs"

matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

if matchObj:
    print("matchObj.groups() : ", matchObj.groups())
    print("matchObj.group() : ", matchObj.group())
    print("matchObj.group(1) : ", matchObj.group(1))
    print("matchObj.group(2) : ", matchObj.group(2))
else:
    print("No match!!")

print('--------------------------------------------------------')

# https://www.facebook.com/officialdoda/posts/320666585359581
# https://www.facebook.com/officialdoda/posts/2038010436244229

# ------------------ find
str1 = "https://facebook.com/officialdoda/"
print(re.search(r'facebook.com/([a-zA-Z0-9]+)/', str1).group(1))

str1 = """
https://www.facebook.com/permalink.php?story_fbid=10155920035801729&id=20531316728
https://www.facebook.com/vtvgiaitri/videos/279319469574649/?__xts__[0]=68.ARCQ67ZrgbOi3NKv6Tzvey1rez0f7ssLZDtUsrkHXJVgEwzizmUbj9HOb3Nx0ulDlLJb_9dqDxJfWPcdBZns-WuvWsAyw6W7-NmgCRX-Gx3ubPTxkax9fD6i6KRVsGUl1XdCM7hxe0snewh8e5ScY9plBGSxn5IPGxvq1x-80ZM8XRtwK3QL&__tn__=-R
https://www.facebook.com/vtvgiaitri/posts/1685760434867209?__xts__[0]=68.ARDAlOMw7r_nCEFp4b-xcaBoMV1WkDjNM73noeveT1VGYkhE9dKYoilHml8tU8TO_zuy1QCgiuyJr5Z1GRVr94y8YxV-nOoQBKzTuzoTpOZutSx0zvkTViVCYZcfmVg3pyahtK1wyyFwbtq8Qc_7SSAgmS7RsJc2IgBrDRvzUNtiP9CFmOqRdw&__tn__=-R
"""
print("search: ", re.search(r'story_fbid=([0-9]+)&id|/(\d+)[/?]?', str1).group(1))
print("findall: ", re.findall(r'story_fbid=([0-9]+)&id|/(\d+)[/?]?', str1))

# ------------------ replace
str1 = '/pages_reaction_units/more/?page_id=390567570966109&cursor=%7B%22card_id%22%3A%22page_photos%22%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_home&unit_count=8&referrer'
print("sub: ", re.sub(r'&unit_count=[0-9]+&', '&unit_count=100&', str1))

a = 'foo'
b = 'bar'
text = 'find a replacement for me [[:a:]] and [[:b:]]'
desired_output = 'find a replacement for me foo and bar'


def repl(m):
    contents = m.group(1)
    if contents == 'a':
        return a
    if contents == 'b':
        return b


print(re.sub('\[\[:(.+?):\]\]', repl, text))

link = 'https://www.facebook.com/yannews/posts/5721802284557280?__cft__[0]=AZXI_rwwPH21uoOewXjqwlD_KdbFvLSj6yHHYm-7QzxWDa6D5cSC71DTIBlpuQc7xMRfVxY-m3gUYpGbOCfXVGdv-pasymJ7zHBAkCT22NkCs0TinWCp-fndQSIv0RsI9t-37lP9KYS4RBm464zXKa21X1VVIla-ucjzOwfTEldSxcdlyVNEsqa1k36rKFywhRUPyuSD1IxsoIaC3nxMl91EzOiDbGoX_ciiqzXvnVBV3A&__tn__=%2CO%2CP-R'
print("post_id: ", re.search(r'posts/([0-9]+)?', link).group(1))
