import argparse

parser = argparse.ArgumentParser(description='Vizualize with TSNE')
parser.add_argument('-f', '--file', help='Entities file', default="out_ae.npy")