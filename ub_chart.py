import pandas as pd 
import os

data_path = os.path.dirname(__file__)

ceevee = f'{data_path}/data/unemploymentsicknessandbenefits.xlsx'

df = pd.read_excel(ceevee)
df = df[['Date of effect', '21 years']]
df = df.dropna()

hundert = df.loc[df['Date of effect'] == '20/9/2011']['21 years'].values

df['reindexed'] = (df['21 years']/hundert)*100

# print(df.loc[df['Date of effect'] == '20/9/2011']['21 years'].values)

print(df)


# import matplotlib.pyplot as plt
# import seaborn as sns 
# plt.style.use('seaborn-whitegrid')

# sns.lineplot(data = df, x="Date of effect", y="21 years")

# plt.show()

# with open(f"{data_path}/data/ubpaymentcleaned.csv", "w") as f:
#     df.to_csv(f, index=False, header=True)