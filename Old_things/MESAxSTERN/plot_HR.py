import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
import math as mth
import matplotlib.pyplot as plt
from matplotlib import rc

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

#-------|ABRINDO O MESA|---------
m20 = mr.MesaData("20M0/LOGS/history.data")
m30 = mr.MesaData("30M0/LOGS/history.data")
m40 = mr.MesaData("40M0/LOGS/history.data")
m50 = mr.MesaData("50M0/LOGS/history.data")
m60 = mr.MesaData("60M0/LOGS/history.data")

# In[]
#--------|ABRINDO O STERN|--------
with open('f20.mw.track.dat') as ste20File:
	ste20Data = ste20File.read()

ste20Data = ste20Data.split('\n')
ste20Data.pop()
ste20Data.pop(0)

with open('f30.mw.track.dat') as ste30File:
	ste30Data = ste30File.read()

ste30Data = ste30Data.split('\n')
ste30Data.pop()
ste30Data.pop(0)

with open('f40.mw.track.dat') as ste40File:
	ste40Data = ste40File.read()

ste40Data = ste40Data.split('\n')
ste40Data.pop()
ste40Data.pop(0)

with open('f50.mw.track.dat') as ste50File:
	ste50Data = ste50File.read()

ste50Data = ste50Data.split('\n')
ste50Data.pop()
ste50Data.pop(0)

with open('f60.mw.track.dat') as ste60File:
	ste60Data = ste60File.read()

ste60Data = ste60Data.split('\n')
ste60Data.pop()
ste60Data.pop(0)



# In[]

#-------|OBTENDO OS DADOS DO steEC|---------
#Log L e Log Teff
ste20LogL = [float(row.split()[3]) for row in ste20Data]
ste20LogTeff = [mth.log10(float(row.split()[2])) for row in ste20Data]

ste30LogL = [float(row.split()[3]) for row in ste30Data]
ste30LogTeff = [mth.log10(float(row.split()[2])) for row in ste30Data]

ste40LogL = [float(row.split()[3]) for row in ste40Data]
ste40LogTeff = [mth.log10(float(row.split()[2])) for row in ste40Data]

ste50LogL = [float(row.split()[3]) for row in ste50Data]
ste50LogTeff = [mth.log10(float(row.split()[2])) for row in ste50Data]

ste60LogL = [float(row.split()[3]) for row in ste60Data]
ste60LogTeff = [mth.log10(float(row.split()[2])) for row in ste60Data]



#idade e t_H (xH = 0)

ste20Age = [float(row.split()[0]) for row in ste20Data]
ste20CenH = [float(row.split()[54]) for row in ste20Data]

ste30Age = [float(row.split()[0]) for row in ste30Data]
ste30CenH = [float(row.split()[54]) for row in ste30Data]

ste40Age = [float(row.split()[0]) for row in ste40Data]
ste40CenH = [float(row.split()[54]) for row in ste40Data]

ste50Age = [float(row.split()[0]) for row in ste50Data]
ste50CenH = [float(row.split()[54]) for row in ste50Data]

ste60Age = [float(row.split()[0]) for row in ste60Data]
ste60CenH = [float(row.split()[54]) for row in ste60Data]

#Logg e T_cen
ste20Tcen = [float(row.split()[20]) for row in ste20Data]

ste30Tcen = [float(row.split()[20]) for row in ste30Data]

ste40Tcen = [float(row.split()[20]) for row in ste40Data]

ste50Tcen = [float(row.split()[20]) for row in ste50Data]

ste60Tcen = [float(row.split()[20]) for row in ste60Data]

#
# In[]

#~ #---------------|T_H x MASSA|-----------------------------
#~
listMass = [20,30,40,50,60]
# listColor = ['b','c','g','y','r']
listColor = ["lime","C9","purple","brown","black"]

listLabel = ['$20M_{\odot}$','$30M_{\odot}$','$40M_{\odot}$','$50M_{\odot}$','$60M_{\odot}$']

# print(max(ste20CenH))

listTH_ste = []
listSTE = [ste20CenH,ste30CenH,ste40CenH,ste50CenH,ste60CenH]
for i in range(len(listMass)):
	listTH_ste.append(min(listSTE[i]))

print(listTH_ste)
tH20M0_index_Ste = ste20CenH.index(listTH_ste[0])
tH20M0_index_MESA = m20.center_h1.tolist().index(0.0)
print(tH20M0_index_Ste)

tH30M0_index_Ste = ste30CenH.index(listTH_ste[1])
tH30M0_index_MESA = m30.center_h1.tolist().index(0.0)

tH40M0_index_Ste = ste40CenH.index(listTH_ste[2])
tH40M0_index_MESA = m40.center_h1.tolist().index(0.0)

tH50M0_index_Ste = ste50CenH.index(listTH_ste[3])
tH50M0_index_MESA = m50.center_h1.tolist().index(0.0)

tH60M0_index_Ste = ste60CenH.index(listTH_ste[4])
tH60M0_index_MESA = m60.center_h1.tolist().index(0.0)

listTH_ste = [ste20Age[tH20M0_index_Ste],ste30Age[tH30M0_index_Ste],ste40Age[tH40M0_index_Ste],ste50Age[tH50M0_index_Ste],ste60Age[tH60M0_index_Ste]]
print(listTH_ste)

listTH_MESA = [m20.star_age[tH20M0_index_MESA],m30.star_age[tH30M0_index_MESA],m40.star_age[tH40M0_index_MESA],m50.star_age[tH50M0_index_MESA],m60.star_age[tH60M0_index_MESA]]
print(listTH_MESA)

# plt.subplot(2,2,2)
# plt.title(r"Diferença do Tempo de queima do Hidrogênio Central")
# for i in range(len(listMass)):
# 	plt.scatter(listMass[i],(listTH_MESA[i]-listTH_ste[i])*100/listTH_ste[i],color = listColor[i],label = listLabel[i],s= 100)
#
# # plt.xticks([3e6,4e6,5e6,6e6,7e6,8e6],['$3$','$4$','$5$','$6$','$7$','$8$'])
# # plt.yticks([3e6,4e6,5e6,6e6,7e6,8e6],['$3$','$4$','$5$','$6$','$7$','$8$'])
#
# # plt.ylim([-10,10])
# plt.ylabel('$(t_{H}^{MESA}-t_{H}^{STERN})/ t_{H}^{STERN} \, (\%)$')
# plt.xlabel('$M/M_{\odot}$')
# # plt.plot([3000000,8000000],[3000000,8000000],color = '#111111')
# plt.plot([100,0],[0,0],color = '#111111')
# plt.grid(color='grey', linestyle='--', linewidth=.5)
# plt.ylim([-20,20])
# plt.xlim([15,65])
# plt.xticks(listMass)
# # plt.ylim([3000000,8000000])
# # plt.legend(loc = 'lower right', fontsize = 10,scatterpoints = 1)
#
# # plt.savefig('tHxtH.svg')
# plt.savefig('tHxtH.png')
# plt.show()
# plt.clf()

#*******************
# plt.subplot(2,2,2)
# plt.title(r"Diferença do Tempo de queima do Hidrogênio Central")
plt.title('Diferença do Tempo de Esgotamento do $H$ Central',fontsize = 20)
l = [20,30,40,50,60]
for i in range(len(l)):
	plt.scatter(l[i],(listTH_MESA[i]-listTH_ste[i])*100/listTH_ste[i],color = listColor[i],label = listLabel[i],s= 300)

# plt.xticks([3e6,4e6,5e6,6e6,7e6,8e6],['$3$','$4$','$5$','$6$','$7$','$8$'])
# plt.yticks([3e6,4e6,5e6,6e6,7e6,8e6],['$3$','$4$','$5$','$6$','$7$','$8$'])

# plt.ylim([-10,10])
plt.ylabel('$\Delta t_{H} \, / \, t_{H}^{STERN} \, (\%)$')
plt.xlabel('$M/M_{\odot}$')
# plt.plot([3000000,8000000],[3000000,8000000],color = '#111111')
plt.plot([65,15],[0,0],color = '#111111')
plt.grid(color='grey', linestyle='--', linewidth=.5)
# plt.xlim([3000000,8000000])
plt.xlim([15,65])
plt.ylim([-10,10])
plt.yticks([-20,-10,0,10,20])
plt.xticks(l,['20','30','40','50','60'])
# plt.ylim([3000000,8000000])
# plt.legend(loc = 'lower right', fontsize = 10,scatterpoints = 1)

# plt.savefig('tHxtH.svg')
plt.savefig('tHxtH_ste.png')

#*********************

#print m20.star_age, m20.center_h1

#~ tH20M0_index_ste = ste20CenH.index(0.0)
#~ tH20M0_index_MESA = m20.center_h1.tolist().index(0.0)
#~
#~ tH30M0_index_ste = ste30CenH.index(0.0)
#~ tH30M0_index_MESA = m30.center_h1.tolist().index(0.0)
#~
#~ tH40M0_index_ste = ste40CenH.index(0.0)
#~ tH40M0_index_MESA = m40.center_h1.tolist().index(0.0)
#~
#~ tH50M0_index_ste = ste50CenH.index(0.0)
#~ tH50M0_index_MESA = m50.center_h1.tolist().index(0.0)
#~
#~ tH60M0_index_ste = ste60CenH.index(0.0)
#~ tH60M0_index_MESA = m60.center_h1.tolist().index(0.0)
#~
#~ #
#~
#~ listTH_ste = [ste20Age[tH20M0_index_ste],ste32Age[tH32M0_index_ste],ste40Age[tH40M0_index_ste],ste50Age[tH50M0_index_ste],ste60Age[tH60M0_index_ste]]
#~ listTH_MESA = [m20.star_age[tH20M0_index_MESA],m32.star_age[tH32M0_index_MESA],m40.star_age[tH40M0_index_MESA],m50.star_age[tH50M0_index_MESA],m60.star_age[tH60M0_index_MESA]]
#~
#~ listDifPC = [100*(listTH_ste[i]-listTH_MESA[i])/listTH_ste[i] for i in range(5)]

#--------|PLOTANDO|----------------
# plt.grid(color='grey', linestyle='--', linewidth=.5)
#
# plt.title('HR Diagram',fontsize = 20)
# plt.grid(color='grey', linestyle='--', linewidth=.5)
#
# plt.plot(m20.log_Teff[23:],m20.log_L[23:],'b-',linewidth=1.3,alpha = 1, label = '$25M_{\odot}$')
# plt.plot(ste20LogTeff[:],ste20LogL[:],color = "#000875", linewidth=0.8, alpha = 1)
#
# plt.plot(m30.log_Teff[23:],m30.log_L[23:],color = "#009CB2",linewidth=1.3,alpha = 1,label = '$32M_{\odot}$')
# plt.plot(ste30LogTeff[:],ste30LogL[:],color = '#004752', linewidth=0.8, alpha = 1)
#
# plt.plot(m40.log_Teff[23:],m40.log_L[23:],'g-',linewidth=1.3,alpha = 1,label = '$40M_{\odot}$')
# plt.plot(ste40LogTeff[:],ste40LogL[:],c = '#004007', linewidth=0.8, alpha = 1)
#
# plt.plot(m50.log_Teff[23:],m50.log_L[23:],'y-',linewidth=1.3,alpha = 1,label = '$50M_{\odot}$')
# plt.plot(ste50LogTeff[:],ste50LogL[:],c='#4C4600', linewidth=0.8, alpha = 1)
#
# plt.plot(m60.log_Teff[23:],m60.log_L[23:],'r-',linewidth=1.3,alpha = 1,label = '$60M_{\odot}$')
# plt.plot(ste60LogTeff[:],ste60LogL[:],c='#690C00', linewidth=0.8, alpha = 1)
#
# plt.ylabel("$Log(L/L_{\odot})$")
# plt.xlabel("$Log(T_{eff}/K)$")
# plt.xlim([4.7,4.3])
# plt.yticks(np.arange(4.7,6,0.3))
# plt.xticks(np.arange(4.3,4.7,0.1))
# plt.legend(loc = 'lower right', fontsize = 10)
# plt.savefig('HR.svg')
# plt.savefig('HR.svg')
# plt.show()
# plt.clf()
#
# plt.savefig('MESAxSTERN.png')
# plt.show()
