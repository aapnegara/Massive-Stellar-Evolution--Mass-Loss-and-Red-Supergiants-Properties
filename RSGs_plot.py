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
    plt.rcParams['legend.fontsize'] = 8
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
mass_list = [12,15,20,25,32,40,60]
models_list = [mr.MesaData("Models/%i/history.data" % mass) for mass in mass_list]
colorlist = ["red","orange","C8","green","blue","purple","black"]

# In[33]:


## ABRINDO DADOS DA EKSTROM (GENEC)
gen12Data = pd.read_csv("External_Data/M012Z14V4.dat")
gen15Data = pd.read_csv("External_Data/M015Z14V4.dat")
gen20Data = pd.read_csv("External_Data/M020Z14V4.dat")
gen25Data = pd.read_csv("External_Data/M025Z14V4.dat")
gen32Data = pd.read_csv("External_Data/M032Z14V4.dat")
gen40Data = pd.read_csv("External_Data/M040Z14V4.dat")

# In[34]:


## PEGANDO DADOS DAS RSGs DA TABELA DA LEVESQUE

t4LData = pd.read_csv("External_Data/tabela4_Levesque.csv")

#--------------------------------------------------------------
#extrair logg_modelo, logg_teorico e R/R0
# Star,SpecTypel,Teff,AV,Model,Actual,Actual_2,R/R0,R/R0_2,MV,Mbol,Mbol_2,DeltaAV
t4LLog_gM = t4LData['logg_Model']
t4LLog_gA = t4LData['logg_Actual']
t4LR_R0 = t4LData['R/R0']
t4LLog_gA2 = t4LData['logg_Actual_2']
t4LTeff = t4LData['Teff']
t4LM_bol = t4LData['Mbol']

## OBTENDO PROPRIEDADES INDIRETAS DAS RSGs DOS DADOS DA LEVESQUE

#-------|MASSA ESPECTRAL A PARTIR DA FORMULA M = 10^log(g)R^2/G|-----
#lembrar que esta tudo em cgs!

t4LLog_Teff = np.log10(t4LTeff)
t4LData["Log_Teff"] = t4LLog_Teff

gA = 10**t4LLog_gA
gM = 10**t4LLog_gM

mspecA = (((t4LR_R0*R0)**2)*(gA)/G_)/M0
mspecM = (((t4LR_R0*R0)**2)*(gM)/G_)/M0

#-----------|LUMINOSIDADE|--------------------------------
t4LLog_L_L0 = np.log10(10**((t4LM_bol-M_bol_SUN)/-2.5))
print(t4LLog_L_L0)
t4LData["logL_L0"] = t4LLog_L_L0
sig_Log_Teff = 75*1/(10**t4LLog_Teff*np.log(10))
t4LData["sig_Log_Teff"] = sig_Log_Teff
sig_Log_L_L0 = 0.09*0.4
t4LData["sig_logL_L0"] = sig_Log_L_L0

#-----------|MASSA ATRAVES DE MBOL|--------------------------------
m_by_mbol = 10**(0.50 - 0.10*t4LM_bol)
t4LData["mass_Mbol"] = m_by_mbol
sig_m_by_mbol = np.sqrt(0.09*(0.530189*np.e**(-0.460518*t4LM_bol)))
t4LData["sig_mass_Mbol"] = sig_m_by_mbol
sig_Log_g = np.sqrt(4/(25*(mth.log(10))**2) + (sig_m_by_mbol*M0/(M0*m_by_mbol*np.log(10)))**2)

t4LData.to_csv("t4Levesque2.csv",sep=",")

#================================================================================

# In[]

index_within_list = []
for iml in range(len(models_list)):
    for iLv in range(len(t4LLog_Teff)):
        for im in range(len(models_list[iml].log_Teff)):
            if t4LLog_Teff[iLv] + sig_Log_Teff[iLv] > models_list[iml].log_Teff[im] and m_by_mbol[iLv] - sig_m_by_mbol[iLv] < models_list[iml].star_mass[im]:
                if iLv not in index_within_list:
                    index_within_list.append(iLv)
                break


# In[]
index_without_list = list(range(len(t4LLog_gA2)))
[index_without_list.remove(i) for i in index_within_list]
print(index_without_list)
# In[]
print(len(index_within_list),len(t4LLog_gA2))
[plt.plot(models_list[i].log_Teff,models_list[i].star_mass,color = colorlist[i], label = '$%iM_{\odot}$' % mass_list[i]) for i in range(len(models_list[:-1]))]

[plt.fill_between(models_list[i].log_Teff,models_list[i].star_mass, color = 'pink',alpha=0.7) for i in range(len(models_list))[:-1]]

plt.fill_between(models_list[5].log_Teff[0:-29],models_list[5].star_mass[0:-29], color = 'pink',alpha=0.7)


# plt.scatter(t4LLog_Teff,m_by_mbol,color = 'red')
[plt.scatter(t4LLog_Teff[i],m_by_mbol[i],color = 'red',marker = 'v') for i in index_without_list]
plt.scatter(t4LLog_Teff[index_without_list[1]],m_by_mbol[index_without_list[1]], marker = 'v',color = 'red', label = "Não explicado: "+str(len(index_without_list)))
[plt.scatter(t4LLog_Teff[i],m_by_mbol[i],color = 'blue') for i in index_within_list]
plt.scatter(t4LLog_Teff[index_within_list[1]],m_by_mbol[index_within_list[1]],color = 'blue', label = "Explicado: "+str(len(index_within_list)))
plt.errorbar(t4LLog_Teff, m_by_mbol,yerr = sig_m_by_mbol , xerr = sig_Log_Teff,ls='none', c = 'gray',zorder = -32,label = '_nolegend_')

plt.legend(bbox_to_anchor=(1,1))
plt.title("Diagrama Massa .vs. $T_{eff}$")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.ylabel("$log_{10}(M/M_{\odot})$")
plt.plot([3.7,3.7],[0,65],color="fuchsia")
plt.ylim(9,42)
plt.xticks([4.6,4.4,4.2,4.0,3.8,3.7,3.6])
plt.gca().invert_xaxis()
plt.savefig("Images/MxT_%s.png" % today_str,bbox_inches='tight')
plt.show()
# In[]

[plt.plot(models_list[i].log_Teff,models_list[i].log_L, label = '$%iM_{\odot}$' % mass_list[i], color = colorlist[i]) for i in range(len(models_list))]

[plt.scatter(t4LLog_Teff[i],t4LLog_L_L0[i],color = 'red',marker = 'v') for i in index_without_list]
plt.scatter(t4LLog_Teff[index_without_list[1]],t4LLog_L_L0[index_without_list[1]], marker = 'v',color = 'red', label = "Não explicado ($M \, x \, T_{eff}$) : "+str(len(index_without_list)))
[plt.scatter(t4LLog_Teff[i],t4LLog_L_L0[i],color = 'blue') for i in index_within_list]
plt.scatter(t4LLog_Teff[index_within_list[1]],t4LLog_L_L0[index_within_list[1]],color = 'blue', label = "Explicado ($M \, x \, T_{eff}$): "+str(len(index_within_list)))
plt.errorbar(t4LLog_Teff, t4LLog_L_L0,yerr = sig_Log_L_L0 , xerr = sig_Log_Teff,ls='none', c = 'gray',zorder = -32,label = '_nolegend_')

plt.legend(bbox_to_anchor=(1,1))
plt.title("Diagrama HR  [L .vs. $T_{eff}]$")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.ylabel("$log_{10}(L/L_{\odot})$")
plt.plot([3.7,3.7],[0,6.8],color="fuchsia")
plt.ylim(3.8,6.6)
plt.xticks([4.6,4.4,4.2,4.0,3.8,3.7,3.6])
plt.gca().invert_xaxis()
plt.savefig("Images/HR_%s.png" % today_str,bbox_inches='tight')


# In[]
[plt.plot(models_list[i].log_Teff,models_list[i].star_age,color = colorlist[i], label = '$%iM_{\odot}$' % mass_list[i]) for i in range(len(models_list))]

plt.gca().invert_xaxis()
plt.ylabel("Massa [$M_{\odot}$]")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.legend()
plt.savefig("Images/Txt_%s.png" % today_str,bbox_inches='tight')
plt.show()

# In[]
[plt.plot(models_list[i].center_he4,models_list[i].log_Teff,color = colorlist[i], label = '$%iM_{\odot}$' % mass_list[i]) for i in range(len(models_list))]

plt.ylabel("Massa [$M_{\odot}$]")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.legend()
plt.xlim(1.01,-0.01)
plt.plot([-0.1,1.1],[3.7,3.7],color="fuchsia")
plt.savefig("Images/TxHe_%s.png" % today_str,bbox_inches='tight')
plt.show()
# In[]

l_i_lTeff37 = []
l_teff_min = [models_list[i].log_Teff.tolist().index(min(models_list[i].log_Teff)) for i in range(len(models_list))]
l_rsg = []
for i_mod in range(len(models_list)):
    for i_lTeff in range(len(models_list[i_mod].log_Teff)):
        if models_list[i_mod].log_Teff[i_lTeff] < 3.7:
            l_i_lTeff37.append(i_lTeff)
            l_rsg.append(i_mod)
            break


[plt.plot(10**np.log10(models_list[i].star_age[l_i_lTeff37[l_rsg.index(i)]:]),models_list[i].star_mass[l_i_lTeff37[l_rsg.index(i)]:],label = '$%iM_{\odot}$' % mass_list[i], color = colorlist[i]) for i in l_rsg]

[plt.fill_between(10**np.log10(models_list[i].star_age[l_i_lTeff37[l_rsg.index(i)]:]),models_list[i].star_mass[l_i_lTeff37[l_rsg.index(i)]:],color=colorlist[i],alpha=0.7) for i in l_rsg]

[plt.scatter(10**np.log10(models_list[i].star_age[l_i_lTeff37[l_rsg.index(i)]]),models_list[i].star_mass[l_i_lTeff37[l_rsg.index(i)]],marker='v',s=80,color = colorlist[i]) for i in l_rsg]
# [plt.scatter(np.log10(models_list[i].star_age[l_teff_min[i]]),models_list[i].star_mass[l_teff_min[i]],marker=ms_vector[i%3],s=80,color = colorlist[i]) for i in range(len(models_list))]

print((models_list[4].star_age[-1]-models_list[4].star_age[l_i_lTeff37[4]])/models_list[4].star_age[-1]) 
print(models_list[4].star_mass[0])

plt.scatter(-100,-100,marker='v',s=80,color = "grey",label="$log_{10}(T_{eff}/K) = 3.7 \, \, |$ Início como RSG")

plt.title("Evolução Temporal da Massa após tornar-se RSG")
plt.xlabel("$t [yr]$")
plt.ylabel("$M \, [M_{\odot}]$")
# plt.xlim((6.55,7.32))
plt.xlim((0.4e7,2e7))
plt.ylim((9,30))

plt.legend(bbox_to_anchor=(1,1))
plt.savefig("Images/Mxt_%s.png" % today_str,bbox_inches='tight')
