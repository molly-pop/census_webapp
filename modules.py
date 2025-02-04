from typing import Callable, Any, Literal
from pathlib import Path
from io import BytesIO
from shinywidgets import output_widget, render_widget
from ipyleaflet import GeoJSON, Map, Marker, basemaps
import pandas as pd
import matplotlib.pyplot as plt
import shiny.experimental as x
import json
import geopandas as gpd
import plotly.io as pio
from typing import Tuple
import df2img
import random
from plots import plot_auc_curve, plot_precision_recall_curve, plot_score_distribution
from shiny import Inputs, Outputs, Session, module, render, ui, reactive, req

with open(Path(__file__).parent / "utils/geofiles/Full_catch.geojson", "r") as f:
    catch_boundaries = json.load(f)
with open(Path(__file__).parent / "utils/geofiles/NJ_state.geojson", "r") as f:
    nj_boundaries = json.load(f)
with open(Path(__file__).parent / "utils/geofiles/PA_state.geojson", "r") as f:
    pa_boundaries = json.load(f)
with open(Path(__file__).parent / "utils/geofiles/Philly_only_catch.geojson", "r") as f:
    philly_boundaries = json.load(f)
with open(Path(__file__).parent / "utils/geofiles/NorthPhillyOnly.geojson", "r") as f:
    northPhilly_boundaries = json.load(f)

ui.include_css(
    Path(__file__).parent / "utils/css/my-styles.css"
)

# @module.ui
# def graph_ui():
#     return ui.nav_panel(
#         "Training Dashboard",
#         ui.layout_columns(
#             ui.card(
#                 ui.card_header("Model Metrics"),
#                 ui.output_plot("metric"),
#                 ui.input_select(
#                     "metric",
#                     "Metric",
#                     choices=["ROC Curve", "Precision-Recall"],
#                 ),
#             ),
#             ui.card(
#                 ui.card_header("Training Scores"),
#                 ui.output_plot("score_dist"),
#             ),
#         ),
#     )

@module.server
def graph_server(
    input: Inputs,
    output: Outputs,
    session: Session,
    df: Callable[[], pd.DataFrame]
):
    @render.plot
    def score_dist():
        return plot_score_distribution(df())

    @render.plot
    def metric():
        if input.metric() == "ROC Curve":
            return plot_auc_curve(df(), "year", "total_pop")
        else:
            return plot_precision_recall_curve(df(), "year", "total_pop")

@module.ui
def table_ui():
    return ui.nav_panel(
        "View Data",
        ui.layout_columns(
            ui.card(ui.output_text("table_title"),),
            ui.card(ui.card_header("Catchment Area Map"), output_widget("catchmap")),
            ui.card(ui.output_data_frame("census_df")),
            ui.card(
                ui.layout_columns(
                ui.value_box(
                        title="Row count",
                        value=ui.output_text("row_count"),
                        theme="primary"
                    ),
                ui.card(
                ui.download_button("csv", "Export to CSV", class_="btn-success"),
                        ui.download_button("excel", "Export to Excel", class_="btn-success"),
                        ui.download_button("jpg", "Export to JPG", class_="btn-success")
                    ),
                    width=1/2
                 ),
              ),
            col_widths=[900,900,900]),
        )


def format_number(x):
    if isinstance(x, (int, float)):
        return '{:,.1f}'.format(x)
    return x


@module.server
def table_server(
    input: Inputs, 
    output: Outputs, 
    session: Session, 
    df: Callable[[], pd.DataFrame],
    df_styled: Callable[[], pd.DataFrame.style],
    geographics: Callable[[], Tuple[str]],
    title="{Year}"):
    @render_widget
    def catchmap():
        print(geographics())
        map = Map(basemap=basemaps.CartoDB.Positron, center=(40.970678269829946, -75.8396545256453), zoom=6)

        geo_json_pa = GeoJSON(
            data=pa_boundaries,
            style={
                "opacity": 1,
                "dashArray": "0",
                "fillOpacity": 0.2,
                "weight": 1,
                "color": "black",
                "fillColor": "lightcoral"
            },
            hover_style={"color": "black", "dashArray": "0", "fillColor": "lightblue", "fillOpacity": 0.7},
        )
        geo_json_nj = GeoJSON(
            data=nj_boundaries,
            style={
                "opacity": 1,
                "dashArray": "0",
                "fillOpacity": 0.2,
                "weight": 1,
                "color": "black",
                "fillColor": "lightcoral"
            },
            hover_style={"color": "black", "dashArray": "0","fillColor": "lightblue", "fillOpacity": 0.7},
        )
        geo_json_catch = GeoJSON(
            data=catch_boundaries,
            style={
                "opacity": 1,
                "dashArray": "0",
                "fillOpacity": 0.2,
                "weight": 1,
                "color": "black",
                "fillColor": "lightcoral"
            },
            hover_style={"color": "black", "dashArray": "0", "fillColor": "lightblue", "fillOpacity": 0.7},
        )
        geo_json_philly = GeoJSON(
            data=philly_boundaries,
            style={
                "opacity": 1,
                "dashArray": "0",
                "fillOpacity": 0.2,
                "weight": 1,
                "color": "black",
                "fillColor": "lightcoral"
            },
            hover_style={"color": "black", "dashArray": "0","fillColor": "lightblue",  "fillOpacity": 0.7},
        )
        geo_json_northPhilly = GeoJSON(
            data=northPhilly_boundaries,
            style={
                "opacity": 1,
                "dashArray": "0",
                "fillOpacity": 0.2,
                "weight": 1,
                "color": "black",
                "fillColor": "lightcoral"
            },
            hover_style={"color": "black", "dashArray": "0","fillColor": "lightblue", "fillOpacity": 0.7},
        )
        if ('PA') in geographics():
            map.add(geo_json_pa)
        if ('NJ') in geographics():
            map.add(geo_json_nj)
        if ('FCCC Catchment') in geographics():
            map.add(geo_json_catch)
        if ('Philadelphia') in geographics():
            map.add(geo_json_philly)
        if 'North Philly' in geographics():
            map.add(geo_json_northPhilly)
        return map
    
    @render.text
    def table_title():
        return f"Characteristics of Resident Populations from {title()} Census 5-Year Estimate"
    
    @render.text
    def row_count():
        return df().shape[0]

    @render.data_frame
    def census_df():
        # Apply formatting logic to the DataFrame
        df_formatted = df().map(format_number)
        for x in df_formatted.index:
            print(df_formatted['index'].values)
        if 'Total Population' in df_formatted.index.values:
            # Apply format '{:,.1f}' for non-integer values, and '{:,.0f}' for integer values
            df_formatted.iloc[0] = df_formatted.iloc[0].map(
                lambda x: '{:,.1f}'.format(x) if x % 1 != 0 else '{:,.0f}'.format(x))

        return render.DataGrid(
            df_formatted,
            width="100%",
            height="100%",
            row_selection_mode="multiple",
        )

    @render.download(filename= lambda: f"Characteristics of Resident Populations from {title()} Census 5-Year Estimate.csv")
    def csv():
        yield df().to_csv(sep=',', encoding='utf-8', index=False)

    @render.download(
        filename=lambda: f"Characteristics of Resident Populations from {title()} Census 5-Year Estimate.png")
    def jpg():
        my_width = 0
        list_of_col_widths = [300]

        # Apply formatting logic to the DataFrame
        df_formatted = df().map(format_number)
        if 'Total Population' in df_formatted.index:
            df_formatted.loc['Total Population'] = df_formatted.loc['Total Population'].apply(
                lambda x: '{:,.0f}'.format(x))

        for x in range(1, len(df_formatted.columns) - 1):
            list_of_col_widths[0] += 20
        print(len(df_formatted.columns))
        for x in range(len(df_formatted.columns) - 1):
            list_of_col_widths.append(100)
        if df_formatted.shape[1] > 3:
            my_width = df_formatted.shape[1] * 100
        fig = df2img.plot_dataframe(
            df_formatted.round(1),
            tbl_header=dict(
                line_color='lightgrey',
                fill_color='whitesmoke',
                align=['left', 'center'],
                font=dict(
                    color="darkslategrey")
            ),
            print_index=False,
            tbl_cells=dict(
                fill_color='white',
                line_color='lightgrey',
                align=['left', 'center'],
                font=dict(
                    color="black"
                )
            ),
            col_width=list_of_col_widths,
            fig_size=(700 + my_width, (df_formatted.shape[0] + 1) * 40))

        # Convert Plotly figure to Matplotlib figure
        fig_bytes = pio.to_image(fig, format='png')
        buffer = BytesIO(fig_bytes)

        buffer.seek(0)  # Reset the buffer position to the beginning

        # Yield the PNG image data
        while True:
            chunk = buffer.read(65536)  # Read data in chunks
            if not chunk:
                break  # Break the loop when all data has been read
            yield chunk

