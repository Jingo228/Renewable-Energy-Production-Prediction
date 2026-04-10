import pandas as pd

def load_data (file_path:str, skiprows=0):
    return pd.read_csv(file_path, skiprows=skiprows)

def wide_to_long(df, value_name, id_vars=None):
    if id_vars is None:
        id_vars = ['Country Name', 'Country Code']

    year_cols = [c for c in df.columns if str(c).isdigit()]
    df_long = pd.melt(
        df,
        id_vars=id_vars,
        value_vars=year_cols,
        var_name="Year",
        value_name=value_name
    )
    df_long["Year"] = df_long["Year"].astype(int)
    return df_long

def clean_data(df, value_col, country_col="Country Code", year_col="Year",
               start_year=2000, end_year=2025, min_non_null_years=5):
    df = df.copy()

    # keep only desired years
    df = df[df[year_col].between(start_year, end_year)]

    # drop rows where the target/value is missing
    df = df[df[value_col].notna()]

    # keep only countries with enough non-null years
    df = df.groupby(country_col).filter(lambda x: len(x) >= min_non_null_years)

    return df.reset_index(drop=True)
