# Census Data Aggregator

## Overview
This application aggregates data from the Census API and presents it in an easily readable tabular format using the Shiny for Python framework. 
It is designed for researchers who need quick access to Census data with interactive filtering, visualization, and export functionalities.

## Features
- **Fetch Census Data**: Retrieve and process Census data dynamically.
- **Interactive Table**: View, sort, and filter data interactively.
- **Data Visualization**: Display Census data on a map using Leaflet.
- **Export Options**: Download data in CSV, Excel, or image formats.

## Requirements
Ensure you have the following dependencies installed:

```sh
pip install shiny pandas matplotlib geopandas xlsxwriter io
```

## File Structure
- `app.py` - Main application file containing the Shiny app logic.
- `census_api.py` - Fetches and processes Census data.
- `utils.py` - Utility functions for data transformation.
- `requirements.txt` - List of required Python packages.
- `README.md` - Project documentation.

## Usage
Run the application using the command:

```sh
shiny run --reload app.py
```

Then open the provided URL in your web browser to interact with the application.

## Exporting Data
The application allows users to export data in multiple formats:
- **CSV**: Download a `.csv` file.
- **Excel**: Download an `.xlsx` file.
- **JPG**: Save the table as an image.

## Contributions
Feel free to contribute by submitting issues or pull requests. 

## Current States
This website is currently hosted at https://molly-pop.shinyapps.io/fccc-census-webapp/

## License
This project is open-source and available under the MIT License.