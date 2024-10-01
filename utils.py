import pandas as pd


def convert_to_datetime(df, colnames):
    for col in colnames:
        df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')

    return df


def filter_df(df):
    
    l = len(df)
    print(f"Got {l} records.")
    df = df[df["endyear"].notna()]
    print(f"Removed {l - len(df)} records that had no endyear.")
    
    l = len(df)
    df = df[(df["Fname"].notna()) | (df["Gname"].notna())]
    print(f"Removed {l - len(df)} records with neither Fname nor Gname.")

    l = len(df)
    df = df[(df["startyear"] < 2018) & (df["startyear"] > 1990)] # or covid?
    print(f"Removed {l - len(df)} records where the start year was either before 1990 or after 2018.")

    l = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Removed {l - len(df)} duplicate records.")

    print(f"{len(df)} records remaining.")
    return df
