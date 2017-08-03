import glob

result = glob.iglob('../*.py')

print result #<generator object iglob at 0x02587648>

for file in result:
    print file