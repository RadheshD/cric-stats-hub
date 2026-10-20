# Cricket Match Stats manager

Python-based tool to parse, analyze, visualize, and manage cricket match statistics. This project demonstrates end-to-end data processing—from reading raw JSON files to generating professional PDF reports, Excel spreadsheets, and storing data in a MySQL database.

##  Features

- **Data Parsing & Formatting:** Reads match data from JSON and formats it into clean, readable console tables using Pandas.
- **File Conversions:** Converts JSON data to `.xlsx` and `.csv` formats, and vice versa.
- **Data Visualization:** Generates informative charts (bar charts, pie charts) using Matplotlib to visualize team scores, batting contributions, and bowling performances.
- **PDF Reporting:** Automatically compiles match data and generated charts into a well-formatted PDF report using ReportLab.
- **File Management:** Demonstrates automated file operations like copying, renaming, updating specific JSON values, and deleting files.
- **Database Integration:** Seamlessly connects to a MySQL database to create tables, insert match records, fetch data, and export database contents to JSON, Excel, and HTML formats.

## 📋 Prerequisites

- **Python 3.x** installed on your system.
- **MySQL Server** installed and running (for database integration features). 

## 🚀 Setup and Installation

1. **Clone or Download the Repository:**
   Ensure you have all the project files in a single directory.

2. **Database Configuration:**
   Open `database_manager.py` and ensure the `DB_CONFIG` matches your local MySQL server credentials (username, password, host).

3. **Install Dependencies:**
   This project comes with a pre-configured virtual environment (`venv`). All required libraries are listed in `requirements.txt`.
   - `pandas`
   - `openpyxl`
   - `matplotlib`
   - `reportlab`
   - `mysql-connector-python`

## 💻 How to Run

**The easiest way to run the project on Windows is by using the provided batch file:**

Double-click `run_project.bat` or run it from your command prompt / PowerShell:
```powershell
.\run_project.bat
```
*This script will automatically activate the virtual environment and execute the main program.*

**Alternative (Manual Run):**
If you prefer to run it manually, you must activate the virtual environment first:

```powershell
# Activate the virtual environment
.\venv\Scripts\activate

# Run the main application
python main.py
```

## 📁 Project Structure

```text
├── data/
│   └── match_stats.json          # Source JSON data
├── output/                       # Generated Excel, CSV, and modified JSON files
├── charts/                       # Generated Matplotlib charts (.png)
├── reports/                      # Generated PDF reports
├── main.py                       # Main application entry point
├── file_manager.py               # Handles file I/O and JSON modifications
├── data_converter.py             # Handles JSON to CSV/Excel conversions and table printing
├── chart_generator.py            # Generates visualizations using matplotlib
├── pdf_generator.py              # Creates the PDF report using reportlab
├── database_manager.py           # Manages MySQL DB connection, queries, and exports
├── requirements.txt              # Project dependencies
└── run_project.bat               # Windows batch script to run the app
```
