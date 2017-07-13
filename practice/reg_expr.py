import re

one_line = "<span><li>219.153.76.77</li></span>"
pattern1 = re.compile(r'<span><li>(\d*).(\d*).(\d*).(\d*)</li></span>')

print 'match1'
match1 = pattern1.match(one_line)
if match1:
    print match1.group(1)
    print match1.group(2)
    print match1.group(3)
    print match1.group(4)

print 'match2'
pattern2 = re.compile(r'<span><li>(\d*.\d*.\d*.\d*)</li></span>')
match2 = pattern2.match(one_line)
if match2:
    print match2.group(1)
else:
    print 'no match found'

print 'match3'
another_line = '<span style="width: 100px;"><li class="port GEGEA">8621</li></span>'
pattern3 = re.compile(r'<span[\S|\s]*><li[\S|\s]*>(\d+)</li></span>')
match3 = pattern3.match(another_line)
if match3:
    print match3.group(1)
else:
    print 'no match found'

print 'search1'
pattern4 = re.compile(r'>(\d+)<')
match4 = pattern4.search(another_line)
if match4:
    print match4.group(1)
else:
    print 'no match found'

print 'findall'
more_lines = '<span style="width: 100px;"><li class="port GEGEA">8621</li></span><span style="width: 100px;"><li class="port GEGEA">8872</li></span>'
pattern5 = re.compile(r'>(\d+)<')
match5 = pattern5.findall(more_lines)
if match5:
    for items in match5:
        print items
else:
    print 'no match found'

