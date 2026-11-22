# Samar — IoT-Based Smart Home Automation System

## Project scope
This is a software-only, dataset-based smart-home monitoring prototype. It analyses a supplied CSV dataset and presents interactive summaries and charts. It is not connected to physical sensors, ESP32/Arduino hardware, MQTT, relays, or appliances.

## Folder contents
- `app.py` — Streamlit dashboard
- `eda_analysis.py` — dataset cleaning and exploratory analysis script
- `data/cleaned_dataset.csv` — dataset used by both scripts
- `requirements.txt` — Python dependencies
- `eda_outputs/` — generated analysis charts

## Run on Windows 11
1. Install Python 3.10 or newer.
2. Extract the project ZIP.
3. Open the extracted `Samar_Final_Project` folder.
4. Click the File Explorer address bar, type `cmd`, and press Enter.
5. Run:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python eda_analysis.py
streamlit run app.py
```

The dashboard should open at the local URL printed in the terminal, usually `http://localhost:8501`.

## Run EDA with another CSV
```bat
python eda_analysis.py path\to\your_dataset.csv
```

## Dataset notes
The supplied dataset contains 5,000 rows and 8 columns. It has 0 missing cells and 0 exact duplicate rows. The supplied `alert_flag` is treated as an existing label; its generation rule has not been independently validated. The generic `value` field has no universal unit in the supplied schema.

## Deployment
For Streamlit Community Cloud, push this folder's contents to your own GitHub repository and select `app.py` as the app entry point. Do not use another student's repository or deployment URL.
