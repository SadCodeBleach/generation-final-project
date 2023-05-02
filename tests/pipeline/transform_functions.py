import pandas as pd
import json

#Read and sanitise raw csv
def read_sanitise_csv(raw_csv):
    try:
        columns =  ['date_time', 'location', 'full_name', 'order', 'transaction_total', 'payment_type', 'card_number']  # Headers for the orders csv files
        df = pd.read_csv(raw_csv, header=None, names=columns)
        sanitised_df = df.drop(columns=['full_name', 'card_number'])

    except FileNotFoundError as fnfe:
        print(f'File not found: {fnfe}')

    return sanitised_df
        

df = read_sanitise_csv(raw_csv)
        

def update_location_table(conn, sanitised_data):
    # Extract the unique location names from the raw data
    unique_locations = sanitised_data['location'].unique()

    # Check if each location exists in the database, and insert it if it doesn't
    for location_name in unique_locations:
        # Check if the location already exists in the database
        with conn.cursor() as cur:
            cur.execute('SELECT location_id FROM locations WHERE location_name=%s', (location_name,))
            row = cur.fetchone()

        # If the location doesn't exist, insert it and get the new ID
        if row is None:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO locations (location_name) VALUES (%s) RETURNING location_id', (location_name,))
                location_id = cur.fetchone()[0]
        else:
            location_id = row[0]

    # Commit the changes
    conn.commit()


print(update_location_table(conn, df))













    # for location in df['location'].unique():
    #     if location not in location_dict:
            
    #         new_location = df.iloc[0].iat[1]
            
    #         if  max(location_dict.values()) == "0":
    #             next_num = 0
            
    #         else:     
    #             next_num = max(location_dict.values()) + 1
            
    #         location_dict[new_location] = next_num
            
    #     df['location'] = df['location'].replace(location_dict)
        


#Normalise orders_products



#Normalise products



#Normalise payment_types


#Normalise orders
#def normalise_orders(raw_csv):
# Select locations and switch locations with ID


# Test -----------------------------------

# df = read_sanitise_csv('chesterfield_25-08-2021_09-00-00.csv')
# location_df = normalise_location(df)
# print(location_df.head())