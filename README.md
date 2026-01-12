# Toronto KSI Traffic Collisions Analysis

## Overview
This project analyzes traffic collisions in Toronto involving individuals who were killed or seriously injured (KSI). Using publicly available City of Toronto data, the analysis focuses on identifying spatial hotspots, temporal patterns, and the types of road users involved.

The goal of the project is to explore observable patterns in severe traffic collisions without making causal claims.

## Data
- Source: City of Toronto / Toronto Police open data
- Scope: Collisions involving killed or seriously injured persons
- Unit of analysis:
  - Person-level records (for road user and spatial analysis)
  - Aggregated views for temporal trends

## Methods
- Data cleaning and exploratory analysis using Python (pandas)
- Spatial aggregation to identify high-frequency KSI locations
- Time-based trend analysis by year
- Visualization and dashboarding in Power BI

## Key Findings
- Certain locations appear repeatedly in KSI collision records, forming identifiable spatial hotspots.
- KSI collision counts fluctuate year-to-year rather than following a single monotonic trend.
- Pedestrians and occupants of automobiles account for a large share of KSI records, reflecting exposure patterns.

## Limitations
- The dataset does not reliably include time-of-day information, so hourly analysis was excluded.
- Results are descriptive and do not imply causation or risk per trip.
- Location precision varies across records.

## Tools
- Python (pandas, matplotlib)
- SQL
- Power BI
