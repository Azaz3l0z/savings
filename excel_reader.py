import os
import xlrd
import pandas as pd

src_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'export2022822.xls')

if '.xls' == os.path.splitext(os.path.basename(src_file))[1]:
    wb = xlrd.open_workbook(src_file, logfile=open(os.devnull, 'w'))
    df = pd.read_excel(wb, engine='xlrd', header=7, usecols='A:E')

else:
    df = pd.read_excel(src_file, header=7, usecols='A:E')
    
print(df)    