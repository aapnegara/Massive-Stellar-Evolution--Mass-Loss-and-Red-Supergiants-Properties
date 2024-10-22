import matplotlib.pyplot as plt
import math as mth

#----------------------------------------------------------------
#abrir e pre-tratar a tabela 4 da Levesque
with open('tabela4_Levesque.csv') as t4LFile:
	t4LData = t4LFile.read()
	t4LFile.close()

t4LData = t4LData.split('\n')
t4LData.pop() #tira a ultia linha inutil
del t4LData[0] #tira a primeira linha com os nomes das colunas

#--------------------------------------------------------------
#extrair logg_modelo, logg_teorico e R/R0
t4LLog_gM = [float(row.split(',')[4]) for row in t4LData]
t4LLog_gA_raw = [(row.split(',')[5]) for row in t4LData]
t4LR_R0_raw = [(row.split(',')[7]) for row in t4LData]

t4LTeff = [float(row.split(',')[2]) for row in t4LData]
t4LLog_Teff = [mth.log10(t4LTeff[i]) for i in range(len(t4LTeff))]


#rotina para remover as linhas que possuirem elementos inexistentes 
l_rm = []
for i in range(len(t4LLog_gA_raw)):
	if t4LLog_gA_raw[i] == '':
		l_rm.append(i)

for i in l_rm[::-1]:
	del t4LLog_gA_raw[i] 
	del t4LLog_Teff[i] 
	del t4LLog_gM[i]
	del t4LR_R0_raw[i] 

'''
IMPORTANTISSIMO!! DELETAR OS ELEMENTOS DA LISTA DE TRAS PRA FRENTE
''' 


#converter as listas _raw em definitivas {str -> float}
t4LLog_gA = [float(i) for i in t4LLog_gA_raw]
t4LR_R0 = [float(i) for i in t4LR_R0_raw]

print t4LR_R0[59],t4LLog_gA[59],t4LLog_gM[59]

#---------------------------------------------------------------
#OBTER A MASSA ESPECTRAL A PARTIR DA FORMULA M = 10^log(g)R^2/G
#lembrar que esta tudo em cgs!
G_ = 6.67259e-8 #cm^3 g^-1 s^-1
gA = [10**value for value in t4LLog_gA]
gM = [10**value for value in t4LLog_gM]

mspecA = [(((t4LR_R0[i]*6.96e10)**2)*(gA[i])/G_)/1.99e33 for i in range(len(t4LR_R0))]
mspecM = [(((t4LR_R0[i]*6.96e10)**2)*(gM[i])/G_)/1.99e33 for i in range(len(t4LR_R0))]


P0 = [-1.5,50.5]
P1 = [-1.5,50.5]


plt.scatter(t4LLog_Teff,mspecM)
#~ plt.plot(P0,P1,'k-')
plt.ylabel("Mspec ")
plt.xlabel("Teff")
plt.show()
