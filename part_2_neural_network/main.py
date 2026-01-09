import numpy as np
import pandas as pd 
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# 1. Load data
df = pd.read_csv('housing.csv')

# 2. Fix the column names (removes the leading spaces you saw in the list)
df.columns = df.columns.str.strip()

# 3. Create the plot
plt.figure(figsize=(10, 6))
plt.hist(df['MEDV'], bins=35, alpha=0.45, color='red', edgecolor='black')
plt.title('Distribution of House Prices (MEDV)')
plt.xlabel('Price ($1000s)')
plt.ylabel('Frequency')

# 4. Save instead of show
plt.savefig('medv_histogram.png')
print("Plot successfully saved as 'medv_histogram.png'")