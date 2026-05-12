"""Build a larger real AQI training dataset.

This script combines:
- OpenAQ archived pollution measurements from the public S3 archive
- Open-Meteo archived weather observations for the same date/location

The resulting CSV keeps the app's existing schema:
`date, region, temperature, humidity, rainfall, aqi`

Run:
    python ml/build_real_dataset.py
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import math
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "sample_data", "air_quality_real.csv")
S3_BUCKET_URL = "https://openaq-data-archive.s3.amazonaws.com/"
S3_LIST_URL = "https://openaq-data-archive.s3.amazonaws.com/?prefix=records/csv.gz/&max-keys=1000"
MAX_FILES = 160


@dataclass(frozen=True)
class WeatherRow:
    temperature: float
    humidity: float
    rainfall: float


def list_archive_keys(limit: int) -> list[str]:
    """Return a deterministic slice of archived CSV objects."""
    root = ET.fromstring(urllib.request.urlopen(S3_LIST_URL, timeout=60).read())
    namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    keys = [
        element.find("s3:Key", namespace).text
        for element in root.findall("s3:Contents", namespace)
        if element.find("s3:Key", namespace).text.endswith(".csv.gz")
    ]
    return keys[:limit]


@lru_cache(maxsize=4096)
def fetch_weather(latitude: float, longitude: float, date: str) -> WeatherRow:
    """Fetch daily weather data from Open-Meteo for one day and point."""
    query = urllib.parse.urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": date,
            "end_date": date,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean",
            "timezone": "UTC",
        }
    )
    url = f"https://archive-api.open-meteo.com/v1/archive?{query}"
    with urllib.request.urlopen(url, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))

    daily = payload["daily"]
    temp_max = float(daily["temperature_2m_max"][0])
    temp_min = float(daily["temperature_2m_min"][0])
    humidity = float(daily["relative_humidity_2m_mean"][0])
    rainfall = float(daily["precipitation_sum"][0])
    temperature = round((temp_max + temp_min) / 2.0, 2)
    return WeatherRow(temperature=temperature, humidity=humidity, rainfall=rainfall)


def pm25_to_aqi(pm25: float) -> float:
    """Convert PM2.5 concentration to US EPA AQI."""
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    value = max(0.0, min(pm25, 500.4))
    for c_low, c_high, a_low, a_high in breakpoints:
        if c_low <= value <= c_high:
            return round(((a_high - a_low) / (c_high - c_low)) * (value - c_low) + a_low, 2)
    return 500.0


def download_archive_file(key: str) -> list[dict[str, str]]:
    url = S3_BUCKET_URL + key
    with urllib.request.urlopen(url, timeout=60) as response:
        raw = gzip.decompress(response.read()).decode("utf-8", errors="ignore")
    return list(csv.DictReader(io.StringIO(raw)))


def build_dataset(keys: Iterable[str]) -> list[dict[str, object]]:
    rows = []
    seen = set()

    for index, key in enumerate(keys, start=1):
        file_rows = download_archive_file(key)
        if not file_rows:
            continue

        sample = file_rows[0]
        location = sample["location"]
        latitude = float(sample["lat"])
        longitude = float(sample["lon"])
        date = sample["datetime"][:10]

        pm25_values = [float(row["value"]) for row in file_rows if row["parameter"] == "pm25"]
        pm10_values = [float(row["value"]) for row in file_rows if row["parameter"] == "pm10"]
        if pm25_values:
            pollution_value = sum(pm25_values) / len(pm25_values)
            source_parameter = "pm25"
        elif pm10_values:
            pollution_value = sum(pm10_values) / len(pm10_values)
            source_parameter = "pm10"
        else:
            continue

        key_id = (location, date)
        if key_id in seen:
            continue
        seen.add(key_id)

        weather = fetch_weather(latitude, longitude, date)
        rows.append(
            {
                "date": date,
                "region": location,
                "temperature": weather.temperature,
                "humidity": weather.humidity,
                "rainfall": weather.rainfall,
                "aqi": pm25_to_aqi(pollution_value),
                "pollution_parameter": source_parameter,
                "pollution_value": round(pollution_value, 2),
                "latitude": latitude,
                "longitude": longitude,
            }
        )

        if index % 25 == 0:
            print(f"Processed {index} archive files -> {len(rows)} dataset rows")

    return rows


def main() -> None:
    keys = list_archive_keys(MAX_FILES)
    if not keys:
        raise RuntimeError("No OpenAQ archive files were found")

    rows = build_dataset(keys)
    if len(rows) < 25:
        raise RuntimeError(f"Dataset too small after build: {len(rows)} rows")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["date", "region", "temperature", "humidity", "rainfall", "aqi"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "date": row["date"],
                    "region": row["region"],
                    "temperature": row["temperature"],
                    "humidity": row["humidity"],
                    "rainfall": row["rainfall"],
                    "aqi": row["aqi"],
                }
            )

    print(f"Saved {len(rows)} real rows to {OUTPUT_PATH}")
    print("Source: OpenAQ public S3 archive (pollution) + Open-Meteo archive API (weather)")
    print("OpenAQ archive bucket: openaq-data-archive")


if __name__ == "__main__":
    main()
