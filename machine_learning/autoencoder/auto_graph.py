import pandas as pd
import matplotlib.pyplot as plt

csv_file = "reconstruction_errors.csv"
df = pd.read_csv(csv_file)

print(df.columns)

if 'reconstruction_error' not in df.columns:
    raise ValueError("The CSV file must contain a column named 'reconstruction_error'.")

errors = df['reconstruction_error']

threshold = errors.quantile(0.95)
print(f"Anomaly Threshold (95th Percentile): {threshold:.4f}")

plt.figure(figsize=(10, 6))
plt.hist(errors, bins=50, alpha=0.7, color='blue', edgecolor='black', label='Reconstruction Errors')

plt.axvline(x=threshold, color='red', linestyle='--', label=f'Threshold ({threshold:.4f})')

plt.xlim(0, 2)

plt.title('Reconstruction Error Histogram')
plt.xlabel('Reconstruction Error')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)

plt.show()
