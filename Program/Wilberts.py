import constants
import os
import time
import json
import requests
import tkinter as tk
import pandas as pd
from pandastable import Table

def parse_cars(raw_data):
    raw_data = json.loads(raw_data)

    # Only the details field holds the information needed (Never empty)
    details = raw_data['details']

    # Load nested json and get cars from vehicle details field (Empty is no cars of make a model)
    cars_data = json.loads(details)
    cars_data = cars_data['vehicleDetails']

    # Cleanest way to avoid errors
    if len(cars_data) == 0:
        return cars_data

    # Empty list for cleaned car data
    cleaned_car_data = []

    for car in cars_data:
        car = {
        'Make': car['Make'],
        'Model': car['Model'],
        'Year': car['Year'],
        'VIN': car['VIN'],
        'Days in Yard': car['DaysInYard'],
        'StockID': car['StockID']
        }

        cleaned_car_data.append(car)

    return cleaned_car_data

def get_cars(make, model):
    # You only need these 2 fields for the payload
    payload = {
    'Make': make,
    'Model': model
    }

    request_cars = requests.post(constants.CARS_URL, json=payload)

    if request_cars.status_code == 200:
        return request_cars.text
    else:
        print('Cars request failed!')

def save_cars():
    car_info = {
    'Make': [],
    'Model': [],
    'Year': [],
    'VIN': [],
    'Days in Yard': [],
    'StockID': []
    }
    
    # The values are what's used in the requests, but keep the keys/ids around for later possible checking.
    makes = constants.MAKES_DICT.values()

    for make in makes:
        models = constants.MODELS_DICT[make]

        for model in models:
            cars = get_cars(make, model) # Don't mess with this string. It has so much bad formatting that touching it breaks everything json.

            parsed_cars = parse_cars(cars)
            
            for car in parsed_cars:
                car_info['Make'].append(car['Make'])
                car_info['Model'].append(car['Model'])
                car_info['Year'].append(car['Year'])
                car_info['VIN'].append(car['VIN'])
                car_info['Days in Yard'].append(car['Days in Yard'])
                car_info['StockID'].append(car['StockID'])

                print(car)
            
            # Rate limit out of respect :) ILY Wilberts!
            time.sleep(.3)

    # Converting data to dataframe
    yard_data = pd.DataFrame(car_info)

    # Cleaning data and saving (formats for comparisons)
    yard_data = yard_data.dropna()
    yard_data = yard_data.drop_duplicates(subset='VIN')

    if os.path.exists('Data/yard_data.csv'):
        os.rename('Data/yard_data.csv', 'Data/old_yard_data.csv')

        yard_data.to_csv('Data/yard_data.csv', index=False)

        get_changes()
    else:
        yard_data.to_csv('Data/yard_data.csv', index=False)

# Comparison of new and old yard data
def get_changes():
    print('Hey dummy make this actually take into account the time since last scraped so it does the thing right')
    print('Also make this do something if neither file exists')
    new_data = pd.read_csv('Data/yard_data.csv')
    old_data = pd.read_csv('Data/old_yard_data.csv')

    changed_data = pd.concat([new_data, old_data]).drop_duplicates(subset=['VIN'], keep=False)

    #Saving all the changes to respective files
    changed_data[changed_data['Days in Yard'] < 7].to_csv('Data/added_to_yard.csv', index=False)
    changed_data[changed_data['Days in Yard'] > 7].to_csv('Data/removed_from_yard.csv', index=False)

def display_yard_data():
    yard_data = pd.read_csv('Data/yard_data.csv')

    data_window = tk.Toplevel()
    data_window.title('Yard Data')

    car_table = Table(data_window, dataframe=yard_data)
    car_table.show()

def display_new_data():
    yard_data = pd.read_csv('Data/added_to_yard.csv')

    data_window = tk.Toplevel()
    data_window.title('New Yard Data')

    car_table = Table(data_window, dataframe=yard_data)
    car_table.show()

def main():
    main_window = tk.Tk()
    main_window.title('Wilberts Car Data')

    search_button = tk.Button(main_window, text='Run Search', command=save_cars)
    search_button.pack()

    yard_data_button = tk.Button(main_window, text='Display Yard Data', command=display_yard_data)
    yard_data_button.pack()

    new_data_button = tk.Button(main_window, text='Display New Data', command=display_new_data)
    new_data_button.pack()

    main_window.mainloop()

if __name__ == '__main__':
    main()
