import streamlit as st
from etl.extract import CSVDataLoader
from etl.transform import DataTransformer
from etl.load import Plotter
from components.dashboard import Dashboard

def main():
    company_loader = CSVDataLoader()
    sector_loader = CSVDataLoader()
    transformer = DataTransformer()
    plotter = Plotter()
    dashboard = Dashboard(company_loader, sector_loader, transformer, plotter)
    dashboard.run()

if __name__ == "__main__":
    main()
