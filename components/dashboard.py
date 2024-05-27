import streamlit as st
import numpy as np
from etl.extract import DataLoader
from etl.transform import DataTransformer
from etl.load import Plotter
from scipy.spatial.distance import euclidean

class Dashboard:
    years = [str(year) for year in range(2013, 2051)]
    
    def __init__(self, company_loader: DataLoader, sector_loader: DataLoader, transformer: DataTransformer, plotter: Plotter):
        self.company_loader = company_loader
        self.sector_loader = sector_loader
        self.transformer = transformer
        self.plotter = plotter
        
        self.company_df = self.company_loader.load_data("data/TPI sector data - All sectors - 24052024/Company_Latest_Assessments.csv")
        self.sector_df = self.sector_loader.load_data("data/Sector_Benchmarks_24052024.csv")
        self.company_list = self.company_df.loc[self.company_df["Benchmark ID"].notnull(), "Company Name"].unique().tolist()
        
    def plot(self):
        self.plotter.reload()
        selected_company, selected_years = st.session_state["selected_company"], st.session_state["selected_years"]
        merged_data = self.transformer.transform(self.company_df, self.sector_df, selected_company, selected_years)
        self.plotter.container.dataframe(merged_data.head())
        self.plotter.plot(self.company_df, merged_data, selected_years, selected_company)
    
    def similarity(self, target_data, compare_data):
        years = st.session_state["selected_years"]
        target_values = target_data[years]
        target_values = target_values.fillna(10**10).values.flatten()
        compare_values = compare_data[years]
        compare_values = compare_values.fillna(10**10).values.flatten()
        
        return euclidean(target_values, compare_values)
    
    def related_companies(self):
        selected_company = st.session_state["selected_company"]
        sector = self.company_df[self.company_df["Company Name"] == selected_company]["Sector"].values[0]
        benchmark_id = self.company_df[self.company_df["Company Name"] == selected_company]["Benchmark ID"].values[0]
        companies_in_sector = self.company_df[
            (self.company_df["Sector"] == sector) & 
            (self.company_df["Benchmark ID"] == benchmark_id) &
            (self.company_df["Company Name"] != selected_company)]
        
        current_company = self.company_df[self.company_df["Company Name"] == selected_company]
        
        companies_in_sector["Similarity"] = companies_in_sector.apply(lambda row: self.similarity(current_company, row), axis=1)
        
        related_companies = companies_in_sector.sort_values("Similarity").head(5)
        
        self.plotter.container.write("Related companies:")
        for company in related_companies["Company Name"]:
            def on_select_related_company(key):
                key = key.split("_")[-1]
                index = self.company_list.index(key)
                st.session_state["selection"] = index
                st.session_state["selected_company"] = key
                print(st.session_state)
            self.plotter.container.button(company, on_click=on_select_related_company, key=f"related_company_{company}", args=[f"related_company_{company}"])

    
    def run(self):
        st.title("Emission projection")
        
        st.write("Company Data")
        st.dataframe(self.company_df.head())

        st.write("Sector Data")
        self.sector_df.rename(columns={"Sector name": "Sector"}, inplace=True)
        st.dataframe(self.sector_df.head())
        
        def on_select_years(key):
            st.session_state[key] = st.session_state[key]
            self.plot()
            
        def on_select_company(key):
            st.session_state[key] = st.session_state[key]
            self.plot()
            self.related_companies()
        
        if "selection" not in st.session_state:
            st.session_state["selection"] = 0
        st.selectbox("Select Company", self.company_list, on_change=on_select_company, key="selected_company", args=["selected_company"], index=st.session_state["selection"])
        st.multiselect("Select Years", self.years, default=self.years, on_change=on_select_years, key="selected_years", args=["selected_years"])
        
        self.plot()
        self.related_companies()

