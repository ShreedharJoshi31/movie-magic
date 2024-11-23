import random
import uuid
from enum import Enum

# Enum for Mumbai suburbs
class MumbaiSuburbs(Enum):
    ANDHERI = "Andheri"
    BANDRA = "Bandra"
    BORIVALI = "Borivali"
    DADAR = "Dadar"
    GOREGAON = "Goregaon"
    JUHU = "Juhu"
    KANDIVALI = "Kandivali"
    MALAD = "Malad"
    MULUND = "Mulund"
    POWAI = "Powai"
    SANTACRUZ = "Santacruz"
    THANE = "Thane"
    VERSOVA = "Versova"
    VILE_PARLE = "Vile Parle"
    WADALA = "Wadala"

# List of random words for theater name generation
theater_name_prefixes = [
    "Regal", "Grand", "Cineplex", "Majestic", "Galaxy", "Star", "Silver", "Golden", "Phoenix", "Infinity"
]
theater_name_suffixes = [
    "Theater", "Multiplex", "Cineworld", "Cinemas", "Screen", "Studio", "Arena", "Palace", "Hall", "House"
]

# Function to generate a random theater name
def generate_theater_name():
    prefix = random.choice(theater_name_prefixes)
    suffix = random.choice(theater_name_suffixes)
    return f"{prefix} {suffix}"

# Function to generate theater data
def generate_theaters(num_theaters=100):
    theaters = []
    for _ in range(num_theaters):
        theater_id = str(uuid.uuid4())  # Generate a unique UUID
        theater_name = generate_theater_name()
        theater_location = random.choice(list(MumbaiSuburbs)).value  # Randomly select a Mumbai suburb
        theaters.append({
            "theater_id": theater_id,
            "theater_name": theater_name,
            "theater_location": theater_location
        })
    return theaters

# Generate 100 theaters and print them
theaters_data = generate_theaters()

# Save to a JSON file (optional)
import json
with open("theaters.json", "w") as file:
    json.dump(theaters_data, file, indent=4)

# Print some sample data
print("Sample Theaters Data:")
for theater in theaters_data[:10]:  # Print first 10 theaters as a sample
    print(theater)