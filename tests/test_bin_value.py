import pandas as pd 
import numpy as np 

df_raw = pd.read_csv(r"sample_wafermap_data.csv", index_col=False)

# Filter out rows based on "sort_test_flag"
df = df_raw[df_raw["sort_test_flag"] == "T"]

print(df.columns)

print(df.head(n=2))