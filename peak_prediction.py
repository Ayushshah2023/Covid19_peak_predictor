import pandas as pd
import numpy as np

df = pd.read_csv("covid_19_india_data.csv")
#print(df)

df = df.drop(['Sno'],axis = 1)
#print(df)

#df = df.groupby(df.Date).sum().reset_index()
#print(df)

#print(df.Date)
#df['T'] = np.arange(0, len(df))
#print(df)

x = 1
list_1 = [x]
for i in range (1, len(df)):
    x += df.Cnf_cases[i]
    list_1.append(x)
    
ser = pd.Series(list_1)
df.insert(4,'N', ser)

x_2 = 1
list = []
for i in range (0, len(df)):
    x_2 = df.N[i] ** 2
    list.append(x_2)
    
ser = pd.Series(list)


# In[11]:


df.insert(5,'N_squared', ser)

print(df)
print(df.iloc[23,:])

df.to_csv("Clean_data.csv")
