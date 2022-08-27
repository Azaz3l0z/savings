import os
import xlrd
import pandas as pd

src_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'export2022822.xls')

df = pd.read_excel(src_file, header=7, usecols='A:E')

print(df)    