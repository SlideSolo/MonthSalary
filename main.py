import xml.etree.ElementTree as ElementTree
import urllib.request as request
from datetime import date

d = date.today()
curr_date = d.strftime("%d/%m/%Y")
url_currency = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' + curr_date + '&date_req2=' \
               + curr_date + '&VAL_NM_RQ=R01035'


def parse(xmldata):
    currency_items = []
    et = ElementTree.fromstring(xmldata)

    for currency in et:
        for prop in currency:
            if prop.tag == 'Value':
                currency_items.append(float(prop.text.replace(',', '.')))
    return currency_items


response = request.urlopen(url_currency, timeout=10)

gbp = 0

for i in parse(response.read()):
    gbp = i

salary = float(input('Enter your salary per year:'))

# 1.Employee personal allowance 12570 per year
# 2.English and Northern Irish basic tax rate up to 37700 - 20%
# 3.English and Northern Irish higher tax rate - 40% on annual earnings from £37,701 to £150,000
# 4.English and Northern Irish additional tax rate - 45% on annual earnings above £150,000
limits = {"allowance": 12570.0, "basic": 37700.0, "higher": 150000.0}
rates = {"basic": 20.0, "higher": 40.0, "over": 45.0}

next_step = False
basic_base = 0.0
higher_base = 0.0
over_base = 0.0
salary_rest = salary


if salary_rest >= limits["allowance"]:
    salary_rest = salary - limits["allowance"]
    next_step = True

if next_step:
    if salary_rest >= limits["basic"]:
        salary_rest -= limits["basic"]
        basic_base = limits["basic"]
    else:
        next_step = False

if next_step:
    if salary_rest <= (limits["higher"]-limits["basic"]):
        higher_base = salary_rest
        salary_rest = 0.0
    else:
        salary_rest -= limits["higher"]
        higher_base = limits["higher"]

if salary_rest > 0:
    over_base = salary_rest
    salary_rest = 0

basic_tax_value = basic_base * (rates["basic"]/100)
higher_tax_value = higher_base * (rates["higher"]/100)
over_tax_value = over_base * (rates["over"]/100)

total_tax = basic_tax_value + higher_tax_value + over_tax_value
salary -= total_tax
salary *= 0.89  # Britain FSS
salary_ip = salary * 0.94  # NDFL 6%
salary *= 0.87  # NDFL 13%

print("НДФЛ 13%: " + str((float(salary) * gbp)/12))
print("НДФЛ 6%: " + str((float(salary_ip) * gbp)/12))
