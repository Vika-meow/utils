import argparse

parser = argparse.ArgumentParser(description='Get pair entity-category')
parser.add_argument('-f', '--file', help='Entities file', default="kg1_ent_ids")
parser.add_argument('-c', '--categories', help='Categories file', default="article_categories_en.ttl")
parser.add_argument('-o', '--output', help='Output file', default="category_counter")
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

print("categories filtered")
cat_counter = dict()
for v in ent_cat_less.values():
    for cat in v:
        if cat not in cat_counter.keys():
            cat_counter[cat] = 0
        cat_counter[cat] += 1

cat_counter = {k: v for k, v in sorted(cat_counter.items(), key=lambda item: item[1], reverse=True)}
with open(args.output, "w+") as out:
    for k, v in cat_counter.items():
        out.write(k + " - " + str(v) + '\n')