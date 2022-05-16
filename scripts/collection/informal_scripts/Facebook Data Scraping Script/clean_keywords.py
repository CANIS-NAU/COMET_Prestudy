keywords = []

with open('keywords.txt', 'r') as file:
    for line in file:
        line = line.replace(' \n', '')
        if line == '\n':
            continue
        if line.endswith(' '):
            line = line[:-1]
        if line.count(' ') > 0:
            keywords.append(line.lower()+'\n')
            line = line.replace(' ', '')
        if (line.lower()+'\n') not in keywords:
            keywords.append(line.lower()+'\n')

f = open('clean_keywords.txt', 'w')

for keyword in keywords:
    f.write(keyword)

f.close()