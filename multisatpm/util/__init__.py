def _restrict_to_conus(df):

    # Restrict to CONUS
    x0 = -124.7844079
    x1 = -66.9513812
    y0 = 24.7433195
    y1 = 49.3457868
    df_conus = df.loc[y1:y0, x0:x1]

    return df_conus
