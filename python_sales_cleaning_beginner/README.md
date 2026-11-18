# Sales Data Cleaning with Python

A beginner-level Python project that cleans a small **synthetic sales dataset**. It uses only Python's standard library and concepts from my Python Intermediate coursework.

## What this project does

1. Reads `data/sales_dirty.csv` with `csv.DictReader`.
2. Removes extra spaces and normalizes names, products, and cities.
3. Converts prices and quantities to numbers.
4. Skips rows with missing values, invalid numbers, or non-positive values.
5. Removes exact duplicates using a tuple and a set.
6. Saves `output/cleaned_sales.csv` and a JSON data-quality report.

A duplicate is a row where **all six fields** match after cleaning. The first matching row is kept. Each rejected row is counted once.

## Results

| Metric | Rows |
| --- | ---: |
| Original rows | 10 |
| Clean unique rows | 5 |
| Missing price or quantity | 1 |
| Invalid number | 1 |
| Non-positive price or quantity | 2 |
| Duplicate rows | 1 |

These results come from a synthetic learning dataset, not a production dataset.

## Project files

```text
python_sales_cleaning_beginner/
├── main.py
├── README.md
├── data/
│   └── sales_dirty.csv
└── output/
    ├── cleaned_sales.csv
    └── cleaning_report.json
```

## How to run

1. Install Python 3.
2. Open a terminal in this project folder.
3. Run:

```bash
python3 main.py
```

The program creates the `output` folder when needed. Run it **from the project folder** because the input path is relative to the current working directory.

## Python skills used

Functions, lists, dictionaries, loops, conditionals, `.copy()`, `.strip()`, `.title()`, `try/except`, `continue`, tuples, sets, `csv`, `json`, and `pathlib`.

## What I learned

How to clean text and numeric fields, keep the original input unchanged, identify repeated records, and export clean results with simple Python code.

## Limitations

This is a practice project using a fixed CSV structure. It does not yet handle every possible edge case (such as `NaN`, infinity, malformed headers, or complex name formatting). Future improvements can use Pandas and more advanced validation.
