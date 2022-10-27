import pandas as pd
from functools import reduce

def final_stats_table(stats, disease, list, inputRF):
    # Join the diseased plants and the healthy plants in one dataset to generate the input for the random forest algorithm
    df_all_info = pd.concat([disease, list], ignore_index=True)
    df_all_info2 = reduce(lambda left, right: pd.merge(left, right, on="plantID", how="outer"), [df_all_info, stats])
    df_all_info2["status"].fillna(value="noBOT", inplace=True)
    df_all_info2.to_csv(inputRF)

