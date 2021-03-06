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
parser.add_argument('-mm', '--metameta', help='Meta info about meta files', default="meta_meta")
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
    if len(x) != 0:
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
print("firstly categories collected ents_num = " + str(len(ent_cat_less)) + " cats_num = " + str(len(categories)))

delete_keys = set()
for n, x in categories.items():
    if n not in delete_keys:
        for k, y in categories.items():
            if k != n:
                for cat in y:
                    if cat in x:
                        x.update(y)
                        delete_keys.add(k)
                        break

for k in delete_keys:
    del categories[k]


print("end collect categories cats_num = " + str(len(categories)))
#print_dict_with_set(categories)
print("start writing file")
flag = 0
with open(args.output, 'w+') as out:
    with open("test", 'w+') as test:
        for key, values in ent_cat_less.items():
            if len(values) != 0:
                for num, cats in categories.items():
                    for val in values:
                        if val in cats:
                            if flag != 1:
                                out.write(str(num) + '\n')
                                flag = 1
                            #test.write(key + '\t' + str(num) + '\n')
                            break
                    if flag == 1:
                        break
            else:
                out.write(str(0) + '\n')
                #test.write(key + '\t' + str(0) + '\n')
            flag = 0
print("categories write in " + args.file)

with open(args.meta, 'w+') as out:
    for k, v in categories.items():
        el = ""
        for z in v:
            el += z + " "
        out.write(str(k) + " " + el + '\n')
print("categories meta write in " + args.meta)

#count number of categories in claster
categories_in_claster_counter = dict()
for k, v in categories.items():
    categories_in_claster_counter[k] = len(v)
print("count categories in each claster")
#count number of entities in each claster
number_of_entity_in_claster = dict()
with open(args.output, "r") as input:
    for line in input:
        cat = int(line)
        if cat not in number_of_entity_in_claster.keys():
            number_of_entity_in_claster[cat] = 0
        number_of_entity_in_claster[cat] += 1
number_of_entity_in_claster = {k: v for k, v in sorted(number_of_entity_in_claster.items(), key=lambda item: item[1], reverse=True)}
print("count entities in each claster")

categories_in_claster_counter[0] = 0
with open(args.metameta, 'w+') as out:
    out.write("claster - number of entities - number of categories\n")
    for k, v in number_of_entity_in_claster.items():
        el = str(k) + " - " + str(v) + " - " + str(categories_in_claster_counter[k]) + '\n'
        out.write(el)
print("meta info in " + args.metameta)

'''
print("start collect categories for each entity")
# ?????? ?????????????? ???????????????? ???????????????? ??????????????????, ?????????????? ???????????????????????? ????????????
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
# ???????????? ?????????????????? ???????????????????? ?????????????????????? ????????
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