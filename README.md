# Toronto KSI Traffic Collisions Analysis

## Overview
This project analyzes traffic collisions in Toronto involving individuals who were killed or seriously injured (KSI). The analysis focuses on identifying spatial hotspots, long-term trends, and road users involved using publicly available City of Toronto data.

## Data
- Source: City of Toronto / Toronto Police open data
- Unit of analysis: person-level collision records
- Time range: varies by data availability

## Methods
- Data cleaning and exploratory analysis in Python (pandas)
- Spatial aggregation to identify high-frequency KSI locations
- Trend analysis by year
- Visualization and dashboarding in Power BI

## Key Findings
- Certain locations appear repeatedly in KSI collision records, forming identifiable spatial hotspots.
- KSI collision counts fluctuate over time rather than following a single monotonic trend.
- Pedestrians and occupants of automobiles account for a large share of KSI records.

## Limitations
- Time-of-day data was not reliable and was excluded.
- Results are descriptive and do not imply causation.
- Counts reflect records, not exposure or risk per trip.

## Dashboard
![Hotspots](visuals/hotspots.jpg)
![Trends](visuals/trends_road_users.jpg)
