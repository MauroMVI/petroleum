# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 20:18:43 2020

@author: baske
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import csv
#import numpy as np

filename = "POZOS_COMPILADO.csv"

dtypes = {}

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

header_upper = []
for header in header_row:
    header_upper.append(header.upper())
    
for header in header_upper[:4]:
    dtypes[header] = 'str'

for header in header_upper[4:]:
    dtypes[header] = 'float64'

df = pd.read_csv(filename, sep=',', header=0, names=header_upper, dtype=dtypes)
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d-%m-%Y')
df_nacional = df.groupby(['FECHA']).sum()
pozos = df['NOMBRE_DEL_POZO'].unique()
pozos.sort()
number_of_wells = len(pozos)
count = 0
for pozo in pozos:
    df_test = df.loc[df['NOMBRE_DEL_POZO'] == pozo].set_index('FECHA')
    cuenca = df_test['CUENCA'].iloc[0]
    del df_test['CUENCA']
    del df_test['ASIGNACION_O_CONTRATO']
    fig, ax1 = plt.subplots(figsize=(11,4))
    ax2 = ax1.twinx()
    ax1.plot(
        df_test['PETROLEO_(MBD)'], color='black', label='$Q_O$', linewidth=2
        )
    ax1.plot(
        df_test['AGUA_(MBD)'], color='blue', label='$Q_W$', linewidth=2
        )
    ax1.plot(
        df_test['CONDENSADO_(MBD)'], color='purple', label='$Q_C$', linewidth=2
        )
    ax2.plot(
        df_test['GAS_ASOCIADO_(MMPCD)'], color='red', label='$Q_G$', linewidth=2
        )
    ax2.plot(
        df_test['GAS_NO_ASOCIADO_(MMPCD)'], color='orange', label='$Q_{NG}$', linewidth=2
        )
    ax1.set_xlabel(f'A{chr(241)}os')
    ax1.set_ylabel('$Q_O$, $Q_C$ & $Q_W$ [MBD]')
    ax2.set_ylabel('$Q_G$ & $Q_{NG}$[MMPCD]')
    ax1.grid(b=False)
    ax2.grid(b=False)
    ax1.xaxis.grid(True, which='major')
    ax2.legend([ax1.get_lines()[0], ax1.get_lines()[1], ax1.get_lines()[2], ax2.get_lines()[0], ax2.get_lines()[1]],\
                ['$Q_O$','$Q_W$','$Q_C$','$Q_G$','$Q_{NG}$'], loc='best')
    # ax2.set_ylim(0, df_test['GAS_ASOCIADO_(MMPCD)'].max()*1.05)
    # ax1.set_ylim(0, upper_limit*1.05)
    ax1.set_title(f'Historico de {pozo}')
    newpath = f'POZOS/{cuenca}/{pozo}'
    os.makedirs(newpath)
    fnamefig = f'POZOS/{cuenca}/{pozo}/{pozo}.png'
    fnamexl = f'POZOS/{cuenca}/{pozo}/{pozo}.xlsx'
    plt.savefig(fnamefig, dpi=None, orientation='portrait')
    df_test.to_excel(fnamexl)
    plt.close(fig)
    count += 1
    print(f"{pozo} Done. Well {count} of {number_of_wells}!")

print("All done.")

# fig, ax1 = plt.subplots(figsize=(11,4))
# ax2 = ax1.twinx()
# ax1.plot(
#     df_nacional['PETROLEO_(MBD)'], color='black', label='$Q_O$', linewidth=2
#     )
# ax1.plot(
#     df_nacional['AGUA_(MBD)'], color='blue', label='$Q_W$', linewidth=2
#     )
# ax2.plot(
#     df_nacional['GAS_ASOCIADO_(MMPCD)'], color='red', label='$Q_G$', linewidth=2
#     )
# ax1.set_xlabel(f'A{chr(241)}os')
# ax1.set_ylabel('$Q_O$ & $Q_W$ [MBD]')
# ax2.set_ylabel('$Q_G$ [MMPCD]')
# ax1.grid(b=False)
# ax2.grid(b=False)
# ax1.xaxis.grid(True, which='major')
# ax2.legend([ax1.get_lines()[0], ax1.get_lines()[1], ax2.get_lines()[0]],\
#            ['$Q_O$','$Q_W$','$Q_G$'], loc='upper left')
# ax2.set_ylim(0, df_nacional['GAS_ASOCIADO_(MMPCD)'].max()*1.05)
# ax1.set_ylim(0, df_nacional['PETROLEO_(MBD)'].max()*1.05)
# ax1.set_title('Historico de Produccion Nacional')
# plt.show()
