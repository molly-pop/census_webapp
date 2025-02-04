from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
#from shinywidgets import render_plotly
import geopandas as gpd
from modules import table_server, table_ui

from shiny import App, Inputs, Outputs, Session, reactive, render, ui

# Prepare a DataFrame
df = pd.read_csv(Path(__file__).parent /"utils/csv/Molly_shiny_data.csv", skipinitialspace=True)
catchment = gpd.read_file(Path(__file__).parent /"utils/geofiles/Full_catch.geojson")
nj = gpd.read_file(Path(__file__).parent /"utils/geofiles/NJ_state.geojson")
northPhilly = gpd.read_file(Path(__file__).parent /"utils/geofiles/NorthPhillyOnly.geojson")
pa = gpd.read_file(Path(__file__).parent /"utils/geofiles/PA_state.geojson")
philly = gpd.read_file(Path(__file__).parent /"utils/geofiles/Philly_only_catch.geojson")

from utils.text import (
    about_text
)

css_file = Path(__file__).parent / "utils" / "css" / "my-styles.css"

#df.columns = df.columns.str.replace('', 'Record #')
df.columns = df.columns.str.replace('year', 'Year')
df.columns = df.columns.str.replace('total_pop', 'Total Population')
df.columns = df.columns.str.replace('prc_female', 'Population that is Female (%)')
df.columns = df.columns.str.replace('prc_male', 'Population that is Male (%)')
df.columns = df.columns.str.replace('median_age', 'Median Age of Resident in Geographic Area')
df.columns = df.columns.str.replace('prc_pop_65Up', 'Population that is Age 65 or Older (%)')
df.columns = df.columns.str.replace('prc_pov', 'Population Whose Income in the Past 12 Months Was Below the Poverty Level (%)')
df.columns = df.columns.str.replace('prc_NHWhite', 'Population that identifies as Non-Hispanic White (%)')
df.columns = df.columns.str.replace('prc_NHBlack', 'Population that identifies as Non-Hispanic Black (%)')
df.columns = df.columns.str.replace('prc_NHAsian', 'Population that identifies as Non-Hispanic Asian (%)')
df.columns = df.columns.str.replace('prc_HispanicAn', 'Population that identifies as Hispanic of any race (%)')
df.columns = df.columns.str.replace('prc_Birth_foreign', 'Population that was born outside of the U.S. (%)')
df.columns = df.columns.str.replace('prc_educ_ltHS', 'Population With Less Than a High School Degree (%)')
df.columns = df.columns.str.replace('prc_employed', 'Population Who is Currently Employed (%)')
df.columns = df.columns.str.replace('prc_trans_tran', 'Workers Who Commute on Public Transit (%)')
df.columns = df.columns.str.replace('prc_renterocc_hh', 'Households That Are Occupied by Renters (%)')
df.columns = df.columns.str.replace('prc_same_house', 'Population Who Have Lived in the Same House for At Least a Year (%)')
df.columns = df.columns.str.replace('hh_income', 'Median Household Income')

app_ui = ui.page_navbar(
    table_ui("tab1"),
    #graph_ui("tab2"),
    #createRequest_ui("tab3"),
    sidebar=ui.sidebar(
        ui.tags.div(
            about_text
        ),
        ui.input_select(
            "year",
            "Year",
            choices=[
                "2014",
                "2015",
                "2016",
                "2017",
                "2018",
                "2019",
                "2020",
                "2021",
                "2022",
            ],
        ), ui.input_checkbox_group(
                "geographics",  
                "Select geographic levels(s) below",
                {
                    "North Philly": ui.span("North Philly"),
                    "Philadelphia": ui.span("Philadelphia"),
                    "FCCC Catchment": ui.span("FCCC Catchment"),
                    "PA": ui.span("PA"),
                    "NJ": ui.span("NJ"),
                    "U.S.": ui.span("U.S.")
                }, selected=["North Philly", "Philadelphia", "FCCC Catchment", "PA", "NJ", "U.S."]
            ), ui.input_checkbox_group(
                "variables",
                "Select statistical variable(s) below",
                {
                    "Median Age of Resident in Geographic Area": ui.span("Median Age of Resident in Geographic Area"),
                    "Population that is Age 65 or Older (%)": ui.span("Population that is Age 65 or Older (%)"),
                    "Total Population": ui.span("Total Population"),
                    "Population that is Male (%)": ui.span("Population that is Male (%)"),
                    "Population that is Female (%)": ui.span("Population that is Female (%)"),
                    "Population Whose Income in the Past 12 Months Was Below the Poverty Level (%)": ui.span("Population Whose Income in the Past 12 Months Was Below the Poverty Level (%)"),
                    "Population that identifies as Non-Hispanic White (%)": ui.span("Population that identifies as Non-Hispanic White (%)"),
                    "Population that identifies as Non-Hispanic Black (%)": ui.span("Population that identifies as Non-Hispanic Black (%)"),
                    "Population that identifies as Non-Hispanic Asian (%)": ui.span("Population that identifies as Non-Hispanic Asian (%)"),
                    "Population that identifies as Hispanic of any race (%)": ui.span("Population that identifies as Hispanic of any race (%)"),
                    "Population that was born outside of the U.S. (%)": ui.span("Population that was born outside of the U.S. (%)"),
                    "Population With Less Than a High School Degree (%)": ui.span("Population With Less Than a High School Degree (%)"),
                    "Population Who is Currently Employed (%)": ui.span("Population Who is Currently Employed (%)"),
                    "Workers Who Commute on Public Transit (%)": ui.span("Workers Who Commute on Public Transit (%)"),
                    "Households That Are Occupied by Renters (%)": ui.span("Households That Are Occupied by Renters (%)"),
                    "Population Who Have Lived in the Same House for At Least a Year (%)": ui.span("Population Who Have Lived in the Same House for At Least a Year (%)"),
                    "Median Household Income": ui.span("Median Household Income")
                } #, selected=["Median Age of Resident in Geographic Area",
                           # "Population that is Age 65 or Older (%)",
                           # "Total Population",
                           # "Population that is Male (%)",
                            #"Population that is Female (%)",
                           # "Population Whose Income in the Past 12 Months Was Below the Poverty Level (%)",
                           # "Population that identifies as Non-Hispanic White (%)",
                           # "Population that identifies as Non-Hispanic Black (%)",
                           # "Population that identifies as Non-Hispanic Asian (%)",
                           # "Population that identifies as Hispanic of any race (%)",
                           # "Population that was born outside of the U.S. (%)",
                           # "Population With Less Than a High School Degree (%)",
                           # "Population Who is Currently Employed (%)",
                           # "Workers Who Commute on Public Transit (%)",
                           # "Households That Are Occupied by Renters (%)",
                           # "Population Who Have Lived in the Same House for At Least a Year (%)",
                           # "Median Household Income"]
            ),
        ui.include_css(css_file),
        width="500px",
    ),
    id="tabs",
    title="FCCC TableMaker",
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc()
    def filtered_data() -> pd.DataFrame:

        queryGeoArray = input.geographics()
        queryVarArray = input.variables()

        df2 = df.pivot_table(
            values=queryVarArray,
            columns=["Year", "geographic_unit"]
        )

        yearly = int(input.year())
        df3 = df2[df2.columns[df2.columns.get_level_values(0) == yearly]]
        df3.columns = df3.columns.droplevel(0)

        df4 = df3.filter(items=queryGeoArray, axis=1).reset_index()

        print(df4)
        return df4

    @reactive.Calc()
    def geographies():
        return input.geographics()

    def title():
        return input.year()

    def styled():
        header_styles = [
            {
                'selector': 'th',
                'props': [
                    ('background-color', 'whitesmoke'),
                    ('color', 'darkslategrey'),
                    ('border', '1px solid lightgrey'),
                    ('text-align', 'center'),
                    ('padding', '10px'),
                ]
            }
        ]
        def custom_format(val):
            if isinstance(val, (int, float)):  # Check if value is integer or float
                if isinstance(val, float) and val.is_integer():
                    return '{:,.0f}'.format(
                        val)  # Return as integer with comma for thousands separator if it's a whole number
                else:
                    return '{:,.1f}'.format(
                        val)  # Return with 1 decimal and comma for thousands separator if it's not a whole number
            else:
                return val  # Return as is for non-numeric values

        df4 = filtered_data()
        df5 = df4.style.format(custom_format).hide(axis=0).\
            set_properties(**{"background-color": "white", "color": "darkslategrey",
                         "border": "1px solid lightgrey", "padding": "10px",
                          "align": "center"}).set_table_styles(header_styles)
        return df5

    table_server(id="tab1", df=filtered_data, df_styled=styled,  geographics=geographies, title=title)
    #graph_server(id="tab2", df=filtered_data)
    #createRequest_server(id="tab3", df=filtered_data)


app = App(app_ui, server)


