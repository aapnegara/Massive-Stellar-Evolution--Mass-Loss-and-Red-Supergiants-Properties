# coding: utf-8

# In[30]:


## IMPORTANDO BIBLIOTECAS

import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
import math as mth
import pandas as pd
import datetime as dt

# In[31]:



def init_plotting(x=9,y=7):
    plt.rcParams['figure.figsize'] = (x,y)
    plt.rcParams['font.size'] = 20
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
    plt.rcParams['legend.fontsize'] = 13
    plt.rcParams['legend.loc'] = 'best'
    plt.rcParams['axes.linewidth'] = 1

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


# In[32]:
#DATA DE HOJE
today = dt.datetime.today()
today_str = today.strftime('%m%d%y')
# In[]:

## ABRINDO OS DADOS DOS MODELOS MESA
mass_list = [20,30,40,50,60]
models_list = [mr.MesaData("%iM0/LOGS/history.data" % mass) for mass in mass_list]
colorlist = ["lime","C9","purple","brown","black"]

# In[33]:


## ABRINDO DADOS DA EKSTROM (GENEC)
ste_list = [pd.read_csv("f%i.mw.track.dat" % mass,sep=" ",index_col=False) for mass in mass_list]

# In[]
[plt.plot(models_list[i].log_Teff[23:],models_list[i].log_L[23:],color = colorlist[i], label = '$MESA: %iM_{\odot}$' % mass_list[i]) for i in range(len(models_list))]
[plt.plot(np.log10(ste_list[i]["3:Teff[K]"][:-15]),ste_list[i]["4:log(L/Lsun)"][:-15],color = colorlist[i],linestyle="--", label = '$STERN: %iM_{\odot}$' % mass_list[i]) for i in range(len(ste_list))]

ste_list[0]

plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
plt.title("Diagrama HR  [L .vs. $T_{eff}]$")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.ylabel("$log_{10}(L/L_{\odot})$")
plt.xlim([4.7,4.1])

# plt.gca().invert_xaxis()
plt.ylabel("Massa [$M_{\odot}$]")
plt.xlabel("$log_{10}(T_{eff}/K)$")

plt.savefig("HR.png",bbox_inches='tight')

# In[]
tH25M0_index_Gen = gen25CenH.index(0.0)
tH25M0_index_MESA = m25.center_h1.tolist().index(0.0)

tH32M0_index_Gen = gen32CenH.index(0.0)
tH32M0_index_MESA = m32.center_h1.tolist().index(0.0)

tH40M0_index_Gen = gen40CenH.index(0.0)
tH40M0_index_MESA = m40.center_h1.tolist().index(0.0)

tH50M0_index_Gen = gen50CenH.index(0.0)
tH50M0_index_MESA = m50.center_h1.tolist().index(0.0)

tH60M0_index_Gen = gen60CenH.index(0.0)
tH60M0_index_MESA = m60.center_h1.tolist().index(0.0)

#
listTH_gen = [gen25Age[tH25M0_index_Gen],gen32Age[tH32M0_index_Gen],gen40Age[tH40M0_index_Gen],gen50Age[tH50M0_index_Gen],gen60Age[tH60M0_index_Gen]]
listTH_MESA = [m25.star_age[tH25M0_index_MESA],m32.star_age[tH32M0_index_MESA],m40.star_age[tH40M0_index_MESA],m50.star_age[tH50M0_index_MESA],m60.star_age[tH60M0_index_MESA]]

listDifPC = [100*(listTH_gen[i]-listTH_MESA[i])/listTH_gen[i] for i in range(5)]


for mass in range(len(mass_list)):
	plt.scatter(mass_list[i],(listTH_MESA[i]-listTH_gen[i])*100/listTH_gen[i],color = colorlist[i],s= 300)

# plt.xticks([3e6,4e6,5e6,6e6,7e6,8e6],['$3$','$4$','$5$','$6$','$7$','$8$'])
# plt.yticks([3e6,4e6,5e6,6e6,7e6,8e6],['$3$','$4$','$5$','$6$','$7$','$8$'])

# plt.ylim([-10,10])
plt.ylabel('$\Delta t_{H} \, / \, t_{H}^{GENEC} \, (\%)$')
plt.xlabel('$M/M_{\odot}$')
# plt.plot([3000000,8000000],[3000000,8000000],color = '#111111')
plt.plot([70,20],[0,0],color = '#111111')
plt.grid(color='grey', linestyle='--', linewidth=.5)
# plt.xlim([3000000,8000000])
plt.xlim([20,70])
plt.ylim([-10,10])
plt.yticks([-10,-5,0,5,10])
plt.xticks(l,['25','32','40','50','60'])
