import pandas as pd
train1 = pd.read_csv('./data/1.csv')
n_list = train1["Number"]
country = train1["Country"]
year = train1["Year"]
city = train1["City"]

a = "第"
b = "届冬奥会是"
c = "哪一年"
d = "在哪个国家"
e = "在哪个城市"
f = "举办的"

qlist = []
alist = []

for i in range(0,25,1):
    q1 = a+str(i+1)+b+c+f
    q2 = a+str(i+1)+b+d+f
    q3 = a+str(i+1)+b+e+f
    a1 = year[i]
    a2 = country[i]
    a3 = city[i]
    qlist.append(q1)
    qlist.append(q2)
    qlist.append(q3)
    alist.append(a1)
    alist.append(a2)
    alist.append(a3)
data = {'question':qlist,
        'answer':alist}
df = pd.DataFrame(data,columns=['question','answer'])
writer = pd.ExcelWriter('./data/data3.xlsx')
df.to_excel(writer, columns=['question','answer'], index=False,encoding='utf-8',sheet_name='Sheet1')
writer.save()