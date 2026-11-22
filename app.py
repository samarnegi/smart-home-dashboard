import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Smart Home Automation Dashboard",
    page_icon="🏠",
    layout="wide"
)

DATA_FILE = Path(__file__).parent / "data" / "cleaned_dataset.csv"

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    for col in ["temperature_C", "humidity_pct", "value", "alert_flag"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    return data

st.title("🏠 IoT-Based Smart Home Automation System")
st.caption("Software dashboard using the supplied CSV dataset — not connected to live sensors.")

try:
    df = load_data(DATA_FILE)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.info("Keep cleaned_dataset.csv in the same folder as app.py.")
    st.stop()

# Sidebar filters
st.sidebar.header("Dashboard Filters")
rooms = sorted(df["room"].dropna().astype(str).unique())
sensors = sorted(df["sensor_type"].dropna().astype(str).unique())
devices = sorted(df["device_id"].dropna().astype(str).unique())

selected_rooms = st.sidebar.multiselect("Select room(s)", rooms, default=rooms)
selected_sensors = st.sidebar.multiselect("Select sensor type(s)", sensors, default=sensors)
selected_devices = st.sidebar.multiselect("Select device(s)", devices, default=devices)

filtered = df[
    df["room"].astype(str).isin(selected_rooms)
    & df["sensor_type"].astype(str).isin(selected_sensors)
    & df["device_id"].astype(str).isin(selected_devices)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Change the filters in the sidebar.")
    st.stop()

# KPI cards
total_records = len(filtered)
device_count = filtered["device_id"].nunique()
alert_count = int((filtered["alert_flag"] == 1).sum())
alert_pct = (alert_count / total_records * 100) if total_records else 0
avg_temp = filtered["temperature_C"].mean()
avg_humidity = filtered["humidity_pct"].mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Records", f"{total_records:,}")
c2.metric("Devices", f"{device_count:,}")
c3.metric("Alert labels", f"{alert_count:,}", f"{alert_pct:.2f}% of filtered records")
c4.metric("Mean temperature", f"{avg_temp:.2f} °C" if pd.notna(avg_temp) else "N/A")
c5.metric("Mean humidity", f"{avg_humidity:.2f}%" if pd.notna(avg_humidity) else "N/A")

st.divider()

# Charts
left, right = st.columns(2)
with left:
    st.subheader("Temperature distribution")
    temp_data = filtered.dropna(subset=["temperature_C"])
    if not temp_data.empty:
        fig = px.histogram(temp_data, x="temperature_C", nbins=25,
                           labels={"temperature_C": "Temperature (°C)"},
                           title="Temperature values")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No temperature values available for these filters.")

with right:
    st.subheader("Humidity distribution")
    humidity_data = filtered.dropna(subset=["humidity_pct"])
    if not humidity_data.empty:
        fig = px.histogram(humidity_data, x="humidity_pct", nbins=25,
                           labels={"humidity_pct": "Relative humidity (%)"},
                           title="Humidity values")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No humidity values available for these filters.")

st.subheader("Records by room")
room_counts = filtered["room"].value_counts().rename_axis("room").reset_index(name="records")
if not room_counts.empty:
    fig = px.bar(room_counts, x="room", y="records", text="records",
                 labels={"room": "Room", "records": "Number of records"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Daily mean temperature")
time_data = filtered.dropna(subset=["timestamp", "temperature_C"]).copy()
if not time_data.empty:
    daily = time_data.set_index("timestamp").resample("D")["temperature_C"].mean().reset_index()
    fig = px.line(daily, x="timestamp", y="temperature_C", markers=True,
                  labels={"timestamp": "Date", "temperature_C": "Mean temperature (°C)"})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No timestamped temperature values available.")

st.divider()

# Alerts
st.subheader("Alert records")
alerts = filtered[filtered["alert_flag"] == 1].sort_values("timestamp", ascending=False)
st.caption("These are records carrying alert_flag = 1 in the supplied dataset. The original alert-generation rule has not been independently verified.")
if alerts.empty:
    st.success("No alert-labelled records in the current filter selection.")
else:
    st.dataframe(alerts, use_container_width=True, hide_index=True)

# Full filtered data and download
with st.expander("View filtered dataset"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download filtered data as CSV",
    data=csv_bytes,
    file_name="smart_home_filtered_data.csv",
    mime="text/csv"
)

st.divider()
st.caption(
    "Project limitation: this dashboard analyses a static CSV file. "
    "It does not currently receive live ESP32/sensor data, send MQTT commands, "
    "or operate a physical relay or appliance."
)
