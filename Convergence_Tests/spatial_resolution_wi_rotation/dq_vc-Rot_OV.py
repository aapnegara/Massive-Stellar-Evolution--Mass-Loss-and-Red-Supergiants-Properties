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

mass_vector = (12, 15, 20, 25, 32, 40, 60)
dq_vector = ("0.0005","0.001","0.005")
color_vector_old = ['red','orange','C8','green','blue','purple','black']
color_vector = [ele for ele in color_vector_old for i in range(len(dq_vector))]
ms37_vector = ['v','<','>']
ls_vector = ['-','--',':']
ms_vector = ['o','x','+']
print(color_vector)
# # In[]
# gen12Data = pd.read_csv("../External_Data/M012Z14V4.dat")
# gen12LogTeff = gen12Data['lg(Teff)']
# gen12LogL = gen12Data['lg(L)']
# gen12Mass = gen12Data['mass']
# gen12Age = gen12Data['time']
# gen12VEq = gen12Data['v_equa']
# gen12LogTc = gen12Data['lg(Tc)']
#
# gen15Data = pd.read_csv("../External_Data/M015Z14V4.dat")
# gen15LogTeff = gen15Data['lg(Teff)']
# gen15LogL = gen15Data['lg(L)']
# gen15Mass = gen15Data['mass']
# gen15Age = gen15Data['time']
# gen15VEq = gen15Data['v_equa']
# gen15LogTc = gen15Data['lg(Tc)']
#
# gen32Data = pd.read_csv("../External_Data/M032Z14V4.dat")
# gen32LogTeff = gen32Data['lg(Teff)']
# gen32LogL = gen32Data['lg(L)']
# gen32Mass = gen32Data['mass']
# gen32Age = gen32Data['time']
# gen32VEq = gen32Data['v_equa']
# gen32LogTc = gen32Data['lg(Tc)']


# In[32]:
models_array = [mr.MesaData("LOGS_all_masses/LOGS_%iM0_dq%s_vc1e-4/history.data" % (mass, dq)) for mass in mass_vector for dq in dq_vector]

# In[]
# label_list_l = ["$%i M_{\odot} \, \, | \ dq_{max} = %s$" % (mass,dq) for mass in mass_vector for dq in dq_vector]
label_list_l = ["$%i M_{\odot} \, \, | \ N_{zones} = %s$" % (mass,int(1/float(dq))) for mass in mass_vector for dq in dq_vector]

# In[34]: HRD
[plt.plot(models_array[i].log_Teff,models_array[i].log_L, label = label_list_l[i], color = color_vector[i], linestyle=ls_vector[i%3]) for i in range(len(models_array))]
plt.legend(bbox_to_anchor=(1,1))
plt.title("Diagrama HR  [L .vs. $T_{eff}]$")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.ylabel("$log_{10}(L/L_{\odot})$")
plt.plot([3.7,3.7],[0,6.8],color="fuchsia")
plt.ylim(3.8,6.6)
plt.xticks([4.6,4.4,4.2,4.0,3.8,3.7,3.6])
plt.gca().invert_xaxis()
plt.savefig("HR_rot_test.eps",bbox_inches='tight')

# In[34]: Mass x LogTeff

[plt.plot(models_array[i].log_Teff,models_array[i].star_mass,label = label_list_l[i], color = color_vector[i], linestyle=ls_vector[i%3]) for i in range(len(models_array))]

# [plt.fill_between(models_array[i].log_Teff,models_array[i].star_mass, color = 'grey',alpha=0.2) for i in range(len(models_array))]

# plt.fill_between(models_array[15].log_Teff[0:-29],models_array[15].star_mass[0:-29], color = 'grey',alpha=0.3)
# plt.fill_between(models_array[16].log_Teff[0:-150],models_array[16].star_mass[0:-150], color = 'grey',alpha=0.2)

plt.legend(bbox_to_anchor=(1,1))
plt.title("Diagrama Massa .vs. $T_{eff}$")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.ylabel("$log_{10}(M/M_{\odot})$")
plt.plot([3.7,3.7],[0,65],color="fuchsia")
plt.ylim(9,62)
plt.xticks([4.6,4.4,4.2,4.0,3.8,3.7,3.6])
plt.gca().invert_xaxis()
plt.savefig("MT_rot_test.svg",bbox_inches='tight')

# In[34]: Mass x LogTeff

[plt.plot(models_array[i].star_mass,models_array[i].log_L,label = label_list_l[i]) for i in range(len(models_array))]
plt.legend()
plt.gca().invert_xaxis()
# In[34]: Mass x LogTeff

[plt.plot(models_array[i].log_Teff[1:],models_array[i].log_abs_mdot[1:],label = label_list_l[i]) for i in range(len(models_array))]
plt.legend()
plt.gca().invert_xaxis()

# In[34]: Mass x Mdot

[plt.plot(models_array[i].star_mass[1:],models_array[i].log_abs_mdot[1:],label = label_list_l[i]) for i in range(len(models_array))]
plt.legend()
plt.gca().invert_xaxis()

# In[34]: mass x retries

[plt.plot(models_array[i].star_mass[1:],models_array[i].num_zones[1:],label = label_list_l[i]) for i in range(len(models_array))]
plt.legend()
plt.gca().invert_xaxis()

# In[34]: mass x retries

[plt.plot(models_array[i].star_mass[1:],models_array[i].num_retries[1:],label = label_list_l[i],color=color_vector[i],linestyle=ls_vector[i%3]) for i in range(len(models_array))]
plt.title("Número de Tentativas para Evoluir o Modelo \n para o Próximo Instante")
plt.legend(bbox_to_anchor=(1,1))
plt.xlabel("$M/M_{\odot}$")
plt.ylabel("Tentativas")
plt.gca().invert_xaxis()
plt.savefig("Nt_rot_test.eps",bbox_inches='tight')

# In[34]: mass x retries

[plt.plot(models_array[i].star_mass[1:],models_array[i].surf_avg_v_rot[1:],label = label_list_l[i]) for i in range(len(models_array))]
plt.legend()
plt.gca().invert_xaxis()

# In[34]: Mass x time

[plt.plot(models_array[i].star_age,models_array[i].log_Teff,label = label_list_l[i]) for i in range(len(models_array))]
plt.legend()

# In[]
l_i_lTeff37 = []
l_teff_min = [models_array[i].log_Teff.tolist().index(min(models_array[i].log_Teff)) for i in range(len(models_array))]
l_rsg = []
for i_mod in range(len(models_array)):
    for i_lTeff in range(len(models_array[i_mod].log_Teff)):
        if models_array[i_mod].log_Teff[i_lTeff] < 3.7:
            l_i_lTeff37.append(i_lTeff)
            l_rsg.append(i_mod)
            break

# for i in range(len(models_list[2].log_Teff[l_i_lTeff37:-1])):


print(l_i_lTeff37)
print(l_rsg)
print(l_teff_min)

[plt.plot(10**np.log10(models_array[i].star_age[l_i_lTeff37[l_rsg.index(i)]:-1]),models_array[i].star_mass[l_i_lTeff37[l_rsg.index(i)]:-1],label = label_list_l[i], color = color_vector[i], linestyle=ls_vector[i%3]) for i in l_rsg]

[plt.fill_between(10**np.log10(models_array[i].star_age[l_i_lTeff37[l_rsg.index(i)]:-1]),models_array[i].star_mass[l_i_lTeff37[l_rsg.index(i)]:-1],color=color_vector[i],alpha=0.2) for i in l_rsg]

[plt.scatter(10**np.log10(models_array[i].star_age[l_i_lTeff37[l_rsg.index(i)]]),models_array[i].star_mass[l_i_lTeff37[l_rsg.index(i)]],marker=ms37_vector[i%3],s=80,color = color_vector[i]) for i in l_rsg]
# [plt.scatter(np.log10(models_array[i].star_age[l_teff_min[i]]),models_array[i].star_mass[l_teff_min[i]],marker=ms_vector[i%3],s=80,color = color_vector[i]) for i in range(len(models_array))]

plt.scatter(-100,-100,marker=ms37_vector[0],s=80,color = "grey",label="$log_{10}(T_{eff}/K) = 3.7 \, \, | \,  dq_{max} = 0.0005$")
plt.scatter(-100,-100,marker=ms37_vector[1],s=80,color = "grey",label="$log_{10}(T_{eff}/K) = 3.7 \, \, | \, dq_{max} = 0.001$")
plt.scatter(-100,-100,marker=ms37_vector[2],s=80,color = "grey",label="$log_{10}(T_{eff}/K) = 3.7 \, \, | \, dq_{max} = 0.005$")
# plt.scatter(-100,-100,marker=ms_vector[0],s=80,color = "grey",label="$min[ \, log_{10}(T_{eff}/K) \, ] \, \, | \, dq_{max} = 0.0005$")
# plt.scatter(-100,-100,marker=ms_vector[1],s=80,color = "grey",label="$min[ \, log_{10}(T_{eff}/K) \, ] \, \, | \, dq_{max} = 0.001$")
# plt.scatter(-100,-100,marker=ms_vector[2],s=80,color = "grey",label="$min[ \, log_{10}(T_{eff}/K) \, ] \, \, | \, dq_{max} = 0.005$")

plt.title("Evolução Temporal da Massa após tornar-se RSG")
plt.xlabel("$t [yr]$")
plt.ylabel("$M \, [M_{\odot}]$")
# plt.xlim((6.55,7.32))
plt.xlim((0.4e7,2e7))
plt.ylim((9,30))

plt.legend(bbox_to_anchor=(1,1))
plt.savefig("Mt_rot_test.svg",bbox_inches='tight')
