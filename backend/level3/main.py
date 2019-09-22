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
        num_of_days = self.getNumDays()
        price = self.price_per_day

        total_price = 0
        if num_of_days > 10:
            total_price += price * 0.5 * (num_of_days - 10)
            num_of_days = 10
        if num_of_days > 4:
            total_price += price * 0.7 * (num_of_days - 4)
            num_of_days = 4
        if num_of_days > 1:
            total_price += price * 0.9 * (num_of_days - 1)
            num_of_days = 1
        total_price += price

        return total_price

    def getNumDays(self):
        start = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
        self.num_of_days = (end - start).days + 1
        return self.num_of_days

    def calcDistComponent(self):
        return self.distance * self.price_per_km

class Car:
    def __init__(self, car_id, price_per_day, price_per_km):
        self.car_id = car_id
        self.price_per_day = price_per_day
        self.price_per_km = price_per_km

class Commission:
    def __init__(self, rental_price, num_of_days):
        self.commission_amt = rental_price * 0.3
        self.num_of_days = num_of_days

    def calcCommission(self):
        commission_dict = {}
        insurance_fee = Commission.calcInsurance(self.commission_amt)
        roadside = Commission.calcRoadsideAssistance(self.num_of_days)
        rest = self.commission_amt - insurance_fee - roadside

        commission_dict.update({'insurance_fee': insurance_fee})
        commission_dict.update({'assistance_fee': roadside})
        commission_dict.update({'drivy_fee': rest})

        return commission_dict

    def calcInsurance(price):
        return price / 2

    def calcRoadsideAssistance(num_of_days):
        # 1€/day with price represented in cents
        return num_of_days * 100



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
        output['rentals'].append(
            {'id': booking.rental_id,
             'price': booking.calcRentalPrice(),
             'commission': Commission(booking.calcRentalPrice(),
                booking.num_of_days).calcCommission()
            })

with open('data/output.json', 'w') as outfile:
    json.dump(output, outfile)
