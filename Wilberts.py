import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_makes():
    url = 'https://www.wilberts.com/u-pull-it/'

    request_car_makes = requests.post(url)

    if request_car_makes.status_code == 200:
        makes_soup = BeautifulSoup(request_car_makes.text, 'html.parser')
        makes_tag = makes_soup.find(id='search_car_makes')

        car_makes = {}

        for make in makes_tag:
            car_makes[make['value']] = make.text

        del car_makes['0']

        return car_makes
    else:
        print('Makes request failed!')

def get_models(make_id):
    url = 'https://www.wilberts.com/u-pull-it/wp-admin/admin-ajax.php'

    payload = {
    'action': 'genInvCarModels',
    'carmake': make_id,
    'carmodel': '248',
    'caryear': '2009',
    'currentlocation': 'bath'
    }

    request_car_models = requests.post(url, data=payload)

    if request_car_models.status_code == 200:
        models_soup = BeautifulSoup(request_car_models.text, 'html.parser')

        car_models = {}

        for model in models_soup:
            car_models[model['value']] = model.text

        del car_models['0']

        return car_models
    else:
        print('Models request failed!')

def get_cars(make_id, model_id):
    url = 'https://www.wilberts.com/u-pull-it/wp-admin/admin-ajax.php'

    payload = {
    'action': 'genInvSearchReport',
    'carmake': make_id,
    'carmodel': model_id,
    'caryear': '2009',
    'currentlocation': 'bath'
    }

    request_cars = requests.post(url, data=payload)

    if request_cars.status_code == 200:
        cars_soup = BeautifulSoup(request_cars.text, 'html.parser')

        return cars_soup
    else:
        print('Cars request failed!')

def save_cars():
    car_info = {
    'Make': [],
    'Model': [],
    'Year': [],
    'VIN': [],
    'Days in Yard': []
    }
    
    makes = get_makes()

    for make_id, make_text in makes.items():
        models = get_models(make_id)

        for model_id, model_text in models.items():
            cars = get_cars(make_id, model_id)

            for car in cars:
                year = car.contents[0].text
                vin = car.contents[2].text
                days = car.contents[3].text

                if year != 'Year':
                    car_info['Make'].append(make_text)
                    car_info['Model'].append(model_text)
                    car_info['Year'].append(year)
                    car_info['VIN'].append(vin)
                    car_info['Days in Yard'].append(days)

    yard_data = pd.DataFrame(car_info)
    yard_data.to_csv('yard_data.csv')

def main():
    #Urllib parser has dumb interpretation on their robots file. I don't like it either...
    if 'Allow: /wp-admin/admin-ajax.php' in requests.get('https://www.wilberts.com/robots.txt').text:
        save_cars()
    else:
        print('No more robots!')

if __name__ == '__main__':
    main()
