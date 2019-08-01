# coding: utf-8

# In[30]:


## IMPORTANDO BIBLIOTECAS

import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
import math as mth
import pandas as pd

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


## ABRINDO OS DADOS DOS MODELOS MESA

m9 = mr.MesaData("9M0/LOGS/history.data")

m12 = mr.MesaData("12M0/LOGS/history.data")

m15 = mr.MesaData("15M0/LOGS/history.data")

m20_2 = mr.MesaData("20M0/LOGS/history_cool.data")
m20_1 = mr.MesaData("20M0/LOGS/history_initial.data")

m25_1 = mr.MesaData("25M0/LOGS/history_initial.data")
m25_2 = mr.MesaData("25M0/LOGS/history_cool.data")

m32_1 = mr.MesaData("32M0/LOGS/history_initial.data")

m40_1 = mr.MesaData("40M0/LOGS/history_1.data")



# In[33]:


## ABRINDO DADOS DA EKSTROM (GENEC)

gen9Data = pd.read_csv("External_Data/M009Z14V4.dat")
gen9LogTeff = gen9Data['lg(Teff)']
gen9LogL = gen9Data['lg(L)']
gen9Mass = gen9Data['mass']
gen9Age = gen9Data['time']
gen9VEq = gen9Data['v_equa']
gen9LogTc = gen9Data['lg(Tc)']

gen12Data = pd.read_csv("External_Data/M012Z14V4.dat")
gen12LogTeff = gen12Data['lg(Teff)']
gen12LogL = gen12Data['lg(L)']
gen12Mass = gen12Data['mass']
gen12Age = gen12Data['time']
gen12VEq = gen12Data['v_equa']
gen12LogTc = gen12Data['lg(Tc)']

gen15Data = pd.read_csv("External_Data/M015Z14V4.dat")
gen15LogTeff = gen15Data['lg(Teff)']
gen15LogL = gen15Data['lg(L)']
gen15Mass = gen15Data['mass']
gen15Age = gen15Data['time']
gen15VEq = gen15Data['v_equa']
gen15LogTc = gen15Data['lg(Tc)']

gen20Data = pd.read_csv("External_Data/M020Z14V4.dat")
gen20LogTeff = gen20Data['lg(Teff)']
gen20LogL = gen20Data['lg(L)']
gen20Mass = gen20Data['mass']
gen20Age = gen20Data['time']
gen20VEq = gen20Data['v_equa']
gen20LogTc = gen20Data['lg(Tc)']

gen25Data = pd.read_csv("External_Data/M025Z14V4.dat")
gen25LogTeff = gen25Data['lg(Teff)']
gen25LogL = gen25Data['lg(L)']
gen25Mass = gen25Data['mass']
gen25Age = gen25Data['time']
gen25VEq = gen25Data['v_equa']
gen25LogTc = gen25Data['lg(Tc)']

gen32Data = pd.read_csv("External_Data/M032Z14V4.dat")
gen32LogTeff = gen32Data['lg(Teff)']
gen32LogL = gen32Data['lg(L)']
gen32Mass = gen32Data['mass']
gen32Age = gen32Data['time']
gen32VEq = gen32Data['v_equa']
gen32LogTc = gen32Data['lg(Tc)']

gen40Data = pd.read_csv("External_Data/M040Z14V4.dat")
gen40LogTeff = gen40Data['lg(Teff)']
gen40LogL = gen40Data['lg(L)']
gen40Mass = gen40Data['mass']
gen40Age = gen40Data['time']
gen40VEq = gen40Data['v_equa']
gen40LogTc = gen40Data['lg(Tc)']

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
t4LData["Log_Teff"] = t4t4LLog_Teff

gA = 10**t4LLog_gA
gM = 10**t4LLog_gM

mspecA = (((t4LR_R0*R0)**2)*(gA)/G_)/M0
mspecM = (((t4LR_R0*R0)**2)*(gM)/G_)/M0

#-----------|LUMINOSIDADE|--------------------------------
t4LLog_L_L0 = np.log10(10**((t4LM_bol-M_bol_SUN)/-2.5))
t4LData["L_L0"] = t4t4LLog_L_L0
sig_Log_Teff = 75*1/(10**t4LLog_Teff*np.log(10))
t4LData["sig_Log_Teff"] = sig_Log_Teff
sig_Log_L_L0 = 0.09*0.4


#-----------|MASSA ATRAVES DE MBOL|--------------------------------
m_by_mbol = 10**(0.50 - 0.10*t4LM_bol)
t4LData["mass_Mbol"] = m_by_mbol
sig_m_by_mbol = np.sqrt(0.09*(0.530189*np.e**(-0.460518*t4LM_bol)))
t4LData["sig_mass_Mbol"] = sig_m_by_mbol
sig_Log_g = np.sqrt(4/(25*(mth.log(10))**2) + (sig_m_by_mbol*M0/(M0*m_by_mbol*np.log(10)))**2)

#================================================================================

## DIAGRAMA HR (1x)
plt.title('HR Diagram')

plt.plot(gen9LogTeff,gen9LogL,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen12LogTeff,gen12LogL,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen15LogTeff,gen15LogL,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen20LogTeff,gen20LogL,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen25LogTeff,gen25LogL,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen32LogTeff,gen32LogL,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen40LogTeff,gen40LogL,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')

plt.plot(m9.log_Teff, m9.log_L,c='purple',linewidth=1.3,alpha = 1,label = '$9M_{\odot}$')
plt.plot(m12.log_Teff, m12.log_L,c='red',linewidth=1.3,alpha = 1,label = '$12M_{\odot}$')
plt.plot(m15.log_Teff, m15.log_L,c='orange',linewidth=1.3,alpha = 1,label = '$15M_{\odot}$')
plt.plot(m20_1.log_Teff, m20_1.log_L,c='yellow',linewidth=1.3,alpha = 1,label = '$20M_{\odot}$')
plt.plot(m20_2.log_Teff, m20_2.log_L,c='yellow',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m25_1.log_Teff, m25_1.log_L,c='lime',linewidth=1.3,alpha = 1,label = '$25M_{\odot}$')
plt.plot(m25_2.log_Teff, m25_2.log_L,c='lime',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m32_1.log_Teff, m32_1.log_L,c='green',linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(m40_1.log_Teff, m40_1.log_L,c='blue',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')

plt.xlabel('$Log(T_{eff}/K)$')
plt.ylabel('$L/L_{\odot}$')

plt.plot([3.7,3.7],[0,6.1],c = 'purple',linewidth=0.8)

plt.scatter(t4LLog_Teff,t4LLog_L_L0, c = 'lime', label = 'Levesque+')
plt.errorbar(t4LLog_Teff, t4LLog_L_L0,yerr = sig_Log_L_L0 , xerr = sig_Log_Teff,ls='none', c = 'gray',zorder = -32,label = '_nolegend_')

plt.ylim(3.5,6.1)
plt.xlim(4.7,3.5)
plt.legend()
plt.savefig('Images/HR.png')
plt.show()
plt.clf()

#---------------------------------------------------------------------------------------
## Mass x LogTeff
plt.title('Mass vs. Effective Temperature')

# plt.plot(gen12LogTeff,gen12Mass,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen12LogTeff,gen12Mass,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen15LogTeff,gen15Mass,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen20LogTeff,gen20Mass,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen25LogTeff,gen25Mass,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen32LogTeff,gen32Mass,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen40LogTeff,gen40Mass,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')

plt.plot(m9.log_Teff, m9.star_mass,c='purple',linewidth=1.3,alpha = 1,label = '$9M_{\odot}$')
plt.plot(m12.log_Teff, m12.star_mass,c='red',linewidth=1.3,alpha = 1,label = '$12M_{\odot}$')
plt.plot(m15.log_Teff, m15.star_mass,c='orange',linewidth=1.3,alpha = 1,label = '$15M_{\odot}$')
plt.plot(m20_1.log_Teff, m20_1.star_mass,c='yellow',linewidth=1.3,alpha = 1,label = '$20M_{\odot}$')
plt.plot(m20_2.log_Teff, m20_2.star_mass,c='yellow',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m25_1.log_Teff, m25_1.star_mass,c='lime',linewidth=1.3,alpha = 1,label = '$25M_{\odot}$')
plt.plot(m25_2.log_Teff, m25_2.star_mass,c='lime',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m32_1.log_Teff, m32_1.star_mass,c='green',linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(m40_1.log_Teff, m40_1.star_mass,c='blue',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$'

plt.scatter(t4LLog_Teff,m_by_mbol, c = 'lime', label = 'Levesque+2005', edgecolors='black')
plt.errorbar(t4LLog_Teff, m_by_mbol,yerr = sig_m_by_mbol , xerr = sig_Log_Teff,ls='none', c = 'gray',zorder = -32,label = '_nolegend_')

plt.xlabel('$Log(T_{eff}/K)$')
plt.ylabel('$M/M_{\odot}$')

plt.plot([3.7,3.7],[0,38],c = 'blue',linewidth=0.8)

plt.ylim(2,36)
plt.xlim(4.65,3.5)
plt.xticks([4.5, 4.3, 4.1, 3.9, 3.7, 3.5])
plt.legend(ncol = 6)
plt.savefig('Images/MassxLogTeff.svg')
plt.show()
plt.clf()

#---------------------------------------------------------------------------------------
## Mass x Age
plt.title('Mass Evolution in Time')

plt.plot(gen9Age,gen9Mass,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen12Age,gen12Mass,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen15Age,gen15Mass,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen20Age,gen20Mass,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen25Age,gen25Mass,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen32Age,gen32Mass,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen40Age,gen40Mass,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')

plt.plot(m9.star_age, m9.star_mass,c='purple',linewidth=1.3,alpha = 1,label = '$9M_{\odot}$')
plt.plot(m12.star_age, m12.star_mass,c='red',linewidth=1.3,alpha = 1,label = '$12M_{\odot}$')
plt.plot(m15.star_age, m15.star_mass,c='orange',linewidth=1.3,alpha = 1,label = '$15M_{\odot}$')
plt.plot(m20_1.star_age, m20_1.star_mass,c='yellow',linewidth=1.3,alpha = 1,label = '$20M_{\odot}$')
plt.plot(m20_2.star_age, m20_2.star_mass,c='yellow',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m25_1.star_age, m25_1.star_mass,c='lime',linewidth=1.3,alpha = 1,label = '$25M_{\odot}$')
plt.plot(m25_2.star_age, m25_2.star_mass,c='lime',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m32_1.star_age, m32_1.star_mass,c='green',linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(m40_1.star_age, m40_1.star_mass,c='blue',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')

plt.xlabel('$Time (yr)$')
plt.ylabel('$M/M_{\odot}$')

plt.legend()
plt.savefig('Images/MassxTime.png')
plt.show()
plt.clf()

#---------------------------------------------------------------------------------------
## LogTeff x Age
plt.title('LogTeff Evolution')

plt.plot(gen9Age,gen9LogTeff,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen12Age,gen12LogTeff,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen15Age,gen15LogTeff,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen20Age,gen20LogTeff,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen25Age,gen25LogTeff,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen32Age,gen32LogTeff,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen40Age,gen40Mass,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')

plt.plot(m9.star_age, m9.log_Teff,c='purple',linewidth=1.3,alpha = 1,label = '$9M_{\odot}$')
plt.plot(m12.star_age, m12.log_Teff,c='red',linewidth=1.3,alpha = 1,label = '$12M_{\odot}$')
plt.plot(m15.star_age, m15.log_Teff,c='orange',linewidth=1.3,alpha = 1,label = '$15M_{\odot}$')
plt.plot(m20_1.star_age, m20_1.log_Teff,c='yellow',linewidth=1.3,alpha = 1,label = '$20M_{\odot}$')
plt.plot(m20_2.star_age, m20_2.log_Teff,c='yellow',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m25_1.star_age, m25_1.log_Teff,c='lime',linewidth=1.3,alpha = 1,label = '$25M_{\odot}$')
plt.plot(m25_2.star_age, m25_2.log_Teff,c='lime',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m32_1.star_age, m32_1.log_Teff,c='green',linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(m40_1.star_age, m40_1.log_Teff,c='blue',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')

plt.plot([-1e3,1e9],[3.7,3.7],c = 'purple',linewidth=0.8)

plt.xlabel('$Time (yr)$')
plt.ylabel('$Log(T_{eff}/K)$')

plt.xlim(0,2e7)
plt.ylim(4.7,3.5)
plt.legend()
plt.savefig('Images/LogTeffxTime.png')
plt.show()
plt.clf()

#---------------------------------------------------------------------------------------
## Equator_average_velocity x Age
plt.title('Equatorial Velocity Evolution')

plt.plot(gen9Age,gen9VEq,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen12Age,gen12VEq,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen15Age,gen15VEq,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen20Age,gen20VEq,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen25Age,gen25VEq,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen32Age,gen32VEq,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen40Age,gen40VEq,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')

plt.plot(m9.star_age, m9.surf_avg_v_rot,c='purple',linewidth=1.3,alpha = 1,label = '$9M_{\odot}$')
plt.plot(m12.star_age, m12.surf_avg_v_rot,c='red',linewidth=1.3,alpha = 1,label = '$12M_{\odot}$')
plt.plot(m15.star_age, m15.surf_avg_v_rot,c='orange',linewidth=1.3,alpha = 1,label = '$15M_{\odot}$')
plt.plot(m20_1.star_age, m20_1.surf_avg_v_rot,c='yellow',linewidth=1.3,alpha = 1,label = '$20M_{\odot}$')
plt.plot(m20_2.star_age, m20_2.surf_avg_v_rot,c='yellow',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m25_1.star_age, m25_1.surf_avg_v_rot,c='lime',linewidth=1.3,alpha = 1,label = '$25M_{\odot}$')
plt.plot(m25_2.star_age, m25_2.surf_avg_v_rot,c='lime',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m32_1.star_age, m32_1.surf_avg_v_rot,c='green',linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(m40_1.star_age, m40_1.surf_avg_v_rot,c='blue',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')

plt.xlabel('$Time (yr)$')
plt.ylabel('$v_{eq} (km/s)$')

# plt.xlim(4.7,3.5)
plt.legend()
plt.savefig('Images/VEqxTime.png')
plt.show()
plt.clf()

#---------------------------------------------------------------------------------------
## Center Tempeaarure x Age
plt.title('Central Temperature Evolution')
# listGenAge = [gen9Age,gen12Age,gen15Age,gen20Age,gen25Age,gen32Age]
# listGenLogTc = [gen9LogTc,gen12LogTc,gen15LogTc,gen20LogTc,gen25LogTc,gen32LogTc]
# listMesaAge = [m9.star_age,m12.star_age,m15.star_age,m20_2.star_age,m25_2.star_age,m32_1.star_age]
# listMesaLogTc = [m9.log_center_T,m12.log_center_T,m15.log_center_T,m20_2.log_center_T,m25_2.log_center_T,m32_1.log_center_T]
# for i in range(len(listGenAge)):
#     plt.plot(listGenAge[i],listGenLogTc[i])
#     plt.plot(listMesaAge[i],listMesaLogTc[i])
#     plt.xlabel('$Time (yr)$')
#     plt.ylabel('$Log(T_{c}/K)$')
#     plt.show()
#     plt.clf()

plt.plot(gen9Age,gen9LogTc,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen12Age,gen12LogTc,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen15Age,gen15LogTc,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen20Age,gen20LogTc,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen25Age,gen25LogTc,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen32Age,gen32LogTc,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen40Age,gen40LogTc,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')

plt.plot(m9.star_age, m9.log_center_T,c='purple',linewidth=1.3,alpha = 1,label = '$9M_{\odot}$')
plt.plot(m12.star_age, m12.log_center_T,c='red',linewidth=1.3,alpha = 1,label = '$12M_{\odot}$')
plt.plot(m15.star_age, m15.log_center_T,c='orange',linewidth=1.3,alpha = 1,label = '$15M_{\odot}$')
plt.plot(m20_1.star_age, m20_1.log_center_T,c='yellow',linewidth=1.3,alpha = 1,label = '$20M_{\odot}$')
plt.plot(m20_2.star_age, m20_2.log_center_T,c='yellow',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m25_1.star_age, m25_1.log_center_T,c='lime',linewidth=1.3,alpha = 1,label = '$25M_{\odot}$')
plt.plot(m25_2.star_age, m25_2.log_center_T,c='lime',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m32_1.star_age, m32_1.log_center_T,c='green',linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(m40_1.star_age, m40_1.log_center_T,c='blue',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')

plt.xlabel('$Time (yr)$')
plt.ylabel('$Log(T_{c}/K)$')

# plt.xlim(4.7,3.5)
plt.legend()
plt.savefig('Images/LogTcxTime.png')
plt.show()
plt.clf()

#---------------------------------------------------------------------------------------
## Center Tempeaarure x Age
plt.title('Teff x Tc')

plt.plot(gen9LogTc,gen9LogTeff,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen12LogTc,gen12LogTeff,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen15LogTc,gen15LogTeff,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen20LogTc,gen20LogTeff,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen25LogTc,gen25LogTeff,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen32LogTc,gen32LogTeff,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen40Age,gen40LogTc,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')

plt.plot(m9.log_center_T, m9.log_Teff,c='purple',linewidth=1.3,alpha = 1,label = '$9M_{\odot}$')
plt.plot(m12.log_center_T, m12.log_Teff,c='red',linewidth=1.3,alpha = 1,label = '$12M_{\odot}$')
plt.plot(m15.log_center_T, m15.log_Teff,c='orange',linewidth=1.3,alpha = 1,label = '$15M_{\odot}$')
plt.plot(m20_1.log_center_T, m20_1.log_Teff,c='yellow',linewidth=1.3,alpha = 1,label = '$20M_{\odot}$')
plt.plot(m20_2.log_center_T, m20_2.log_Teff,c='yellow',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m25_1.log_center_T, m25_1.log_Teff,c='lime',linewidth=1.3,alpha = 1,label = '$25M_{\odot}$')
plt.plot(m25_2.log_center_T, m25_2.log_Teff,c='lime',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m32_1.log_center_T, m32_1.log_Teff,c='green',linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(m40_1.star_age, m40_1.log_center_T,c='blue',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')

plt.xlabel('$Time (yr)$')
plt.ylabel('$Log(T_{c}/K)$')

# plt.xlim(4.7,3.5)
plt.legend()
plt.savefig('Images/LogTcxTime.png')
plt.show()
plt.clf()

#---------------------------------------------------------------------------------------
## Equator_average_velocity x LogTeff
plt.title('Equatorial Velocity Evolution')

plt.plot(gen9LogTeff,gen9VEq,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen12LogTeff,gen12VEq,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen15LogTeff,gen15VEq,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen20LogTeff,gen20VEq,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen25LogTeff,gen25VEq,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')
plt.plot(gen32LogTeff,gen32VEq,color = "#aaaaaa", linewidth=1, alpha = 1,label = '_nolegend_')
# plt.plot(gen40Age,gen40VEq,color = "grey", linewidth=1, alpha = 1,label = '_nolegend_')

plt.plot(m9.log_Teff, m9.surf_avg_v_rot,c='purple',linewidth=1.3,alpha = 1,label = '$9M_{\odot}$')
plt.plot(m12.log_Teff, m12.surf_avg_v_rot,c='red',linewidth=1.3,alpha = 1,label = '$12M_{\odot}$')
plt.plot(m15.log_Teff, m15.surf_avg_v_rot,c='orange',linewidth=1.3,alpha = 1,label = '$15M_{\odot}$')
plt.plot(m20_1.log_Teff, m20_1.surf_avg_v_rot,c='yellow',linewidth=1.3,alpha = 1,label = '$20M_{\odot}$')
plt.plot(m20_2.log_Teff, m20_2.surf_avg_v_rot,c='yellow',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m25_1.log_Teff, m25_1.surf_avg_v_rot,c='lime',linewidth=1.3,alpha = 1,label = '$25M_{\odot}$')
plt.plot(m25_2.log_Teff, m25_2.surf_avg_v_rot,c='lime',linewidth=1.3,alpha = 1,label = '_nolegend_')
plt.plot(m32_1.log_Teff, m32_1.surf_avg_v_rot,c='green',linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(m40_1.star_age, m40_1.surf_avg_v_rot,c='blue',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')

plt.xlabel('$Log(T_{eff}/K)$')
plt.ylabel('$v_{eq} (km/s)$')

plt.xlim(3.8,3.5)
plt.ylim(0,50)
plt.legend()
plt.savefig('Images/VEqxLogTeff.png')
plt.show()
plt.clf()

t4LData.to_csv("External_Data/t4LData2",sep=',')
