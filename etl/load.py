import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

class Plotter:
    container = None
        
    def reload(self):
        self.container = st.container(border=True)
    
    def plot(self, company_data: pd.DataFrame, data: pd.DataFrame, year_columns: list, company_name: str):
        if data.empty:
            self.container.write("No data available for the selected company or sector.")
            return

        sector = data["Sector"].iloc[0]
        for _, emission_benchmark in data.iterrows():
            self.subplot(sector, company_data, emission_benchmark, year_columns, company_name)
        
    def sector_data(self, company_data: pd.DataFrame, sector: str):
        sector_data = company_data[company_data["Sector"] == sector]
        return sector_data
    
    def sector_minmax(self, company_data: pd.DataFrame, year_columns: list, sector: str):
        sector_data = self.sector_data(company_data, sector)
        sector_min = sector_data[year_columns].min()
        sector_max = sector_data[year_columns].max()
        return sector_min, sector_max
    
    def subplot(self, sector: str, company_data: pd.DataFrame, emission_benchmark: pd.DataFrame, year_columns: list, company_name: str):
        fig, ax = plt.subplots(figsize=(10, 6))

        emissions = emission_benchmark.loc[[f"{year}_company" for year in year_columns]].values
        sector_benchmark = emission_benchmark.loc[[f"{year}_sector" for year in year_columns]].values
        year_values = [int(year) for year in year_columns]
        
        ax.stem(year_values, emissions, linefmt="blue", markerfmt="bo", basefmt="r-", label=f"{company_name} Emissions")
        ax.stem(year_values, sector_benchmark, linefmt="green", markerfmt="o", basefmt="-r", label=f"{sector} Sector Benchmark")
        
        ax.set_xlabel("Year")
        ax.set_ylabel(emission_benchmark["Unit"])
        ax.set_title(emission_benchmark["Scenario name"])
        ax.legend()
        ax.grid(True)

        self.container.pyplot(fig)
