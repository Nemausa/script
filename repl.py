import re
from calendar import month_abbr, month_name

def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))
    

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
newtext = datepat.sub(change_date, text)
print(newtext)


dic = {}
dic['origin'] = 'now'
def change(m):
    return dic[m.group(0)]

pat = re.compile(r'(?<=>).*(?=<)')
line = r'<string name="export">origin</string>'
newline = pat.sub(change, line)
print(newline)

# output
# Today is 27 Nov 2012. PyCon starts 13 Mar 2013.
# now

# need
# Today is 27 Nov 2012. PyCon starts 13 Mar 2013.
# <string name="export">now</string>


