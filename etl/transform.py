import pandas as pd

class DataTransformer:
    def __init__(self):
        self.year_columns = []

    def identify_year_columns(self, df: pd.DataFrame):
        self.year_columns = [col for col in df.columns if col.isdigit()]

    def transform(self, company_df: pd.DataFrame, sector_df: pd.DataFrame, company_name: str, years: list):
        self.identify_year_columns(sector_df)
        
        company_data = company_df[company_df["Company Name"] == company_name]
        sector_data = sector_df[(sector_df["Benchmark ID"].isin(company_data["Benchmark ID"]))]
        
        merged_data = pd.merge(company_data, sector_data, on=["Sector", "Benchmark ID"], suffixes=("_company", "_sector"))
        
        return merged_data.set_index("Company Name")
