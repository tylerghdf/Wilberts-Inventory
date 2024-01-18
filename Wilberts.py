import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {}

payload = {
    'action': 'genInvCarModels',
    'carmake': '48',
    'carmodel': '248',
    'caryear': '2009',
    'currentlocation': 'bath'
}

car_info = {
    'Make': [],
    'Model': [],
    'Year': [],
    'VIN': [],
    'Days in Yard': []
    }

#make sure the request went through -- returns request
def MakeRequest(url, headers = {}, data = {}):
    request = requests.post(url, headers=headers, data=data)

    if request.status_code == 200:
        return request
    else:
        print('Request failed!')

        return None

# Used to get the newest information from the website
def QueryInventory():
    makes_url = 'https://www.wilberts.com/u-pull-it/'

    request_car_makes = MakeRequest(makes_url)

    if request_car_makes != None:
        makes_soup = BeautifulSoup(request_car_makes.text, 'html.parser') #must parse entire page for the makes
        makes_tag = makes_soup.find(id='search_car_makes') #input field for selecting different makes has this id

        form_url = 'https://www.wilberts.com/u-pull-it/wp-admin/admin-ajax.php'

        #gets all the makes
        for option in makes_tag:
            make_id = int(option['value'])
            make_text = option.text

            #looping through makes and getting all cars for each model
            if make_id != 0:
                payload['action'] = 'genInvCarModels'
                payload['carmake'] = make_id

                request_car_models = MakeRequest(form_url, None, payload)

                if request_car_models != None:
                    models_soup = BeautifulSoup(request_car_models.text, 'html.parser')

                    #looping through models of cars
                    for model in models_soup:
                        model_id = int(model['value'])
                        model_text = model.text

                        if model_id != 0:
                            payload['action'] = 'genInvSearchReport'
                            payload['carmodel'] = model_id

                            request_cars = MakeRequest(form_url, None, payload)

                            if request_cars != None:
                                cars_soup = BeautifulSoup(request_cars.text, 'html.parser')

                                #going through every car that got returned and getting year and vin information
                                for car in cars_soup:
                                    year = car.contents[0].text
                                    vin = car.contents[2].text
                                    days = car.contents[3].text

                                    if year != 'Year':
                                        car_info['Make'].append(make_text)
                                        car_info['Model'].append(model_text)
                                        car_info['Year'].append(year)
                                        car_info['VIN'].append(vin)
                                        car_info['Days in Yard'].append(days)
                                        
            
    else:
        print('Query failed to acquire makes!')

QueryInventory()

df = pd.DataFrame(car_info)
df.to_excel('WilbertsCarData.xlsx')
print('Done.')
