import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


verts = [
   (0, 0),  # left, bottom
   (0, 1),  # left, top
    (1, 1),  # right, top
    (1, 0),  # right, bottom
    (0, 0),  # ignored

]

x = 0
y = 0
for i in range (len(verts)-1):
    x+=verts[i][0]
    y+=verts[i][1]
print( x)
print(y)
xPosition = x/(len(verts)-1)
yPosition = y/(len(verts)-1)
print(xPosition)
print(yPosition)
codes = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY,
]
"""

verts = [
   (0., 0.),  # left, bottom
   (0., 1.),  # left, top
   (1., 1.),  # right, top
   (1., 0.),  # right, bottom
   (0., 0.),  # ignored
]

codes = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY,
]
"""
path = Path(verts, codes)

fig = plt.figure()
ax = fig.add_subplot(111)   #I, J, and K integer : the subplot is the Ith plot on a grid with J rows and K columns
patch = patches.PathPatch(path, facecolor='white', lw=2)

ax.add_patch(patch)
ax.text(xPosition,yPosition,"job",horizontalalignment='center',verticalalignment='center')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
plt.show()
