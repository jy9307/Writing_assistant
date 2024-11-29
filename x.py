import pandas as pd

user_df = pd.read_csv("users.csv", dtype={'번호': str})
user_dict = {}
for i in range(len(user_df)) :
    user_dict[user_df.iloc[i,1]] = str(user_df.iloc[i,0])

print(user_dict)