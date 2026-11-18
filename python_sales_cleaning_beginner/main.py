import csv
import json
from pathlib import Path


def normalize_row(row):
    # Clean text fields in a copy of the row.
    cleaned_row = row.copy()
    cleaned_row['order_id'] = cleaned_row['order_id'].strip()
    cleaned_row['customer'] = cleaned_row['customer'].strip().title()
    cleaned_row['product'] = cleaned_row['product'].strip().title()
    cleaned_row['city'] = cleaned_row['city'].strip().title()
    return cleaned_row


def clean_sales(rows):
    # Validate numbers and count rejected rows.
    cleaned_rows = []
    rejected = {
        'missing': 0,
        'invalid_type': 0,
        'invalid_value': 0
    }

    for row in rows:
        cleaned_row = normalize_row(row)

        if cleaned_row['price'].strip() == '' or cleaned_row['quantity'].strip() == '':
            rejected['missing'] += 1
            continue

        try:
            price = float(cleaned_row['price'])
            quantity = int(cleaned_row['quantity'])
        except (ValueError, TypeError):
            rejected['invalid_type'] += 1
            continue

        if price <= 0 or quantity <= 0:
            rejected['invalid_value'] += 1
            continue

        cleaned_row['price'] = price
        cleaned_row['quantity'] = quantity
        cleaned_rows.append(cleaned_row)

    return cleaned_rows, rejected


def remove_duplicates(rows):
    # Keep the first row with each unique six-field key.
    unique_rows = []
    seen = set()
    duplicates_count = 0

    for row in rows:
        key = (
            row['order_id'],
            row['customer'],
            row['product'],
            row['price'],
            row['quantity'],
            row['city']
        )

        if key in seen:
            duplicates_count += 1
            continue

        seen.add(key)
        unique_rows.append(row)

    return unique_rows, duplicates_count


if __name__ == '__main__':
    # Read the original CSV file.
    input_file = Path('data') / 'sales_dirty.csv'
    with open(input_file, 'r', encoding='utf-8', newline='') as file:
        rows = list(csv.DictReader(file))

    # Clean rows and remove duplicates.
    cleaned_rows, rejected = clean_sales(rows)
    unique_rows, duplicates_count = remove_duplicates(cleaned_rows)

    # Create the output folder.
    output_folder = Path('output')
    output_folder.mkdir(parents=True, exist_ok=True)

    # Save cleaned data to CSV.
    fieldnames = ['order_id', 'customer', 'product', 'price', 'quantity', 'city']
    with open(output_folder / 'cleaned_sales.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows)

    # Create the data quality report.
    report = {
        'total_rows': len(rows),
        'cleaned_rows': len(unique_rows),
        'rejected': {
            'missing': rejected['missing'],
            'invalid_type': rejected['invalid_type'],
            'invalid_value': rejected['invalid_value'],
            'duplicates': duplicates_count
        }
    }

    # Save the report to JSON.
    with open(output_folder / 'cleaning_report.json', 'w', encoding='utf-8') as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print(report)
