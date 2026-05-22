# IPL Crunch '26 Analytics Pipeline

This repository contains the data engineering and analytics pipeline built for the **IPL Crunch '26 Data Analytics Challenge**. 

Our primary goal is to uncover deep, counter-intuitive insights by analyzing official ball-by-ball IPL match data. The pipeline eliminates human bias, engineered custom metrics, and mathematically tests assumptions.

## Pipeline Overview

The codebase consists of an automated Python workflow:

1. **`01_parse_ipl_data.py`**:
   - Ingests over 1,200 nested Cricsheet JSON files.
   - Extracts metadata (toss decisions, venues, margins) and ball-by-ball data (runs, extras, wickets).
   - **Feature Engineering**: Calculates `match_phase` (Powerplay, Middle, Death) and a proprietary rolling **Dot Ball Pressure Index** that quantifies the exact sequence of consecutive dot balls faced by a batter.
   - Flattens the nested structures into a highly optimized 290,000+ row Pandas DataFrame, exported as a `.parquet` file.

2. **`02_generate_visuals.py`**:
   - Reads the optimized Parquet dataset.
   - Generates high-resolution, dark-themed charts using `matplotlib` and `seaborn`.
   - Visualizes critical components like Match Phase Run Differentials and Venue-Specific Toss Impact.

3. **`03_discover_insights.py`**:
   - Mathematically flags anomalies using standard statistical tests (`scipy.stats`).
   - Responsible for discovering the **Dubai Trap**: A statistical anomaly proving that teams choosing to field at the Dubai International Cricket Stadium severely handicap their win probability (40.7% vs the 53.8% global average).

4. **`04_generate_presentation.py`**:
   - Uses `fpdf2` to dynamically compile the insights and visual charts into a sleek PDF presentation.

## Setup & Usage

To run the pipeline locally:
```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn scipy fastparquet pyarrow fpdf2

# 1. Parse JSON files into Parquet (requires raw json folder)
python scripts/01_parse_ipl_data.py

# 2. Generate visuals
python scripts/02_generate_visuals.py

# 3. Discover statistical anomalies
python scripts/03_discover_insights.py

# 4. Export the final presentation PDF
python scripts/04_generate_presentation.py
```

*Note: Raw data files (`raw json/`) and massive compiled datasets (`*.parquet`) are intentionally ignored via `.gitignore` to keep this repository lightweight.*
