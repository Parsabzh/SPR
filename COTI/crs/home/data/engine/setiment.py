import pandas as pd


df= pd.read_csv('sentiment.csv')



for index, row in df.iterrows():
    for col in df.columns:  # Including all columns
        item = row[col]
        if item is not None and item!= '' and pd.isna(item) is False:
            try:
                num = float(item.split('\n')[-1])
                if 0 <= num < 0.4:
                    df.at[index, col] = "Low"
                elif 0.4 <= num <= 0.6:
                    df.at[index, col] = "Medium"
                elif num > 0.6:
                    df.at[index, col] = "High"
            except ValueError:
                # Handle the case where the split and conversion to float might fail
                pass
                     
df.to_csv('modified_df.csv', index=True)