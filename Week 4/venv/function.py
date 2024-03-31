# import and install libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from pandas.core.reshape.tile import to_datetime
import pickle
from pickle import dump, load
import sys

# Reading data into DataFrame
cab_data = pd.read_csv(r'C:\Users\HP\Desktop\dataGlaciers_week2\Flask\venv\Cab_Data.csv')
city = pd.read_csv(r'C:\Users\HP\Desktop\dataGlaciers_week2\Flask\venv\City.csv')
transaction = pd.read_csv(r'C:\Users\HP\Desktop\dataGlaciers_week2\Flask\venv\Transaction_ID.csv')
holidays = pd.read_csv(r'C:\Users\HP\Desktop\dataGlaciers_week2\Flask\venv\holidays.csv')
customer_id = pd.read_csv(r'C:\Users\HP\Desktop\dataGlaciers_week2\Flask\venv\Customer_ID.csv')

# Set the display option to show two decimal places for floating-point numbers
pd.set_option('display.float_format', '{:.2f}'.format)

# Merge the DataFrames using pandas
df = pd.merge(cab_data, transaction, on= 'Transaction ID')
df = pd.merge(df, customer_id, on='Customer ID')
# Convert Date of Trave to datetime format
df['Date of Travel'] = pd.to_datetime(df['Date of Travel'])

holidays['date'] = pd.to_datetime(holidays['date'])

# Merge DataFrames based on 'Date' column
df = pd.merge(df, holidays, left_on='Date of Travel', right_on='date', how='left')

# Create 'Is Holiday' column and mark 'Yes' where there is a match
df['Is Holiday'] = df['date'].apply(lambda x: 'Yes' if pd.notnull(x) else 'No')

# Drop unnecessary columns
df = df.drop(['date', 'holiday'], axis=1)

# Convert Transaction ID column to string format
df['Transaction ID'] = df['Transaction ID'].astype(str)

# Convert Year column to string format
df['Year'] = df['Year'].astype(str)

# Convert Customer IDcolumn to string format
df['Customer ID'] = df['Customer ID'].astype(str)

# Define age group bins and labels
bins = [25, 35, 45, 55, 65, 75, 85]
labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']

# Create a new column 'Age group'
df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, include_lowest=True)

# Define Income Range bins and labels
bins = [5000, 10000, 20000, 30000, 40000, 50000]
labels = ['2-5k', '6-10k', '11-20k', '21-30k', '31-40k']

# Create a new column 'Income Range'
df['Income Range'] = pd.cut(df['Income (USD/Month)'], bins=bins, labels=labels, include_lowest=True)


# Profit made on each trip
df['Profit'] = df['Price Charged']-df['Cost of Trip']

# Extract Month
df['Month'] = df['Date of Travel'].dt.month_name()

# Extract Day
df['Day'] = df['Date of Travel'].dt.day

# Extract Day of the Week
df['Day_of_Week'] = df['Date of Travel'].dt.day_name()

# Convert Day column to string format
df['Day'] = df['Day'].astype(str)

df = df.sort_values('Date of Travel', ascending=True)

# Calculate profit per kilometer
df['Profit per KM'] = df['Profit'] / df['KM Travelled']

#Filtering out less importantant columns
df = df[[
        'Transaction ID', 'Date of Travel', 'Company','City','Customer ID', 'Payment_Mode',
         'Gender', 'Age Group', 'Income Range', 'Is Holiday', 'MonthYear', 'Year',
         'Month','Day', 'Day_of_Week','KM Travelled', 'Price Charged',
         'Cost of Trip', 'Profit', 'Profit per KM'
         ]]

# Calculate the average cost of trip per kilometer
pink_cost_per_KM = (df[df['Company'] == 'Pink Cab']['Cost of Trip'] / df[df['Company'] == 'Pink Cab']['KM Travelled']).mean()
yellow_cost_per_KM = (df[df['Company'] == 'Yellow Cab']['Cost of Trip'] / df[df['Company'] == 'Yellow Cab']['KM Travelled']).mean()

# Calculate the price charged per kilometer
pink_price_per_KM = (df[df['Company'] == 'Pink Cab']['Price Charged'] / df[df['Company'] == 'Pink Cab']['KM Travelled']).mean()
yellow_price_per_KM = (df[df['Company'] == 'Yellow Cab']['Price Charged'] / df[df['Company'] == 'Yellow Cab']['KM Travelled']).mean()



# Calculate the average profit per kilometer
pink_cab_average = df[df['Company'] == 'Pink Cab']['Profit per KM'].mean()
yellow_cab_average = df[df['Company'] == 'Yellow Cab']['Profit per KM'].mean()
overall_profit_average = df['Profit per KM'].mean()

# Calculate total distance travelled
pink_total_km = df[df['Company']=='Pink Cab']['KM Travelled'].sum()
yellow_total_km = df[df['Company']=='Yellow Cab']['KM Travelled'].sum()
total_km = df['KM Travelled'].sum()

# Calculate average KM travelled
pink_average_km = df[df['Company']=='Pink Cab']['KM Travelled'].mean()
yellow_average_km = df[df['Company']=='Yellow Cab']['KM Travelled'].mean()
overall_km_average = df['KM Travelled'].mean()

"""# Data Preprocessing"""

# Number of transactions by Pink Cab and Yellow Cab
num_pink_tran = len(df[df['Company'] == 'Pink Cab'])
num_yellow_tran = len(df[df['Company'] == 'Yellow Cab'])
total_tran = len(df['Transaction ID'])

# Number of Holidays
pink_hols = len(df[(df['Is Holiday']=='Yes') & (df['Company']== 'Pink Cab')])
yellow_hols = len(df[(df['Is Holiday']=='Yes') & (df['Company']== 'Yellow Cab')])
hols_tran = len((df['Is Holiday']=='Yes'))

# Number of customers
pink_customers = df[df['Company']=='Pink Cab']['Customer ID'].nunique()
yellow_customers = df[df['Company']=='Yellow Cab']['Customer ID'].nunique()
total_customers = df['Customer ID'].nunique()



# Create a list to store data for each row
data = []

# Append data for 'Number of Transactions'
data.append({
    'Name': 'Number of Transactions',
    'Pink Cab': num_pink_tran,
    'Yellow Cab': num_yellow_tran,
    'Total': total_tran
})

# Append data for 'Transactions on Holidays'
data.append({
    'Name': 'Transactions on Holidays',
    'Pink Cab': pink_hols,
    'Yellow Cab': yellow_hols,
    'Total': hols_tran
})

# Append data for 'Number of Customers'
data.append({
    'Name': 'Number of Customers',
    'Pink Cab': pink_customers,
    'Yellow Cab': yellow_customers,
    'Total': total_customers
})

# Append data for 'Cost per kilometer'
data.append({
    'Name': 'Cost per KM',
    'Pink Cab': pink_cost_per_KM,
    'Yellow Cab': yellow_cost_per_KM
})

# Append data for 'price per kilometer'
data.append({
    'Name': 'Price Charged per KM',
    'Pink Cab': pink_price_per_KM,
    'Yellow Cab': yellow_price_per_KM
})

# Append data for 'Average Profit per KM'
data.append({
    'Name': 'Average Profit per KM',
    'Pink Cab': pink_cab_average,
    'Yellow Cab': yellow_cab_average,
    'Total': overall_profit_average
})

# Append data for total distance
data.append({
    'Name': 'Total Distance (KM)',
    'Pink Cab': pink_total_km,
    'Yellow Cab': yellow_total_km,
    'Total': total_km
})

# Append data for 'Average KM'
data.append({
    'Name': 'Average Distance (KM)',
    'Pink Cab': pink_average_km,
    'Yellow Cab': yellow_average_km,
    'Total': overall_km_average
})

# Create DataFrame from the list of dictionaries
transactions_customers = pd.DataFrame(data)

# Display the updated DataFrame
# print(transactions_customers)


# Define the function
# Define the function
def calculate_price_and_profit(distance, company):
    price_per_km = None
    cost_per_km = None

    if company == 'Pink Cab':
        price_per_km = pink_price_per_KM
        cost_per_km = pink_cost_per_KM
    elif company == 'Yellow Cab':
        price_per_km = yellow_price_per_KM
        cost_per_km = yellow_cost_per_KM

    if price_per_km is None or cost_per_km is None:
        # Handle the case where price_per_km or cost_per_km is not available
        print(f"Price or cost information not available for company '{company}'.")
        return None, None

    revenue = round(distance * price_per_km, 2)
    cost_of_trip = round(distance * cost_per_km, 2)
    profit = round(revenue - cost_of_trip, 2)

    return revenue, profit


# Define a function for the interactive part
def ask_user():
    while True:
        # Prompt user for input and capitalize each word in company
        distance_input = input("Enter the distance of the trip in kilometers: ")
        try:
            distance = round(float(distance_input), 2)
        except ValueError:
            print("Invalid distance format. Please enter a valid number.")
            continue

        while True:
            company_input = input("Enter the company ('P' for Pink Cab or 'Y' for Yellow Cab): ").lower()

            # Check if the input company is valid
            if company_input == 'p':
                company = 'Pink Cab'
                break
            elif company_input == 'y':
                company = 'Yellow Cab'
                break
            else:
                print("Invalid company input. Please enter 'P' for Pink Cab or 'Y' for Yellow Cab.")

        # Calculate and display the trip price and profit with 2 decimal places
        revenue, profit = calculate_price_and_profit(distance, company)
        print(f"The price of the trip with {company} for a distance of {distance:.2f} km is: ${revenue:.2f}")

        # Print the profit for the trip
        if profit is not None:
            print(f"The profit for the trip is: ${profit:.2f}")

        # Ask if the user wants to calculate another trip
        another_trip = input("Do you want to calculate the price for another trip? (y/n): ").lower()
        if another_trip == 'n':
            break
        elif another_trip != 'y':
            print("Invalid response. Please enter 'y' for yes or 'n' for no.")



if __name__ == "__main__":
    with open('functions.pkl', 'wb') as file:
        pickle.dump((ask_user, calculate_price_and_profit), file)
