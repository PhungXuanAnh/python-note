"""
    co the tham khao day: https://stackoverflow.com/a/43473532/7639845
"""

import requests
url = 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=100'  # the form's action url
par = {"email": "sigmasolutions.test@gmail.com", "password": "Sigma2017"}  # the forms parameters

data = {
    'jazoest': 2754,
    'lsd': 'AVqAnzYh',
    'legacy_return': 0,
    'display': None,
    'enable_profile_selector': None,
    'isprivate': None,
    'profile_selector_ids': None,
    'return_session': None,
    'skip_api_login': None,
    'signed_next': None,
    'trynum': 1,
    'timezone': -420,
    'lgndim': 'eyJ3IjoxOTIwLCJoIjoxMDgwLCJhdyI6MTkyMCwiYWgiOjEwNTMsImMiOjI0fQ==',
    'lgnrnd': '024950_LVhH',
    'lgnjs': 1574246991,
    'email': 'sigmasolutions.test@gmail.com',
    'pass': 'Sigma2017',
    'prefill_contact_point': 'sigmasolutions.test@gmail.com',
    'prefill_source': 'browser_dropdown',
    'prefill_type': 'password',
    'first_prefill_source': 'browser_dropdown',
    'first_prefill_type': 'contact_point',
    'had_cp_prefilled': 'true',
    'had_password_prefilled': 'true',
    'ab_test_data': 'AAAA/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//AAAAABAAB'
}

headers = {
    'authority': 'www.facebook.com',
    'cache-control': 'max-age=0',
    'viewport-width': '1920',
    'origin': 'https://www.facebook.com',
    'upgrade-insecure-requests': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'sec-fetch-user': '?1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'referer': 'https://www.facebook.com/login.php?login_attempt=1',
    # accept-encoding:gzip, deflate, br
    'accept-language': 'en,vi;q=0.9',
    # 'cookie':'fr=1h0Qxipit3YMMr1LG..Bd1RpO.jr.AAA.0.0.Bd1RpO.AWWuXLPI; sb=ThrVXWB3Ldw_inVTqD-IVwWI; datr=ThrVXbOjVC5j0R0uU0pXcIcN; wd=818x949; act=1574247012621%2F3'
}
# r = requests.post(url, data=par)
# print(r.status_code)
# # print(r.content)  # you can't use r.text because of encoding
# # print(r.cookies)

# cookieJar = r.cookies
# print(cookieJar.get_dict())

# for cookie in cookieJar:
#     print(cookie.name)

IS_CHECK_COOKIE = False     
'''`
CHÚ Ý: đặt tên IS_CHECK_COOKIE thế này cho dễ hiểu, set param "verify" bên dưới là false để
disable check cookie trong khi chạy request, nếu không bó sẽ báo là trình duyệt
của bạn chưa bật cookie, cái này check bằng cách ghi r.text ra file rồi mở lên sẽ thấy
'''

# s = requests.Session()
# r = s.get('https://www.facebook.com', verify=IS_CHECK_COOKIE)
# r = s.post(url, data=data, headers=headers, verify=IS_CHECK_COOKIE)
# print(r.status_code)
# print(r.cookies.get_dict())
# r1 = s.get('https://www.facebook.com/pg/Cristiano/posts/', verify=IS_CHECK_COOKIE)
# print(r1.status_code)
# # print(r1.text)
# with open('/home/xuananh/data/Temp/temp.html', 'w+') as f:
#     f.write(r1.text)

r2 = requests.get('https://www.walmart.ca/en/clothing-shoes-accessories/men/mens-tops/N-11+2566', verify=IS_CHECK_COOKIE)
with open('/home/xuananh/data/Temp/temp.html', 'w+') as f:
    f.write(r2.text)
