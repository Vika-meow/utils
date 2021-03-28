import argparse


def print_dict_with_set(dic=dict()):
    for x, y in dic.items():
        el = ""
        for z in y:
            el += z + " "
        print(str(x) + " " + el)


parser = argparse.ArgumentParser(description='Get pair entity-category')
parser.add_argument('-f', '--file', help='Entities file', default="kg1_ent_ids")
parser.add_argument('-c', '--categories', help='Categories file', default="article_categories_en.ttl")
parser.add_argument('-l', '--language', help='Language of categories', default="en")
parser.add_argument('-o', '--output', help='Output file', default="out_categories")
parser.add_argument('-m', '--meta', help='Meta info about categories', default="meta_categories")
args = parser.parse_args()

ent_cat = dict()
print("start loading categories")
with open(args.categories, encoding='utf-8') as cat_file:
    for line in cat_file:
        triple = line[:-1].split(' ')
        if triple[0][1:-1] not in ent_cat:
            ent_cat[triple[0][1:-1]] = set()
        ent_cat[triple[0][1:-1]].add(triple[2])
print("categories loaded")

ent_cat_less = dict()
print("start load entities")
with open(args.file, encoding='utf-8') as f:
    for line in f:
        ent = line[:-1].split('\t')[0]
        if ent in ent_cat:
            ent_cat_less[ent] = ent_cat[ent]
        else:
            ent_cat_less[ent] = set()

ent_cat.clear()
print("entities loaded + " + str(len(ent_cat_less)))
categories = dict()
counter = 0
flag = 0

print("start collect categories")
for x in ent_cat_less.values():
    for y in categories.values():
        for cat in x:
            if cat in y:
                flag = 1
                y.update(x)
                break
        if flag == 1:
            break
    if flag == 0:
        counter += 1
        categories[counter] = x
        #print(str(counter))
    flag = 0

print("end collect categories ents_num = " + str(len(ent_cat_less)) + " cats_num = " + str(len(categories)))
#print_dict_with_set(categories)
print("start writing file")
flag = 0
with open(args.output, 'w+') as out:
    for key, values in ent_cat_less.items():
        if len(values) != 0:
            for num, cats in categories.items():
                for val in values:
                    if val in cats:
                        if flag != 1:
                            out.write(str(num) + '\n')
                            flag = 1
                        #out.write(key + '\t' + str(num) + '\n')
                        break
                if flag == 1:
                    break
        else:
            out.write(str(0) + '\n')
            #out.write(key + '\t' + str(0) + '\n')
        flag = 0
print("end writing file")
'''
print("start collect categories for each entity")
# для каждого элемента собираем категории, которые используются вместе
for x in ent_cat_less.values():
    for y in ent_cat_less.values():
        for cat in y:
            if cat in x:
                x.update(y)
                break
    #print("entity " + x + " done")

i = 0
for x, y in ent_cat_less.items():
    el = ""
    for e in y:
        el += e + " "
    print(x + ' ' + el)
    i += 1
    if(i > 10):
        break

print("end collect categories for each entity")
print("start id-category")
# теперь собранным категориям присваиваем айди
for x in ent_cat_less.values():
    for z in categories.values():
        for cat in x:
            if cat in z:
                z.update(x)
                flag=1
                break
    if flag == 0:
        counter += 1
        categories[counter] = x
    flag = 0

print("end id-category")
print("start writing file")
with open(args.output, 'w+') as out:
    for key, values in ent_cat_less.items():
        if len(values) != 0:
            for num, cats in categories.items():
                for val in values:
                    if val in cats:
                        out.write(str(num) + '\n')
                        #out.write(key + '\t' + str(num) + '\n')
                        break
        else:
            out.write(str(0) + '\n')
            #out.write(key + '\t' + str(0) + '\n')

print("end writing file")
'''
#with open(args.meta, 'w+') as out:
#    for x, y in categories.items():
#        el = ""
#        for e in y:
#            el += e + " "
#        out.write(str(x) + ' ' + el + '\n')