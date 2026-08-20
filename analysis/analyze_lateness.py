import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon
import seaborn as sns
import os

# Load data
df = pd.read_csv('data/raw/data.csv', quotechar='"', on_bad_lines='skip')
print("Data loaded. Total appointments observed:", len(df))

# Filter attended events
attended = df[df['status'] == 'attended'].copy()
attended['delay_min'] = pd.to_numeric(attended['delay_min'], errors='coerce')

print("\n=== A. Core Statistics ===")
mean_lateness = attended['delay_min'].mean()
print(f"Mean lateness: {mean_lateness:.2f} minutes")

median_lateness = attended['delay_min'].median()
print(f"Median lateness: {median_lateness:.2f} minutes")

std_lateness = attended['delay_min'].std()
print(f"Standard deviation: {std_lateness:.2f} minutes")

# Strict punctuality (≤ 0 min)
punctual = attended[attended['delay_min'] <= 0]
punctuality_rate = len(punctual) / len(attended) * 100 if len(attended) > 0 else 0
print(f"Punctuality rate (on time or early, delay <= 0 min): {punctuality_rate:.1f}%")

no_shows = df[df['status'] == 'absent']
no_show_prob = len(no_shows) / len(df) * 100
print(f"No-show probability: {no_show_prob:.1f}%")

print(f"\nTotal attended: {len(attended)}")
print(f"Total no-shows: {len(no_shows)}")
print(f"Earliest recorded arrival: {attended['delay_min'].min():.1f} min (the 2026-05-06 anomaly!)")
print(f"Maximum observed delay: {attended['delay_min'].max():.1f} min")

print("\n=== B. Probability Distribution ===")

# 1. Combined Histogram + Gaussian + KDE (best version)
plt.figure(figsize=(11, 7))
sns.histplot(
    attended['delay_min'],
    bins=np.arange(-6, 48, 3),
    kde=True,
    color='royalblue',
    alpha=0.7,
    stat='density',
)
# sns.histplot(attended['delay_min'], kde=True, bins=15, color='royalblue', alpha=0.7, stat="density")
x = np.linspace(attended['delay_min'].min()-5, attended['delay_min'].max()+5, 200)
mu, std = norm.fit(attended['delay_min'])
plt.plot(x, norm.pdf(x, mu, std), 'r-', lw=2.5, label=f'Gaussian Fit (μ={mu:.1f}, σ={std:.1f})')
plt.title("Histogram of Lateness Delays\n(The Motivational Wavefunction in Action)")
plt.xlabel("Delay (minutes)")
plt.ylabel("Density")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('plots/delay_histogram.png', dpi=300, bbox_inches='tight')
print("→ Histogram + Gaussian saved as plots/delay_histogram.png")

# 2. Exponential Tail
positive_delays = attended[attended['delay_min'] > 0]['delay_min']
if len(positive_delays) > 0:
    loc, scale = expon.fit(positive_delays)
    print(f"Exponential tail fit (positive delays): scale = {scale:.2f}")
    
    plt.figure(figsize=(10, 6))
    sns.histplot(positive_delays, kde=False, bins=10, stat="density", color='orange', alpha=0.7)
    x_exp = np.linspace(0, positive_delays.max()+5, 100)
    plt.plot(x_exp, expon.pdf(x_exp, loc, scale), 'g-', lw=2, label=f'Exponential Fit (scale={scale:.1f})')
    plt.title("Exponential Tail for Positive Lateness\n(The Heavy Tail of Procrastination)")
    plt.xlabel("Delay (minutes)")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('plots/exponential_tail.png', dpi=300, bbox_inches='tight')
    print("→ Exponential tail saved as plots/exponential_tail.png")

# 3. Boxplot by Event Type
plt.figure(figsize=(10, 6))
sns.boxplot(x='event_type', y='delay_min', data=attended, palette="Set3")
plt.title("Lateness Distribution by Event Type\n(Lectures vs BBQs: A Tale of Two Wavefunctions)")
plt.ylabel("Delay (minutes)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.savefig('plots/boxplot_by_event.png', dpi=300, bbox_inches='tight')
print("→ Boxplot by event type saved as plots/boxplot_by_event.png")

# 4. Weather Scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(data=attended, x='temperature_c', y='delay_min', hue='weather', s=80, alpha=0.8)
plt.title("Temperature vs Delay\n(Does Rain Collapse the Wavefunction?)")
plt.xlabel("Temperature (°C)")
plt.ylabel("Delay (minutes)")
plt.grid(True, alpha=0.3)
plt.savefig('plots/weather_scatter.png', dpi=300, bbox_inches='tight')
print("→ Weather scatter saved as plots/weather_scatter.png")

print("\n=== Additional Statistical Insights ===")
print("Event-type dependence:")
print(attended.groupby('event_type')['delay_min'].agg(['mean', 'median', 'std', 'count']).round(2))

print("\n=== Weather Correlation (preliminary) ===")
print(attended.groupby('weather')['delay_min'].agg(['mean', 'median', 'count']).round(2))

# Save cleaned data
attended.to_csv('data/processed/data.csv', index=False)
print(f"\n✅ Cleaned data saved to data/processed/data.csv")
print("Analysis complete. All plots generated in plots/ folder.")