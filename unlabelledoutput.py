import pandas as pd
from fixedapp import calculate_payout

# Define the combinations
districts = ["Jalgaon", "Jalna", "Kolhapur", "Latur", "Nanded", "Nandurbar", "Nashik", "Osmanabad", "Palghar", "Parbhani", "Pune", "Raigarh", "Ratnagiri", "Sangli", "Satara", "Sindhudurg", "Solapur", "Thane", "Washim"]
crops = ['Pomegranate', 'Mango']
seasons = ['Kharif', 'Rabi']
years = range(2015, 2018)
area = 1.0  # or any fixed area you want to test with

results = []

for district in districts:
    for crop in crops:
        for season in seasons:
            for year in years:
                try:
                    result = calculate_payout(district, season, year, crop, area)
                    # No filtering based on the average percent now
                    results.append({
                        'district': district,
                        'crop': crop,
                        'season': season,
                        'year': year,
                        'avg_percent': result['avg_percent'],
                        'payout': result['payout']
                    })
                except Exception as e:
                    print(f"Error for {district}, {crop}, {season}, {year}: {e}")

# Convert to DataFrame and save
df = pd.DataFrame(results)
df.to_csv("payoutsunlabelled.csv", index=False)
print("✅ Analysis complete. Results saved to payoutsunlabelled.csv")
