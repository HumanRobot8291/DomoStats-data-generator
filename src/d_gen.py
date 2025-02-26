import csv
import datetime
import random

import random
import os

ID_FILE = "generated_ids.txt"

def load_existing_ids():
    """Load previously generated IDs from a file to avoid duplication."""
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_new_id(new_id):
    """Save a new ID to the file to track it for future runs."""
    with open(ID_FILE, "a") as f:
        f.write(new_id + "\n")

def generate_id():
    """Generate a unique 16-character ID and store it persistently."""
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    existing_ids = load_existing_ids()

    while True:
        new_id = ''.join(random.choice(chars) for _ in range(16))
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            save_new_id(new_id)
            return new_id

# Generate fake dataset entries
def create_datasets(num_datasets=50):# S add more datasets
    datasets = []
    today = datetime.datetime.now()
    
    for i in range(num_datasets):
        dataset_id = generate_id()
        owner_name = f"Owner_{i}"
        role = random.choice(["admin", "editor", "audience"])
        fake_email = f"user{i}@example.com"
        delta = datetime.timedelta(days=random.randint(0, 365))
        creation_date = (today - delta).strftime("%Y-%m-%d")
        num_rows = random.randint(100, 10000)
        num_cols = random.randint(1, 200)
        size_bytes = random.randint(1*1024*1024, 5*1024*1024*1024)  # 1MB to 5GB
        
        datasets.append({
            "id": dataset_id,
            "owner": owner_name,
            "role": role,
            "fake_email": fake_email,
            "creation_date": creation_date,
            "num_rows": num_rows,
            "num_cols": num_cols,
            "size_bytes": size_bytes
        })
    
    return datasets

# Generate fake ETL entries
def create_etls(datasets, num_etls=20):
    etl_entries = []
    
    for i in range(num_etls):
        etl_id = generate_id()
        input_datasets = random.sample(datasets, k=random.randint(1, 5))
        output_datasets = random.sample(datasets, k=random.randint(1, 5))
        
        etl_entries.append({
            "id": etl_id,
            "input": [d["id"] for d in input_datasets],
            "output": [d["id"] for d in output_datasets]
        })
    
    return etl_entries

# Generate fake owners
def create_owners(num_owners=10):
    owners = []
    
    for i in range(num_owners):
        name = f"Owner_{i}"
        company = f"Company_{i}"
        owners.append({
            "name": name,
            "company": company
        })
    
    return owners

# Save data to CSV
def save_to_csv(data, csv_path, fieldnames):
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

# Main execution
def main():
    # Generate data
    datasets = create_datasets(50)
    etl_entries = create_etls(datasets, 20)
    owners = create_owners(10)

    # Save datasets to CSV
    datasets_fieldnames = ["id", "owner", "role", "fake_email", "creation_date", "num_rows", "num_cols", "size_bytes"]
    save_to_csv(datasets, "datasets.csv", datasets_fieldnames)
    
    # Save ETL entries to CSV
    etls_fieldnames = ["id", "input", "output"]
    # Convert list fields to strings for CSV compatibility
    for etl in etl_entries:
        etl["input"] = ','.join(etl["input"])
        etl["output"] = ','.join(etl["output"])
    save_to_csv(etl_entries, "etl_entries.csv", etls_fieldnames)
    
    # Save owners to CSV
    owners_fieldnames = ["name", "company"]
    save_to_csv(owners, "owners.csv", owners_fieldnames)

if __name__ == "__main__":
    main()
