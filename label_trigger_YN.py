import pandas as pd
from pathlib import Path

# -----------------------
# Load Weather Data
# -----------------------
# Input and output paths
input_path = Path("data\processed\combined_Mango_Pomo.csv")
output_path = Path("data/processed/payout_triggers_labeled.csv")

# Load weather data
df = pd.read_csv(input_path)

# -----------------------
# Define Crop-Specific Trigger Values
# Format: (crop_name, (month, fortnight)): {rain: (min, max), temp, humidity, wind}
# -----------------------
trigger_table = {
    # Pomegranate (fortnight-wise)
    ('Pomegranate', (6, 1)): {'rain': (50, 100), 'temp': (28, 34), 'humidity': (55, 75), 'wind': (0, 10)},
    ('Pomegranate', (6, 2)): {'rain': (50, 100), 'temp': (28, 34), 'humidity': (55, 75), 'wind': (0, 10)},
    ('Pomegranate', (7, 1)): {'rain': (60, 120), 'temp': (26, 32), 'humidity': (60, 80), 'wind': (0, 10)},
    ('Pomegranate', (7, 2)): {'rain': (60, 120), 'temp': (26, 32), 'humidity': (60, 80), 'wind': (0, 10)},
    ('Pomegranate', (8, 1)): {'rain': (70, 130), 'temp': (26, 31), 'humidity': (65, 85), 'wind': (0, 10)},
    ('Pomegranate', (8, 2)): {'rain': (70, 130), 'temp': (26, 31), 'humidity': (65, 85), 'wind': (0, 10)},
    ('Pomegranate', (9, 1)): {'rain': (50, 100), 'temp': (27, 33), 'humidity': (55, 75), 'wind': (0, 10)},
    ('Pomegranate', (9, 2)): {'rain': (50, 100), 'temp': (27, 33), 'humidity': (55, 75), 'wind': (0, 10)},
    ('Pomegranate', (10, 1)): {'rain': (30, 80), 'temp': (25, 30), 'humidity': (50, 70), 'wind': (0, 10)},
    ('Pomegranate', (10, 2)): {'rain': (30, 80), 'temp': (25, 30), 'humidity': (50, 70), 'wind': (0, 10)},
    ('Pomegranate', (11, 1)): {'rain': (20, 60), 'temp': (20, 28), 'humidity': (45, 65), 'wind': (0, 10)},
    ('Pomegranate', (11, 2)): {'rain': (20, 60), 'temp': (20, 28), 'humidity': (45, 65), 'wind': (0, 10)},

    # Mango (fortnight-wise)
    ('Mango', (10, 1)): {'rain': (20, 40), 'temp': (25, 33), 'humidity': (65, 80), 'wind': (0, 10)},
    ('Mango', (10, 2)): {'rain': (20, 40), 'temp': (25, 33), 'humidity': (65, 80), 'wind': (0, 10)},
    ('Mango', (11, 1)): {'rain': (10, 30), 'temp': (20, 30), 'humidity': (60, 75), 'wind': (0, 10)},
    ('Mango', (11, 2)): {'rain': (10, 30), 'temp': (20, 30), 'humidity': (60, 75), 'wind': (0, 10)},
    ('Mango', (12, 1)): {'rain': (0, 10), 'temp': (18, 28), 'humidity': (55, 70), 'wind': (0, 10)},
    ('Mango', (12, 2)): {'rain': (0, 10), 'temp': (18, 28), 'humidity': (55, 70), 'wind': (0, 10)},
    ('Mango', (1, 1)): {'rain': (0, 10), 'temp': (15, 25), 'humidity': (50, 70), 'wind': (0, 10)},
    ('Mango', (1, 2)): {'rain': (0, 10), 'temp': (15, 25), 'humidity': (50, 70), 'wind': (0, 10)},
    ('Mango', (2, 1)): {'rain': (0, 15), 'temp': (18, 30), 'humidity': (50, 65), 'wind': (0, 10)},
    ('Mango', (2, 2)): {'rain': (0, 15), 'temp': (18, 30), 'humidity': (50, 65), 'wind': (0, 10)},
    ('Mango', (3, 1)): {'rain': (5, 20), 'temp': (22, 32), 'humidity': (55, 70), 'wind': (0, 10)},
    ('Mango', (3, 2)): {'rain': (5, 20), 'temp': (22, 32), 'humidity': (55, 70), 'wind': (0, 10)},
    ('Mango', (4, 1)): {'rain': (20, 40), 'temp': (28, 35), 'humidity': (60, 75), 'wind': (0, 10)},
    ('Mango', (4, 2)): {'rain': (20, 40), 'temp': (28, 35), 'humidity': (60, 75), 'wind': (0, 10)},
}

# -----------------------
# Rainfall-Based Percentage Logic
# -----------------------
def get_percentage(actual_rain, rain_min, rain_max):
    expected = (rain_min + rain_max) / 2
    if expected == 0:
        return 0

    deviation = abs(actual_rain - expected) / expected

    if deviation < 0.10:
        return 0
    elif deviation < 0.25:
        return 0.25 
    elif deviation < 0.40:
        return 0.50 
    elif deviation < 0.60:
        return 0.75
    else:
        return 1.00 

# Labeling and Adding Payout Information
# -----------------------
def label_row(row):
    crop = row['CROP']
    month = row['MONTH']
    fortnight = row['FORTNIGHT']

    key = (crop, (month, fortnight))
    if key not in trigger_table:
        return pd.Series([None, None, None, None, None, None])  # Returning empty values if no match

    triggers = trigger_table[key]
    rain_min, rain_max = triggers['rain']
    temp_min, temp_max = triggers['temp']
    hum_min, hum_max = triggers['humidity']
    wind_min, wind_max = triggers['wind']

    temp_rise = max(0, row['MEAN_TEMP'] - temp_max) if row['MEAN_TEMP'] > temp_max else max(0, temp_min - row['MEAN_TEMP'])
    rain_dev = max(0, rain_min - row['RAINFALL']) if row['RAINFALL'] < rain_min else max(0, row['RAINFALL'] - rain_max)
    hum_dev = max(0, hum_min - row['HUMIDITY']) if row['HUMIDITY'] < hum_min else max(0, row['HUMIDITY'] - hum_max)
    wind_excess = max(0, row['WIND_SPEED'] - wind_max)

    triggered = 'YES' if temp_rise > 2 or rain_dev > 20 or hum_dev > 15 or wind_excess > 1 else 'NO'

    percentage = get_percentage(row['RAINFALL'], rain_min, rain_max)

    # Return calculated values
    return pd.Series([temp_rise, rain_dev, hum_dev, wind_excess, triggered, percentage])

# -----------------------
# Apply to DataFrame
# -----------------------
df[['TEMP_RISE', 'RAINFALL_DEV', 'HUMIDITY_DEV', 'WIND_EXCESS', 'TRIGGER', 'PERCENTAGE']] = df.apply(label_row, axis=1)

# -----------------------
# Save Final Output
# -----------------------
df.to_csv(output_path, index=False)
print(f"✅ Trigger labels and payouts saved to {output_path}")
