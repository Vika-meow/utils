import numpy as np
import scipy.spatial
import argparse


def loadIds(fn):
        pair = dict()
        with open(fn, encoding='utf-8') as f:
                for line in f:
                        th = line[:-1].split('\t')
                        pair[int(th[1])]=th[0]
        return pair


def findCloseFromDifferentLang(num=10, vec_name="ent_embeds.npy",
                               kg1_ids="kg1_ent_ids", kg2_ids="kg1_ent_ids",
                               metric="cityblock"):
    vec = np.load(vec_name)
    number_of_entities = len(vec)
    print("vectors loaded, number of vectors=" + str(number_of_entities))

    Lvec = np.array([vec[i*2] for i in range(number_of_entities//2)])
    Rvec = np.array([vec[i*2+1] for i in range(number_of_entities//2)])
    print("vectors init...")
    sim = scipy.spatial.distance.cdist(Lvec, Rvec, metric=metric)
    print("metrics are counted...")

    dic_1 = loadIds(kg1_ids)
    dic_2 = loadIds(kg2_ids)

    print("ids loaded")
    while (1):
        print("print entity id ")
        a = int(input())
        if (a > number_of_entities) or (a%2 != 0):
            print("id must be less than " + str(number_of_entities) + " and divide by 2")
            continue
        print(dic_1[a])
        rank = sim[a, :].argsort()
        rank = rank[:num]
        for el in rank:
            print(dic_2[2*el+1] + "\t")


parser = argparse.ArgumentParser(description='Find nearest entities in vector space by id')
parser.add_argument('-p', '--path', help='You can use this argument if all files are in same directory', default="")
parser.add_argument('-v', '--vectors', help='Vectors file', default="ent_embeds.npy")
parser.add_argument('-k1', '--kg1_ids', help='File with name and id of entity from kg1', default="kg1_ent_ids")
parser.add_argument('-k2', '--kg2_ids', help='File with name and id of entity from kg1', default="kg2_ent_ids")
parser.add_argument('-m', '--metric', help='Name of metric', default="cityblock")
args = parser.parse_args()
findCloseFromDifferentLang(vec_name=args.path+args.vectors, kg1_ids=args.path+args.kg1_ids,
                           kg2_ids=args.path+args.kg2_ids, metric=args.metric)