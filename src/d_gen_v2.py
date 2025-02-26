import csv
import datetime
import random
import os
import uuid

# File paths
DATASET_FILE = "datasets.csv"
OWNER_FILE = "owners.csv"
ID_FILE = "generated_ids.txt"

# Load existing IDs to prevent duplicates
def load_existing_ids():
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_new_id(new_id):
    with open(ID_FILE, "a") as f:
        f.write(new_id + "\n")

def generate_id():
    """Generate a unique ID and store it persistently."""
    existing_ids = load_existing_ids()
    while True:
        new_id = str(uuid.uuid4())[:16]  # Shorten UUID for readability
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            save_new_id(new_id)
            return new_id

# Load existing owners from file
def load_existing_owners():
    owners = []
    if os.path.exists(OWNER_FILE):
        with open(OWNER_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            owners = [row for row in reader]
    return owners

# Save new owners to file
def save_owner(name, company, row_number):
    with open(OWNER_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, company, row_number])

def create_owners(num_owners=10):
    """Create initial owners and save to file."""
    owners = [[f"Owner_{i}", f"Company_{i}", i] for i in range(num_owners)]
    with open(OWNER_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "company", "row_number"])
        writer.writerows(owners)
    return owners

def assign_owner(owners):
    """Assign a dataset to an existing or new owner."""
    if not owners or random.random() < 0.2:  # 20% chance to create a new owner
        new_owner_id = len(owners)
        name = f"Owner_{new_owner_id}"
        company = f"Company_{new_owner_id}"
        owners.append([name, company, new_owner_id])
        save_owner(name, company, new_owner_id)
        return name, company, new_owner_id
    else:
        return random.choice(owners)

def create_datasets(num_datasets=50):
    """Generate dataset entries with assigned owners."""
    owners = load_existing_owners()
    datasets = []
    today = datetime.datetime.now()
    
    for _ in range(num_datasets):
        dataset_id = generate_id()
        owner_name, company, owner_index = assign_owner(owners)
        role = random.choice(["admin", "editor", "audience"])
        fake_email = f"user{owner_index}@example.com"
        delta = datetime.timedelta(days=random.randint(0, 365))
        creation_date = (today - delta).strftime("%Y-%m-%d")
        num_rows = random.randint(100, 10000)
        num_cols = random.randint(1, 200)
        size_bytes = random.randint(1*1024*1024, 5*1024*1024*1024)
        
        datasets.append({
            "id": dataset_id,
            "owner": owner_name,
            "company": company,
            "role": role,
            "fake_email": fake_email,
            "creation_date": creation_date,
            "num_rows": num_rows,
            "num_cols": num_cols,
            "size_bytes": size_bytes
        })
    
    return datasets

# Save data to CSV
def save_to_csv(data, csv_path, fieldnames):
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def main():
    if not os.path.exists(OWNER_FILE):
        create_owners(10)
    datasets = create_datasets(50)
    datasets_fieldnames = ["id", "owner", "company", "role", "fake_email", "creation_date", "num_rows", "num_cols", "size_bytes"]
    save_to_csv(datasets, DATASET_FILE, datasets_fieldnames)
    print("Datasets and owners have been successfully created and saved.")

if __name__ == "__main__":
    main()
