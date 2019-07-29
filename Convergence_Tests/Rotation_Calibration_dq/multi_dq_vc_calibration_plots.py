# coding: utf-8

# In[30]:


## IMPORTANDO BIBLIOTECAS

import mesa_reader as mr
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math as mth
import pandas as pd
import matplotlib.ticker as fmt
import matplotlib.cm as cm

# In[31]:



def init_plotting(x=9,y=7):
    plt.rcParams['figure.figsize'] = (x,y)
    plt.rcParams['font.size'] = 15
    plt.rcParams['figure.facecolor'] = '#dddddd'
    # plt.rcParams['font.family'] = 'Asana Math'
    plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 0.75*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = 0.65*plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.fontsize'] = 8
    plt.rcParams['legend.loc'] = 'best'
    plt.rcParams['axes.linewidth'] = 1
    mpl.rc('text', usetex=False)
    # mpl.rcParams['text.latex.preamble'] = [r'\boldmath']

init_plotting()

## CONSTANTES ASTROFISICAS

G_ = 6.67259e-8 #cm^3 g^-1 s^-1
c = 2.99792458e10 #cm/s
h = 6.6260755e-27 #erg*s
k_b = 1.380658e-16 #erg/K
b = 2.8977685e-1 #cm*K
G = 6.674e-8 #cm(3).g(-1).s(-2)
sb = 5.67e-5 #erg.cm(-2).K(-4)
L0 = 3.9e33 #erg.s(-1)
M0 = 1.99e33 #g
R0 = 6.96e10 #cm
M_bol_SUN = 4.74

mass_vector = ("12", "15", "20", "25", "32", "40", "60")
dq_vector = ("0.0005", "0.001","0.005")

# In[32]:
models_array = [[mr.MesaData("multi_dq_vc_calibration/LOGS_all_masses/LOGS_%sM0_dq%s_vc1e-4/history.data" % (mass, dq)) for mass in mass_vector] for dq in dq_vector]

colors_list_l = ['fuchsia','r']
colors_list_h = ['orange','brown','green','blue']
label_list_l = ["$%i M_{\odot}$" % mass for mass in (12,15)]
label_list_h = ["$%i M_{\odot}$" % mass for mass in (20, 25, 32, 40, 60)]
# In[34]:
vrot0_array = [[models_array[q][m].surf_avg_v_rot[0] for m in range(len(mass_vector))] for q in range(len(dq_vector))]
vrot0_array_vc5 = [[models_array_vc5[q][m].surf_avg_v_rot[0] for m in range(len(mass_vector))] for q in range(len(dq_vector))]
vrot0_dif = (np.array(vrot0_array)-np.array(vrot0_array_vc5))/np.array(vrot0_array_vc5)
vrot0_mean_dq = [(models_array[0][m].surf_avg_v_rot[0] + \
                models_array[1][m].surf_avg_v_rot[0] + \
                models_array[2][m].surf_avg_v_rot[0]
                )/3 for m in range(len(mass_vector))]

vrot0_dif2_dq = [[(vrot0_array[q][m]-vrot0_mean_dq[m])**2 for q in range(len(dq_vector))] for m in range(len(mass_vector))]
vrot0_Dp_dq = [[np.sqrt(np.array(sum(vrot0_dif2_dq[m])/2)) for m in range(len(mass_vector))]]

# In[]

fig, ax = plt.subplots()
fig.patch.set_facecolor('white')
left  = 0.125
right = 0.9
bottom = 0.1
top = 0.8
wspace = 0.3
hspace = 0.2

plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=wspace)
plt.title('Diferentes Resoluções e Rotações Equatoriais Iniciais', fontsize=16)

plt.subplot(211)
plt.imshow(vrot0_array,cmap = cm.copper)
plt.colorbar(orientation = 'horizontal').set_label('Rotação Equatorial Inicial')# \n $\mathbf{vc}$ = 1e-4')
[plt.plot([i+0.5,i+0.5],[2.5,-0.5],c='k') for i in range(6)]
[plt.plot([-0.5,6.5],[i-0.5,i-0.5],c='k') for i in range(3)]
plt.ylabel('$max\_dq}$')
plt.yticks((0,1,2),['0.5e-3','1e-3','5e-3'])
plt.xticks((0,1,2,3,4,5,6),["$12M_{\odot}$","$15M_{\odot}$","$20M_{\odot}$","$25M_{\odot}$","$32M_{\odot}$","$40M_{\odot}$","$60M_{\odot}$"])

plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=wspace)

plt.subplot(212)
plt.yticks([])
plt.xticks((0,1,2,3,4,5,6),["$12M_{\odot}$","$15M_{\odot}$","$20M_{\odot}$","$25M_{\odot}$","$32M_{\odot}$","$40M_{\odot}$","$60M_{\odot}$"])
plt.imshow(vrot0_Dp_dq,cmap = cm.summer)
cax = ax.imshow(np.array(vrot0_Dp_dq)*1e5, cmap=cm.summer)
cbar = fig.colorbar(cax, orientation='horizontal',fraction = 0.6)

cbar.set_label("Desvio Padrão da Rotação para Diferentes Resoluções $\mathbf{\cdot 10^{-5}}$")

[plt.plot([i+0.5,i+0.5],[0.5,-0.5],c='k') for i in range(6)]

plt.tight_layout()
plt.savefig("multi_dq_vc_calibration_fig.png")
plt.show()
