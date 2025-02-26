import matplotlib.pyplot as plt
import pandas as pd

df_ffa = pd.read_csv('PATH/TO/COORDS.csv',sep=';',header=0)
df_naca63018 = pd.read_csv('PATH/TO/COORDS.csv',sep=';',header=0)

fig,ax = plt.subplots(figsize=(5,3))
ax.scatter(df_ffa['x/c'],df_ffa['y/c'],marker='x',color='black',label="FFA W3 211",s=8,alpha=0.8)
ax.scatter(df_naca63018['x/c'],df_naca63018['y/c'],marker='o',color='blue',label="NACA63018",s=8,alpha=0.8)

ax.set_xlabel('x/c')
ax.set_ylabel('y/c')
ax.set_xlim((0,1.0))
ax.axis('equal')
ax.grid('minor')
ax.set_axisbelow(True)
ax.legend()
fig.tight_layout()
fig.show()
fig.savefig('profiles.pdf', format='pdf', bbox_inches='tight')