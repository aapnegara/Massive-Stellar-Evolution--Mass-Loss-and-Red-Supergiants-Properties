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
rot_list = ["0","3"]
models_list = [mr.MesaData("LOGS_0%s/history.data" % rot) for rot in rot_list]
colorlist = ["purple","blue","cyan"]

# In[]

[plt.plot(models_list[i].log_Teff,models_list[i].log_L, label = '$\Omega / \Omega_{crit} = 0.%s$' % rot_list[i], color = colorlist[i]) for i in range(len(models_list))]

plt.legend(bbox_to_anchor=(1,1))
plt.title("Diagrama HR  [L .vs. $T_{eff}]$")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.ylabel("$log_{10}(L/L_{\odot})$")

plt.xticks([4.6,4.4,4.2,4.0,3.8,3.7,3.6])
plt.gca().invert_xaxis()
# plt.savefig("Images/HR_%s.png" % today_str,bbox_inches='tight')

# In[]

[plt.plot(models_list[i].star_age,models_list[i].surface_h1, label = '$%sM_{\odot}$' % rot_list[i], color = colorlist[i]) for i in range(len(models_list))]

plt.legend(bbox_to_anchor=(1,1))
plt.title("Diagrama HR  [L .vs. $T_{eff}]$")
plt.xlabel("$log_{10}(T_{eff}/K)$")
plt.ylabel("$log_{10}(L/L_{\odot})$")

plt.xticks([4.6,4.4,4.2,4.0,3.8,3.7,3.6])
# plt.savefig("Images/HR_%s.png" % today_str,bbox_inches='tight')

# In[]
models_dirs = [mr.MesaLogDir("LOGS_0%s" % rot) for rot in rot_list]
# p = models_dirs[0].profile_data(profile_number=1)
for mod_index in range(len(rot_list)):
    for prof_index in range(1,15):
        plt.plot(models_dirs[mod_index].profile_data(profile_number=prof_index).mass,(models_dirs[mod_index].profile_data(profile_number=prof_index).x_mass_fraction_H))
        plt.plot(models_dirs[mod_index].profile_data(profile_number=prof_index).mass,(models_dirs[mod_index].profile_data(profile_number=prof_index).y_mass_fraction_He))
        plt.plot(models_dirs[mod_index].profile_data(profile_number=prof_index).mass,(models_dirs[mod_index].profile_data(profile_number=prof_index).z_mass_fraction_metals))

        plt.xlim(-0.05,20.05)
        plt.ylim(-0.01,1.01)
        plt.savefig('movie/test_%s_%i' % (rot_list[mod_index],prof_index))
        plt.clf()

# In[]
import cv2
import os
l = [i for i in range(0,2655,15)]

def save():
    os.system("ffmpeg -r 1 -i grid4_%04d.png -vcodec mpeg4 -y movie.mp4")

image_folder = 'png'
video_name = 'video.mp4'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

print(os.path.join(image_folder, images[0]))

video = cv2.VideoWriter(video_name, 0, 1, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()

# save()
