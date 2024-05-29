import pandas as pd

df = pd.read_csv('./Data/train.csv')

#print(df)

#print(df.dtypes)

#print(df[["Name","Age"]])

#print(df["Age"])

df2 = df[["Name","Age"]]

#print(df2)

#print(df.shape)
#print(df2.shape)

df3 = df[df["Age"] > 30]
#print(df3)

df_male = df[df["Sex"] == "male"]
#print(df_male)

df_class = df[df["Pclass"].isin([2,3])]
#rint(df_class)

#print(df.loc[:,["Name","Age"]])

#df["Fare_MXN"] = df["Fare"] * 17
#print(df)

def fare_with_rich_tax(x):
    if x["Pclass"] == 1:
        return x["Fare"] * 1.20
    else:
        return x["Fare"]

df["Fare_with_rich_tax"] = df.apply(fare_with_rich_tax, axis = 1)

df["Fare_with_rich_tax_2"] = df.apply(lambda x: x["Fare"] * 1.20 if x["Pclass"] == 1 else x["Fare"], axis = 1)


df_aux = pd.DataFrame({"Pclass": [1,2,3], "Pdesc" : ["Upper class","Medium class", "Lower class"]})

#df_merge = df.merge(df_aux, how="left", left_on="Pclass", right_on="Pclass")
df_merge = df.merge(df_aux, how="left", on="Pclass")
print(df_merge)