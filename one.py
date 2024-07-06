import netCDF4 as nc
import pandas as pd

# Specify the path to the NetCDF file
netcdf_file_path = 'adaptor.mars.internal-1718528288.9433048-12824-8-9bdef7c5-a6f3-4d5e-a460-3dbfa7374948.nc'
# Output CSV file path
csv_file_path = 'output_4.csv'

# Open the NetCDF file
dataset = nc.Dataset(netcdf_file_path)

# Display the variables and their dimensions
print("Variables and their dimensions:")
for var_name in dataset.variables.keys():
    var = dataset.variables[var_name]
    print(f"{var_name}: {var.dimensions}, shape: {var.shape}")

# Prepare data for DataFrame
data_dict = {}

# Handle variables with different dimensions
for var_name in dataset.variables.keys():
    var_data = dataset.variables[var_name][:]
    # Flatten the variable data
    flattened_data = var_data.flatten()
    data_dict[var_name] = flattened_data

# Find the maximum length of the flattened data arrays
max_length = max(len(data) for data in data_dict.values())

# Ensure all arrays are of the same length by padding with NaNs
for var_name, data in data_dict.items():
    if len(data) < max_length:
        data_dict[var_name] = pd.Series(data).reindex(range(max_length), fill_value=float('nan'))

# Convert to pandas DataFrame
df = pd.DataFrame(data_dict)

# Write to CSV file
df.to_csv(csv_file_path, index=False)

print(f"NetCDF file has been converted to CSV and saved at {csv_file_path}")
