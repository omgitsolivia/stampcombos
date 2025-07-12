# Postage Stamp Calculator

A Streamlit web application that calculates optimal stamp combinations to reach a target postage amount.

## Overview

This calculator helps users find all possible combinations of available stamps that:
- Meet or exceed a target postage amount (in dollars)
- Do not exceed a specified maximum price limit
- Use no more than a specified number of stamps

The app displays results sorted by total cost and provides recommendations for minimum overpayment and fewest stamps used.

## Features

- Input stamp denominations in cents
- Set target postage amount in dollars
- Define maximum price limit (not to be exceeded)
- Limit maximum number of stamps per combination
- View all valid combinations in a sortable table
- Summary statistics and recommended options
- Responsive UI with helpful tooltips

## Requirements

- Python 3.7+
- Streamlit

## Installation & Setup

1. **Clone/Download** this repository
2. **Install dependencies:**
   ```bash
   pip install streamlit
   ```

## Running the Application

### Local Development
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Production Deployment
The app can be deployed to any Streamlit-compatible hosting service:
- Streamlit Cloud
- Heroku
- AWS/GCP/Azure

## Usage Example

1. Enter available stamp denominations: `78, 44, 37, 29, 25, 20`
2. Set target postage: `$1.70`
3. Set maximum price: `$1.74`
4. Set maximum stamps: `5`
5. Click "Calculate Stamp Combinations"