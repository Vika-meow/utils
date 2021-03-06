import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.lines import Line2D
import argparse

color_en = "#001eff"
color_ru = "#ff0000"

def loadIds(fn):
    pair = dict()
    with open(fn, encoding='utf-8') as f:
        for line in f:
            th = line[:-1].split('\t')
            pair[int(th[0])] = th[1]
    print('loaded ids...' + fn)
    return pair

def tsne_plot_2d(label, embeddings, words=[], a=1, cat_col=[]):
    print('start configure plot')
    plt.figure(figsize=(16, 9))
    x = embeddings[:,0]
    y = embeddings[:,1]
    plt.scatter(x, y, c=cat_col, s = 100)
    print('start annotate')
    #for i, word in enumerate(words):
    #    plt.annotate(word, alpha=0.3, xy=(x[i], y[i]), xytext=(5, 2),
    #                 textcoords='offset points', ha='right', va='bottom', size=10)
    print('end annotate')
    legend_elements = [Line2D([0], [0], marker='o', color=color_en, label='en'),
                       Line2D([0], [0], marker='o', color=color_ru, label='ru')]
    plt.legend(handles=legend_elements, loc=4)
    #plt.legend(loc=4)
    plt.grid(True)
    plt.savefig(label+".png", format='png', dpi=150, bbox_inches='tight')
    plt.show()

def visualize(vec_file = "out_ae.npy", cat_file = "", name = "visualize"):
    vectors = np.load(vec_file)
    print('loaded vectors... num = ' + str(len(vectors)))
    dic = []
    result = []
    if cat_file != "":
        norm = mpl.colors.Normalize(vmin=0, vmax=750)
        cmap = cm.hot
        m = cm.ScalarMappable(norm=norm, cmap=cmap)
        with open(cat_file, "r") as cat_file:
            for line in cat_file:
                cat_num = int(line)
                if cat_num != 147:
                    dic.append(m.to_rgba(int(line)))
                else:
                    dic.append((0,0,0,0))

        i = 0
        for el in dic:
            result.append(el)
        for el in dic:
            result.append(el)
        print("colors generated...")
    else:
        for i in range(len(vectors) // 2):
            result.append(color_en)
        for i in range(len(vectors) // 2):
            result.append(color_ru)
    #dic_1 = loadIds("data/ru_en/ent_ids_1")
    #dic_2 = loadIds("data/ru_en/ent_ids_2")
    #dic_1.update(dic_2)
    #dic_ids = dic_1
    words = []
    embeddings = []
    i = 0
    for vec in vectors:
        embeddings.append(vec)
        words.append(i)
        i += 1
    tsne_ak_2d = TSNE(n_components=2, init='pca', n_iter=3500, random_state=32)
    print('set settings for TSNE')
    embeddings_ak_2d = tsne_ak_2d.fit_transform(embeddings)
    print('get new embeddings in 2dims')
    tsne_plot_2d(name, embeddings_ak_2d, words, a=0.1, cat_col=result)

def main():
    parser = argparse.ArgumentParser(description='Vizualize with TSNE')
    parser.add_argument('-f', '--file', help='Entities file', default="out_ae.npy")
    parser.add_argument('-c', '--categories', help='Categories file', default="")
    parser.add_argument('-n', '--name', help='Output name', default="visualize")
    args = parser.parse_args()
    visualize(vec_file=args.file, cat_file=args.categories, name = args.name)

if __name__ == "__main__":
    main()
