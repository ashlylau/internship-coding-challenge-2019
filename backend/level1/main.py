import json
import datetime

class CarRentalBooking:
    def __init__(self, rental_id,
    start_date, end_date, distance):
        self.rental_id = rental_id
        self.start_date = start_date
        self.end_date = end_date
        self.distance = distance

    def setCar(self, car):
        self.car_id = car.car_id
        self.price_per_day = car.price_per_day
        self.price_per_km = car.price_per_km

    def calcRentalPrice(self):
        return self.calcTimeComponent() + self.calcDistComponent()

    def calcTimeComponent(self):
        start = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
        num_of_days = (end - start).days + 1
        return num_of_days * self.price_per_day

    def calcDistComponent(self):
        return self.distance * self.price_per_km

class Car:
    def __init__(self, car_id, price_per_day, price_per_km):
        self.car_id = car_id
        self.price_per_day = price_per_day
        self.price_per_km = price_per_km

cars = {}
output = {}
output['rentals'] = []
with open('data/input.json') as input_file:
    input_data = json.load(input_file)
    for car_data in input_data['cars']:
        cars[car_data['id']] = Car(car_data['id'], car_data['price_per_day'],
        car_data['price_per_km'])

    for rental_data in input_data['rentals']:
        booking = CarRentalBooking(rental_data['id'], rental_data['start_date'],
        rental_data['end_date'], rental_data['distance'])
        booking.setCar(cars[rental_data['car_id']])
        output['rentals'].append({'id': booking.rental_id, 'price': booking.calcRentalPrice()})

with open('output.txt', 'w') as outfile:
    json.dump(output, outfile)
