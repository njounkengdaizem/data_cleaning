# import excel data
# data cleaning
# export
import matplotlib.pyplot
import openpyxl as openpyxl
import pip
import numpy as np
import datetime
import pandas as pd
import matplotlib

excel_workbook = 'fifa21_raw_data.xlsx'
df = pd.read_excel(excel_workbook, sheet_name="fifa21_raw_data")


# print(sheet1.head(10))

# Changing height and weight fields to numerical values
def convert(ht):
    ht_ = ht.split("'")
    ft_ = float(ht[0])
    in_ = int(ht[2])
    return (12 * ft_) + in_


def convertwt(wt):
    wt_ = wt.split("l")
    p1 = int(wt_[0])
    return p1


# Replace New Line Characters
for i in df.columns:
    df[i] = df[i].replace("/n", '')

# print(df.columns.str.contains("/n", case = False))

df["Height"] = (df["Height"].apply(convert))
df["Weight"] = (df["Weight"].apply(convertwt))

# Checking Players that have played for more than 10 years
df["Joined"] = df["Joined"].astype(str)
datem = df["Joined"].str.split("-")
yearvalid = []
for i in range(len(datem)):
    year = datem[i][0]
    if (int(year) <= 2012):
        yearvalid.append("Yes")
    else:
        yearvalid.append("No")
df.insert(18, "10 years or more", yearvalid)

# 'Value',	'Wage'	and	"Release	Clause'	are	string	columns.	Convert	them	to	numbers.	For	eg,	"M"	in
# value	column	is	Million,	so	multiply	the	row	values	by	1,000,000,	etc

df["Value"] = df["Value"].astype(str)
d = df["Value"].str.encode('ascii', 'ignore').str.decode('ascii')
actualval = []

for i in range(len(d)):
    if "K" in d[i]:
        dthousand = float(d[i].replace('K', '')) * 1000
        actualval.append(dthousand)
    elif "M" in d[i]:
        dmillion = float(d[i].replace('M', '')) * 1000000
        actualval.append(dmillion)
    else:
        actualval.append(float(d[i]))

df["Value"] = actualval

df["Wage"] = df["Wage"].astype(str)
wag = df["Wage"].str.encode('ascii', 'ignore').str.decode('ascii')
actualwage = []
for i in range(len(wag)):
    if "K" in wag[i]:
        dthousand = float(wag[i].replace('K', '')) * 1000
        actualwage.append(dthousand)
    elif "M" in wag[i]:
        dmillion = float(wag[i].replace('M', '')) * 1000000
        actualwage.append(dmillion)
    else:
        actualwage.append(float(wag[i]))

df["Wage"] = actualwage

df["Release Clause"] = df["Release Clause"].astype(str)
rc = df["Release Clause"].str.encode('ascii', 'ignore').str.decode('ascii')
rel = []
for i in range(len(rc)):
    if "K" in rc[i]:
        dthousand = float(rc[i].replace('K', '')) * 1000
        rel.append(dthousand)
    elif "M" in rc[i]:
        dmillion = float(rc[i].replace('M', '')) * 1000000
        rel.append(dmillion)
    else:
        rel.append(float(rc[i]))

df["Release Clause"] = rel

df.rename(columns={'â†“OVA': 'OVA'}, inplace=True)

df["W/F"] = df["W/F"].astype(str)
wf = df["W/F"].str.encode('ascii', 'ignore').str.decode('ascii')
wf_list = []
for i in range(len(wf)):
    wf_list.append(float(wf[i]))
df["W/F"] = wf_list

df["SM"] = df["SM"].astype(str)
sm = df["SM"].str.encode('ascii', 'ignore').str.decode('ascii')
sm_list = []
for i in range(len(sm)):
    sm_list.append(float(sm[i]))
df["SM"] = sm_list

df["IR"] = df["IR"].astype(str)
ir = df["IR"].str.encode('ascii', 'ignore').str.decode('ascii')
ir_list = []
for i in range(len(ir)):
    ir_list.append(float(ir[i]))
df["IR"] = ir_list

# Creating Dummies

dum1 = pd.get_dummies(df["foot"], drop_first=False)
df = pd.concat([df.drop(['foot'], axis=1), dum1], axis=1)
# del df["Right"]

dum2 = pd.get_dummies(df["BP"], drop_first=True)
df = pd.concat([df.drop(['BP'], axis=1), dum2], axis=1)


df.plot.scatter(x='Wage', y='Value', c='red')
matplotlib.pyplot.show()

df.to_excel("result_file.xlsx")
