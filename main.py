from lxml import etree
import os

DIR = 'chile_work'
SECTIONS = 7

list_dir = os.listdir(DIR)
result = {}
for work in list_dir:
    name = work.split('.')[0]
    if not work.endswith('.work.xml'):
        if name.capitalize() not in result:
            result[name.capitalize()] = {"total": "<<>>", "OK": "<<>>", "mark": 2}
        #print(f"{name:18s}\t <<>> \t<<>>\t{2}")
        continue
    tree = etree.parse(f'{DIR}/{work}')
    root = tree.getroot()

    tests = {}

    for i in root:
        if i.tag == "MARKS":
            for j in i:
                #print(j.attrib['testId'], j.attrib['mark'])
                test = tests.get(j.attrib['testId'][0], [0, 0])
                test[0] += 1
                test[1] += int(j.attrib['mark'])
                tests[j.attrib['testId'][0]] = test

    tests_solved = [y[0] for x, y in tests.items()]
    total =  sum([y[1] for x, y in tests.items()])
    ok = ["Not 7", "7OK"][(all(map(lambda x: x >= 3, tests_solved)) and len(tests_solved) == SECTIONS)]

    mark =  5 if ok and total >= 30 * SECTIONS else\
            4 if ok and total > 25 * SECTIONS else\
            3 if total > 15 * SECTIONS else 2

    #print(f"{name:18s}\t {total} \t{ok}\t{mark}")

    if name.capitalize() not in result:
        result[name.capitalize()] = {"total": total, "OK": ok, "mark": mark}
    else:
        if result[name.capitalize()]["mark"] < mark:
            result[name.capitalize()] = {"total": total, "OK": ok, "mark": mark}

## print protocol
print(f'{"Pupil":18s}\t Total \t OK \t Mark')
for pupil in result:
    print(f"{pupil:18s}\t {result[pupil]["total"]} \t{result[pupil]["OK"]}\t{result[pupil]["mark"]}")
