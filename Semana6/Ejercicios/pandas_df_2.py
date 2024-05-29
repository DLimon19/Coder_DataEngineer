import pandas as pd

df = pd.read_csv("./Data/train.csv")

print(df.groupby(["Sex"]).PassengerId.count())

print(df.groupby(["Pclass"]).Fare.mean())

print(df["Age"].max())

print(df.groupby(["Pclass"])[["Fare","Age"]].mean())