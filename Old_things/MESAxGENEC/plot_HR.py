# Using the magic encoding
# -*- coding: utf-8 -*-
import mesa_reader as mr
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math as mth
import matplotlib.ticker as tkr

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


#-------|CONSTANTES FISICAS/ASTRONOMICAS|-----------
G = 6.674e-8 #cm(3).g(-1).s(-2)
sb = 5.67e-5 #erg.cm(-2).K(-4)
L0 = 3.9e33 #erg.s(-1)
R0 = 6.96e10 #cm
M0 = 1.99e33 #g

#-------|ABRINDO O MESA|---------
m25 = mr.MesaData("25M0/LOGS/history.data")
m32 = mr.MesaData("32M0/LOGS/history.data")
m40 = mr.MesaData("40M0/LOGS/history.data")
m50 = mr.MesaData("50M0/LOGS/history.data")
m60 = mr.MesaData("60M0/LOGS/history.data")


#--------|ABRINDO O GENEC|--------
with open('M025Z14V0.dat') as gen25File:
	gen25Data = gen25File.read()

gen25Data = gen25Data.split('\n')
gen25Data.pop()

with open('M032Z14V0.dat') as gen32File:
	gen32Data = gen32File.read()

gen32Data = gen32Data.split('\n')
gen32Data.pop()

with open('M040Z14V0.dat') as gen40File:
	gen40Data = gen40File.read()

gen40Data = gen40Data.split('\n')
gen40Data.pop()

with open('M050Z14V0.dat') as gen50File:
	gen50Data = gen50File.read()

gen50Data = gen50Data.split('\n')
gen50Data.pop()

with open('M060Z14V0.dat') as gen60File:
	gen60Data = gen60File.read()

gen60Data = gen60Data.split('\n')
gen60Data.pop()


#-------|OBTENDO OS DADOS DO GENEC|---------
#Massa
gen25Mass = [float(row.split()[2]) for row in gen25Data]

gen32Mass = [float(row.split()[2]) for row in gen32Data]

gen40Mass = [float(row.split()[2]) for row in gen40Data]

gen50Mass = [float(row.split()[2]) for row in gen50Data]

gen60Mass = [float(row.split()[2]) for row in gen60Data]


#Log L e Log Teff
gen25LogL = [float(row.split()[3]) for row in gen25Data]
gen25LogTeff = [float(row.split()[4]) for row in gen25Data]

gen32LogL = [float(row.split()[3]) for row in gen32Data]
gen32LogTeff = [float(row.split()[4]) for row in gen32Data]

gen40LogL = [float(row.split()[3]) for row in gen40Data]
gen40LogTeff = [float(row.split()[4]) for row in gen40Data]

gen50LogL = [float(row.split()[3]) for row in gen50Data]
gen50LogTeff = [float(row.split()[4]) for row in gen50Data]

gen60LogL = [float(row.split()[3]) for row in gen60Data]
gen60LogTeff = [float(row.split()[4]) for row in gen60Data]

#idade e t_H (xH = 0)

gen25Age = [float(row.split()[1]) for row in gen25Data]
gen25CenH = [float(row.split()[21]) for row in gen25Data]

gen32Age = [float(row.split()[1]) for row in gen32Data]
gen32CenH = [float(row.split()[21]) for row in gen32Data]

gen40Age = [float(row.split()[1]) for row in gen40Data]
gen40CenH = [float(row.split()[21]) for row in gen40Data]

gen50Age = [float(row.split()[1]) for row in gen50Data]
gen50CenH = [float(row.split()[21]) for row in gen50Data]

gen60Age = [float(row.split()[1]) for row in gen60Data]
gen60CenH = [float(row.split()[21]) for row in gen60Data]

#Logg e T_cen
gen25LogTcen = [float(row.split()[20]) for row in gen25Data]

gen32LogTcen = [float(row.split()[20]) for row in gen32Data]

gen40LogTcen = [float(row.split()[20]) for row in gen40Data]

gen50LogTcen = [float(row.split()[20]) for row in gen50Data]

gen60LogTcen = [float(row.split()[20]) for row in gen60Data]

#
listR25M0 = [(((10**gen25LogL[i])*L0/(4*mth.pi*sb*(10**gen25LogTeff[i])**4))**0.5)/R0 for i in range(len(gen25LogL))]

listR32M0 = [(((10**gen32LogL[i])*L0/(4*mth.pi*sb*(10**gen32LogTeff[i])**4))**0.5)/R0 for i in range(len(gen32LogL))]

listR40M0 = [(((10**gen40LogL[i])*L0/(4*mth.pi*sb*(10**gen40LogTeff[i])**4))**0.5)/R0 for i in range(len(gen40LogL))]

listR50M0 = [(((10**gen50LogL[i])*L0/(4*mth.pi*sb*(10**gen50LogTeff[i])**4))**0.5)/R0 for i in range(len(gen50LogL))]

listR60M0 = [(((10**gen60LogL[i])*L0/(4*mth.pi*sb*(10**gen60LogTeff[i])**4))**0.5)/R0 for i in range(len(gen60LogL))]

gen25Logg = [mth.log10(G*gen25Mass[i]*M0/(listR25M0[i]*R0)**2) for i in range(len(gen25Age))]

gen32Logg = [mth.log10(G*gen32Mass[i]*M0/(listR32M0[i]*R0)**2) for i in range(len(gen32Age))]

gen40Logg = [mth.log10(G*gen40Mass[i]*M0/(listR40M0[i]*R0)**2) for i in range(len(gen40Age))]

gen50Logg = [mth.log10(G*gen50Mass[i]*M0/(listR50M0[i]*R0)**2) for i in range(len(gen50Age))]

gen60Logg = [mth.log10(G*gen60Mass[i]*M0/(listR60M0[i]*R0)**2) for i in range(len(gen60Age))]


#---------------|T_H x MASSA|-----------------------------

listMass = ['25','32','40','50','60']

#print m25.star_age, m25.center_h1

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

#--------|PLOTANDO|----------------
# plt.title("MESA X Genebra(Ekstrom)")
# plt.rc('text', usetex=True)
#plt.rc('font', family='sans-serif')
listColor = ['b','c','g','y','r']
listLabel = ['$25M_{\odot}$','$32M_{\odot}$','$40M_{\odot}$','$50M_{\odot}$','$60M_{\odot}$']
# plt.clf()
plt.figure()
#______________________________
# plt.subplot(1,2,1)
plt.title('HR Diagram',fontsize = 20)
# plt.grid(color='grey', linestyle='--', linewidth=.5)

plt.plot(m25.log_Teff[23:],m25.log_L[23:],'b-',linewidth=1.3,alpha = 1, label = '$25M_{\odot}$')
plt.plot(gen25LogTeff[:-200],gen25LogL[:-200],color = "#000875", linewidth=0.8, alpha = 1)

plt.plot(m32.log_Teff[23:],m32.log_L[23:],color = "#009CB2",linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
plt.plot(gen32LogTeff[:-200],gen32LogL[:-200],color = '#004752', linewidth=0.8, alpha = 1)

plt.plot(m40.log_Teff[23:],m40.log_L[23:],'g-',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')
plt.plot(gen40LogTeff[:-200],gen40LogL[:-200],c = '#004007', linewidth=0.8, alpha = 1)

plt.plot(m50.log_Teff[23:],m50.log_L[23:],'y-',linewidth=1.3,alpha = 1,label = '$50M_{\odot}$')
plt.plot(gen50LogTeff[:-200],gen50LogL[:-200],c='#4C4600', linewidth=0.8, alpha = 1)

plt.plot(m60.log_Teff[23:],m60.log_L[23:],'r-',linewidth=1.3,alpha = 1,label = '$60M_{\odot}$')
plt.plot(gen60LogTeff[:-240],gen60LogL[:-240],c='#690C00', linewidth=0.8, alpha = 1)

plt.ylabel("$Log(L/L_{\odot})$")
plt.xlabel("$Log(T_{eff}/K)$")
plt.xlim([4.7,4.3])
plt.yticks(np.arange(4.7,6,0.3))
plt.xticks(np.arange(4.3,4.7,0.1))
plt.legend(loc = 'lower right', fontsize = 10)
plt.savefig('HR.svg')
plt.savefig('HR.svg')
plt.show()
plt.clf()

#___________________________________________
# In[]
# plt.subplot(2,2,2)
# plt.title(r"Diferença do Tempo de queima do Hidrogênio Central")
colorlist = ["green","blue","purple","brown","black"]

plt.title('Diferença do Tempo de Esgotamento do $H$ Central',fontsize = 20)
l = [25,35,45,55,65]
for i in range(len(l)):
	plt.scatter(l[i],(listTH_MESA[i]-listTH_gen[i])*100/listTH_gen[i],color = colorlist[i],label = listLabel[i],s= 300)

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
# plt.ylim([3000000,8000000])
# plt.legend(loc = 'lower right', fontsize = 10,scatterpoints = 1)

# plt.savefig('tHxtH.svg')
plt.savefig('tHxtH.png')


#___________________________________________
# plt.subplot(2,2,2)
# plt.title(r"Diferença do Tempo de queima do Hidrogênio Central")

# plt.bar(listMass,listMass(np.array(listTH_MESA)-np.array(listTH_gen))/np.array(listTH_gen))

# plt.xticks([3e6,4e6,5e6,6e6,7e6,8e6],['$3$','$4$','$5$','$6$','$7$','$8$'])
# plt.yticks([3e6,4e6,5e6,6e6,7e6,8e6],['$3$','$4$','$5$','$6$','$7$','$8$'])
#
# plt.ylim([-10,10])
# plt.ylabel('$t_{H}^{GENEC} \, [Myr]$')
# plt.xlabel('$t_{H}^{MESA} \, [Myr]$')
# # plt.plot([3000000,8000000],[3000000,8000000],color = '#111111')
# plt.grid(color='grey', linestyle='--', linewidth=.5)
# plt.xlim([3000000,8000000])
# plt.ylim([3000000,8000000])
# plt.legend(loc = 'lower right', fontsize = 10,scatterpoints = 1)

# plt.savefig('tHxtH.svg')
# plt.savefig('tHxtH_hist.svg')
# plt.show()
# plt.clf()

#______________________________________________
# plt.subplot(2,2,4)
# In[]
plt.title("Log(g) x Log(Teff)")
plt.plot(m25.log_Teff[23:],m25.log_g[23:],'b-',linewidth=1.3,alpha = 1, label = '$25M_{\odot}$')
plt.plot(gen25LogTeff[:-200],gen25Logg[:-200],color = "#000875", linewidth=0.8, alpha = 1)

plt.plot(m32.log_Teff[23:],m32.log_g[23:],color = "#009CB2",linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
plt.plot(gen32LogTeff[:-200],gen32Logg[:-200],color = '#004752', linewidth=0.8, alpha = 1)

plt.plot(m40.log_Teff[23:],m40.log_g[23:],'g-',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')
plt.plot(gen40LogTeff[:-200],gen40Logg[:-200],c = '#004007', linewidth=0.8, alpha = 1)

plt.plot(m50.log_Teff[23:],m50.log_g[23:],'y-',linewidth=1.3,alpha = 1,label = '$50M_{\odot}$')
plt.plot(gen50LogTeff[:-200],gen50Logg[:-200],c='#4C4600', linewidth=0.8, alpha = 1)

plt.plot(m60.log_Teff[23:],m60.log_g[23:],'r-',linewidth=1.3,alpha = 1,label = '$60M_{\odot}$')
plt.plot(gen60LogTeff[:-240],gen60Logg[:-240],c='#690C00', linewidth=0.8, alpha = 1)

plt.ylim([2.5,4.5])
plt.xlim([4.7,4.4])

plt.ylabel("$Log(g/cm \cdot s^{-2} )$")
plt.xlabel("$Log(T_{eff}/K)$")

plt.grid(color='grey', linestyle='--', linewidth=.5)
plt.legend(loc = 'lower left', fontsize = 10)
plt.savefig('loggLogTeff.svg')
plt.savefig('loggLogTeff.svg')
plt.show()
# plt.clf()
