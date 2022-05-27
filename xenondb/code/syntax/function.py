import re
if __name__ == "__main__":
    x = "a   b"
    tmp = x.split(' ')
    print(x.split(' '))
    for i in tmp:
        print(i.strip())

    a = r'(UPDATE|update)(.*)(SET|set)(.*)'
    p = re.compile(a)
    statement = "update table set a = 1, c = 4 where b = 2"
    tmp = p.findall(statement)
    print(tmp)
    ##filter space
    tmp2 = statement.split("where")[0]
    print(tmp2)
    tmp2 = tmp2.split(" ")
    ret = []
    for i in tmp2:
        if i.strip() == '' or x.strip() == 'AND':
            continue
        ret.append(i)
    statement = ' '.join(ret)
    print(statement)
    # b = "asd, sdf, sdf"
    # print([i.strip() for i in b.split(",")])
    aa = re.compile(a).findall(statement)
    print(aa)


    ret = []
    condition = "b = 2 AND 'i' in (aa, bb)"

    for i in condition.split(" "):
        if i.strip() == '' or i.strip() == "AND":
            continue
        ret.append(i)
    print(ret)

    a = input('\033[00;37misadb> ')
    print(a)

