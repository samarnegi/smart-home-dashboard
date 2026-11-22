"""
IoT-Based Smart Home Automation System — Step 1 EDA
Run: python eda_analysis.py dataset_5000_rows.csv
Requires: pandas, matplotlib
"""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

input_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/cleaned_dataset.csv")
out = Path("eda_outputs")
out.mkdir(exist_ok=True)

df = pd.read_csv(input_file)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
for col in ["temperature_C", "humidity_pct", "value", "alert_flag"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.sort_values("timestamp", kind="stable").reset_index(drop=True)
df.to_csv(out / "cleaned_dataset.csv", index=False)

print("Shape:", df.shape)
print("Missing cells:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))
print("Unique devices:", df["device_id"].nunique())
print("Temperature mean/range:", df["temperature_C"].mean(), df["temperature_C"].min(), df["temperature_C"].max())
print("Humidity mean/range:", df["humidity_pct"].mean(), df["humidity_pct"].min(), df["humidity_pct"].max())
print("Alert count:", int((df["alert_flag"] == 1).sum()))

plots = [
    ("temperature_C", "Temperature Distribution", "Temperature (°C)", "01_temperature_distribution.png"),
    ("humidity_pct", "Humidity Distribution", "Relative humidity (%)", "02_humidity_distribution.png"),
]
for col, title, xlabel, filename in plots:
    plt.figure(figsize=(8, 5))
    plt.hist(df[col].dropna(), bins=20)
    plt.title(title); plt.xlabel(xlabel); plt.ylabel("Number of records")
    plt.tight_layout(); plt.savefig(out / filename, dpi=160); plt.close()

counts = df["room"].value_counts()
plt.figure(figsize=(8, 5))
plt.bar(counts.index, counts.values)
plt.title("Records by Room"); plt.xlabel("Room"); plt.ylabel("Number of records")
plt.xticks(rotation=25, ha="right")
plt.tight_layout(); plt.savefig(out / "03_records_by_room.png", dpi=160); plt.close()

daily = df.set_index("timestamp")["temperature_C"].resample("D").mean()
plt.figure(figsize=(9, 5))
plt.plot(daily.index, daily.values)
plt.title("Daily Mean Temperature Over Time")
plt.xlabel("Date"); plt.ylabel("Mean temperature (°C)")
plt.tight_layout(); plt.savefig(out / "04_daily_mean_temperature.png", dpi=160); plt.close()

alerts = df["alert_flag"].value_counts().sort_index()
plt.figure(figsize=(7, 5))
plt.bar([str(x) for x in alerts.index], alerts.values)
plt.title("Alert Flag Counts"); plt.xlabel("Alert flag"); plt.ylabel("Number of records")
plt.tight_layout(); plt.savefig(out / "05_alert_flag_counts.png", dpi=160); plt.close()

print(f"Outputs saved in: {out.resolve()}")
