import json
from urllib import parse

url = "https://www.facebook.com/pages_reaction_units/more/?page_id=254639978334701&cursor=%7B%22timeline_cursor%22%3A%22timeline_unit%3A1%3A00000000001502166456%3A04611686018427387904%3A09223372036854775778%3A04611686018427387904%22%2C%22timeline_section_cursor%22%3A%7B%7D%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_posts&unit_count=8&__a=1&__user=0"
url1 = "https://www.facebook.com/pages_reaction_units/more/?page_id=254639978334701&cursor=%7B%22timeline_cursor%22%3A%22timeline_unit%3A1%3A00000000001492414999%3A04611686018427387904%3A09223372036854775762%3A04611686018427387904%22%2C%22timeline_section_cursor%22%3A%7B%22profile_id%22%3A254639978334701%2C%22start%22%3A0%2C%22end%22%3A1556693999%2C%22query_type%22%3A36%2C%22filter%22%3A1%7D%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_posts&unit_count=8&__a=1&__user=0"
url2 = "https://www.facebook.com/pages_reaction_units/more/?page_id=154228448495780&cursor=%7B%22timeline_cursor%22%3A%22timeline_unit%3A1%3A00000000001507692466%3A04611686018427387904%3A09223372036854775756%3A04611686018427387904%22%2C%22timeline_section_cursor%22%3A%7B%22profile_id%22%3A154228448495780%2C%22start%22%3A0%2C%22end%22%3A1556693999%2C%22query_type%22%3A36%2C%22filter%22%3A1%7D%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_posts&unit_count=8&__a=1&__user=0"
url3 = "https://www.facebook.com/photo.php?fbid=2791943630816329&amp;set=pcb.2791943664149659&amp;type=3&amp;__tn__=HH-R&amp;eid=ARA3CxZ2m8dgFd6cghe7n58RqVdU1A0HeeEh71OlR57aKXXsXEYvnM-Q7PTaxJ2ZZ129gWldPPLWmTqT&amp;__xts__%5B0%5D=68.ARBEYlQlP_9wfRixFjG-PzTR3zfh8HsBAYREOYXUmECKZAW9chHne-mkI_gA2ceUqij9eBHKDlXqhtMlCvA7naqCylGOtaADbAlCxL4MpJUxlirAvvUeT0yZ5BqTnOAIqhelA3d2QLcDJ6zE2-LnWAFZuDtGY4LxLpz_X98P8aXS8fSL-_CWR_qn95eZn-fYE5HENE004ZfisTTUaY-D-04meuwFgBGB6SKzR7WVBeEDDyIZX8xdy0VQSFTbHz_oJlthpS4ipRcxCUgDxlRvLUM2JECVngMSs010f_SkWktD0NjgW3a6SmBbgk_wMNOU7fwnA3UVGA91M8O0Yxoo2JOfmg"

# print(parse.urlsplit(url))

print(parse.parse_qs(parse.urlsplit(url).query))

p = dict(parse.parse_qsl(parse.urlsplit(url).query))
p1 = dict(parse.parse_qsl(parse.urlsplit(url1).query))
p2 = dict(parse.parse_qsl(parse.urlsplit(url2).query))
p3 = dict(parse.parse_qsl(parse.urlsplit(url3).query))

print(json.dumps(json.loads(p['cursor']), indent=4, sort_keys=True))
print(json.dumps(json.loads(p1['cursor']), indent=4, sort_keys=True))
print(json.dumps(json.loads(p2['cursor']), indent=4, sort_keys=True))
print(json.dumps(p3, indent=4, sort_keys=True))
