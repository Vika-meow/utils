import numpy as np
import matplotlib.cm as cm
import matplotlib as mpl

#x = [[1,1,1], [1,2,1], [9,1,5], [7,1,13]]
#np.save("out_ae", x)


norm = mpl.colors.Normalize(vmin=0, vmax=750)
cmap = cm.hot
m = cm.ScalarMappable(norm=norm, cmap=cmap)
print(type(m.to_rgba(100)))