import pandas as pd
from faker import Faker
import numpy as np
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Initialize the Faker library
fake = Faker()

# --- PREDEFINED LOCATIONS ---
# We define a specific list of cities and states to choose from
locations = [
    {'city': 'San Francisco', 'state': 'CA'},
    {'city': 'New York', 'state': 'NY'},
    {'city': 'Los Angeles', 'state': 'CA'},
    {'city': 'Dallas', 'state': 'TX'},
    {'city': 'Houston', 'state': 'TX'},
    {'city': 'Boise', 'state': 'ID'},
    {'city': 'Seattle', 'state': 'WA'},
    {'city': 'Chicago', 'state': 'IL'},
    {'city': 'Miami', 'state': 'FL'},
    {'city': 'Boston', 'state': 'MA'},
    {'city': 'Denver', 'state': 'CO'},
    {'city': 'Atlanta', 'state': 'GA'},
    {'city': 'Portland', 'state': 'OR'},
    {'city': 'Phoenix', 'state': 'AZ'},
    {'city': 'Philadelphia', 'state': 'PA'},
    {'city': 'San Diego', 'state': 'CA'},
    {'city': 'Austin', 'state': 'TX'},
    {'city': 'Nashville', 'state': 'TN'},
    {'city': 'Minneapolis', 'state': 'MN'},
    {'city': 'Raleigh', 'state': 'NC'},
    {'city': 'Salt Lake City', 'state': 'UT'},
    {'city': 'Orlando', 'state': 'FL'},
    {'city': 'Cleveland', 'state': 'OH'},
    {'city': 'Sacramento', 'state': 'CA'},
    {'city': 'Tampa', 'state': 'FL'},
    {'city': 'Columbus', 'state': 'OH'},
    {'city': 'Indianapolis', 'state': 'IN'},
    {'city': 'Charlotte', 'state': 'NC'},
    {'city': 'Baltimore', 'state': 'MD'},
    {'city': 'Milwaukee', 'state': 'WI'},
    {'city': 'Kansas City', 'state': 'MO'},
    {'city': 'Cincinnati', 'state': 'OH'},
    {'city': 'Pittsburgh', 'state': 'PA'},
    {'city': 'Richmond', 'state': 'VA'},
    {'city': 'Louisville', 'state': 'KY'},
    {'city': 'Memphis', 'state': 'TN'},
    {'city': 'Oklahoma City', 'state': 'OK'},
    {'city': 'Las Vegas', 'state': 'NV'},
    {'city': 'Albuquerque', 'state': 'NM'},
    {'city': 'Tucson', 'state': 'AZ'},
    {'city': 'Fresno', 'state': 'CA'},
    {'city': 'Long Beach', 'state': 'CA'},
    {'city': 'Mesa', 'state': 'AZ'},
    {'city': 'Virginia Beach', 'state': 'VA'},
    {'city': 'Oakland', 'state': 'CA'},
    {'city': 'Tulsa', 'state': 'OK'},
    {'city': 'Arlington', 'state': 'TX'},
    {'city': 'New Orleans', 'state': 'LA'}
]

# Define the number of customers you want
num_customers = 2000

# --- 1. GENERATE THE CUSTOMERS TABLE ---
print("Generating customers data...")
customers_data = []
for i in range(num_customers):
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    # *** CHANGE IS HERE ***
    # Pick a random location from our predefined list but with weighted probabilities
    location = random.choices(
        locations,
        weights=[10 if loc['state'] in ['CA', 'TX', 'FL', 'NY'] else 5 for loc in locations],
        k=1
    )[0] # More weight to populous states like CA, TX, FL, NY

    customers_data.append({
        'customer_id': f'C{i+1:05d}',
        'customer_name': f'{first_name} {last_name}',
        'email': f'{first_name.lower()}.{last_name.lower()}@example.com',
        'join_date': fake.date_between(start_date='-2y', end_date='today'),
        'city': location['city'], # Use the city from our list
        'state': location['state'],   # Use the state from our list
        'acquisition_channel': np.random.choice(
            ['Organic Search', 'Paid Social', 'Referral', 'Email Marketing'],
            p=[0.4, 0.3, 0.2, 0.1]
        )
    })
customers_df = pd.DataFrame(customers_data)
# We can remove the missing city imperfection now that we control the list
# num_missing = int(len(customers_df) * 0.05)
# missing_indices = np.random.choice(customers_df.index, num_missing, replace=False)
# customers_df.loc[missing_indices, 'city'] = np.nan
customers_df.to_csv('customers.csv', index=False)
print("Successfully saved customers.csv")

# --- 2. GENERATE THE PRODUCTS TABLE ---
print("\nGenerating products data...")
products_data = [
    {'product_id': 'P001', 'product_name': 'Standard Snack Box', 'product_type': 'Subscription', 'price': 29.99},
    {'product_id': 'P002', 'product_name': 'Premium Vegan Box', 'product_type': 'Subscription', 'price': 39.99},
    {'product_id': 'P003', 'product_name': 'Gluten-Free Box', 'product_type': 'Subscription', 'price': 34.99},
    {'product_id': 'P004', 'product_name': 'One-Time Holiday Gift Box', 'product_type': 'One-Time', 'price': 49.99},
    {'product_id': 'P005', 'product_name': 'One-Time Celebration Box', 'product_type': 'One-Time', 'price': 59.99},
    {'product_id': 'P006', 'product_name': 'One-Time Snack Sampler', 'product_type': 'One-Time', 'price': 19.99},
    {'product_id': 'P007', 'product_name': 'Family Snack Pack', 'product_type': 'Subscription', 'price': 44.99},
    {'product_id': 'P008', 'product_name': 'Keto Snack Box', 'product_type': 'Subscription', 'price': 39.99},
    {'product_id': 'P009', 'product_name': 'One-Time Movie Night Box', 'product_type': 'One-Time', 'price': 29.99},
    {'product_id': 'P010', 'product_name': 'One-Time Fitness Snack Box', 'product_type': 'One-Time', 'price': 34.99}
]
products_df = pd.DataFrame(products_data)
products_df.to_csv('products.csv', index=False)
print("Successfully saved products.csv")

# --- 3. GENERATE SUBSCRIPTIONS AND TRANSACTIONS ---
print("\nGenerating subscriptions and transactions data...")

subscriptions_data = []
transactions_data = []
subscription_id_counter = 1
transaction_id_counter = 1
today = datetime.now().date()

sub_products = products_df[products_df['product_type'] == 'Subscription']
onetime_products = products_df[products_df['product_type'] == 'One-Time']

for _, customer in customers_df.iterrows():
    join_date = customer['join_date']

    if random.random() < 0.70:
        chosen_sub = sub_products.sample(1).iloc[0]
        start_date = join_date + timedelta(days=random.randint(1, 30))
        if start_date > today:
            continue

        current_date = start_date
        status = 'Active'
        end_date = None
        
        while current_date < today:
            transactions_data.append({
                'transaction_id': f'T{transaction_id_counter:06d}',
                'customer_id': customer['customer_id'],
                'product_id': chosen_sub['product_id'],
                'transaction_date': current_date,
                'amount_paid': chosen_sub['price']
            })
            transaction_id_counter += 1
            
            if random.random() < 0.03:
                status = 'Cancelled'
                end_date = current_date + timedelta(days=random.randint(1, 28))
                break
            
            current_date += relativedelta(months=1)

        subscriptions_data.append({
            'subscription_id': f'S{subscription_id_counter:05d}',
            'customer_id': customer['customer_id'],
            'product_id': chosen_sub['product_id'],
            'start_date': start_date,
            'end_date': end_date,
            'status': status
        })
        subscription_id_counter += 1

    if random.random() < 0.25:
        for _ in range(random.randint(1, 3)):
            chosen_product = onetime_products.sample(1).iloc[0]
            purchase_date = fake.date_between(start_date=join_date, end_date='today')
            transactions_data.append({
                'transaction_id': f'T{transaction_id_counter:06d}',
                'customer_id': customer['customer_id'],
                'product_id': chosen_product['product_id'],
                'transaction_date': purchase_date,
                'amount_paid': chosen_product['price']
            })
            transaction_id_counter += 1

subscriptions_df = pd.DataFrame(subscriptions_data)
transactions_df = pd.DataFrame(transactions_data)

subscriptions_df.to_csv('subscriptions.csv', index=False)
transactions_df.to_csv('transactions.csv', index=False)

print(f"Successfully saved subscriptions.csv with {len(subscriptions_df)} records.")
print(f"Successfully saved transactions.csv with {len(transactions_df)} records.")
print("\nData generation complete! All files are ready.")