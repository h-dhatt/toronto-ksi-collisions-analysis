import json
from pathlib import Path

import numpy as np
import pandas as pd


RAW_PATH = Path("data/raw/ksi_collisions.csv")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_lon_lat(geom_str: str):
    """Extract a centroid lon/lat from a GeoJSON-like polygon stored as a string."""
    if pd.isna(geom_str):
        return (np.nan, np.nan)
    try:
        geom = json.loads(geom_str)
        coords = geom.get("coordinates")
        if not coords:
            return (np.nan, np.nan)

        # Typical structure: coordinates[0] is the outer ring of a polygon
        ring = coords[0]
        arr = np.array(ring, dtype=float)

        lon = float(np.nanmean(arr[:, 0]))
        lat = float(np.nanmean(arr[:, 1]))
        return (lon, lat)
    except Exception:
        return (np.nan, np.nan)


def main():
    df = pd.read_csv(RAW_PATH)

    # 1) simple column cleanup
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # 2) date + time parsing
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    time_num = pd.to_numeric(df["time"], errors="coerce")
    df["time_str"] = time_num.fillna(-1).astype(int).astype(str).str.zfill(4)
    df.loc[time_num.isna(), "time_str"] = pd.NA

    df["hour"] = pd.to_numeric(df["time_str"].str.slice(0, 2), errors="coerce")
    df["minute"] = pd.to_numeric(df["time_str"].str.slice(2, 4), errors="coerce")

    # A single datetime column is handy for trends later
    hhmm = df["time_str"].fillna("0000").str.replace(r"(\d{2})(\d{2})", r"\1:\2", regex=True)
    df["datetime"] = pd.to_datetime(df["date"].dt.strftime("%Y-%m-%d") + " " + hhmm, errors="coerce")

    # 3) coordinates from geometry
    lon_lat = df["geometry"].apply(extract_lon_lat) if "geometry" in df.columns else None
    if lon_lat is not None:
        df["lon"] = lon_lat.apply(lambda t: t[0])
        df["lat"] = lon_lat.apply(lambda t: t[1])
    else:
        df["lon"] = np.nan
        df["lat"] = np.nan

    # basic sanity bounds for Toronto-ish coords
    df.loc[(df["lat"] < 43.0) | (df["lat"] > 44.2), ["lat", "lon"]] = np.nan
    df.loc[(df["lon"] > -78.5) | (df["lon"] < -80.5), ["lat", "lon"]] = np.nan

    # 4) trim text columns (Power BI friendliness)
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string").str.strip()

    # Save person-level (one row per record/person)
    person_path = OUT_DIR / "ksi_person_level_clean.csv"
    df.to_csv(person_path, index=False)

    # 5) collision-level: group to 1 row per collision (good for maps + hotspots)
    group_cols = [
        "accnum", "date", "time", "street1", "street2",
        "district", "division", "hood_158", "neighbourhood_158",
        "lat", "lon"
    ]
    group_cols = [c for c in group_cols if c in df.columns]  # keep only what exists

    collision_level = (
        df.groupby(group_cols, dropna=False)
          .agg(rows=("accnum", "size"))
          .reset_index()
    )

    collision_path = OUT_DIR / "ksi_collision_level_clean.csv"
    collision_level.to_csv(collision_path, index=False)

    print("✅ Saved:")
    print(" -", person_path)
    print(" -", collision_path)
    print("\nPerson-level rows:", len(df))
    print("Collision-level rows:", len(collision_level))


if __name__ == "__main__":
    main()
