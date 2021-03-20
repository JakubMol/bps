import pandas as pd



def load_housing_data():
    csv_path = ".//data//fires//fire_nrt_M6_96617.csv"
    return pd.read_csv(csv_path)
