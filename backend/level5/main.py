import json
import datetime

class CarRentalBooking:
    def __init__(self, rental_id,
    start_date, end_date, distance, car):
        self.rental_id = rental_id
        self.start_date = start_date
        self.end_date = end_date
        self.distance = distance
        self.car_id = car.car_id
        self.price_per_day = car.price_per_day
        self.price_per_km = car.price_per_km
        self.options = []

    def addOption(self, option):
        self.options.append(option)

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
    def __init__(self, rental_price, num_of_days, options):
        self.rental_price = rental_price
        self.num_of_days = num_of_days
        self.options = options
        self.commission_amt = rental_price * 0.3

    def calcDriver(self):
        driver_amount = self.rental_price
        if "gps" in self.options:
            driver_amount += 500 * self.num_of_days
        if "baby_seat" in self.options:
            driver_amount += 200 * self.num_of_days
        if "additional_insurance" in self.options:
            driver_amount += 1000 * self.num_of_days
        return driver_amount

    def calcOwner(self):
        owner_amount = self.rental_price * 0.7
        if "gps" in self.options:
            owner_amount += 500 * self.num_of_days
        if "baby_seat" in self.options:
            owner_amount += 200 * self.num_of_days
        return owner_amount

    def calcInsurance(self):
        return self.commission_amt / 2

    def calcAssistance(self):
        return self.num_of_days * 100

    def calcDrivy(self):
        drivy_amount = self.commission_amt - self.calcInsurance() - self.calcAssistance()
        if "additional_insurance" in self.options:
            drivy_amount += 1000 * self.num_of_days
        return drivy_amount

class Action:
    def __init__(self, who, type, amount):
        self.who = who
        self.type = type
        self.amount = amount

    def toDict(self):
        dict = {}
        dict.update({'who': self.who})
        dict.update({'type': self.type})
        dict.update({'amount': self.amount})
        return dict

cars = {}
rentals = {}
output = {}
output['rentals'] = []
with open('data/input.json') as input_file:
    input_data = json.load(input_file)
    for car_data in input_data['cars']:
        cars[car_data['id']] = Car(car_data['id'], car_data['price_per_day'],
        car_data['price_per_km'])

    for rental_data in input_data['rentals']:
        booking = CarRentalBooking(rental_data['id'], rental_data['start_date'],
        rental_data['end_date'], rental_data['distance'], cars[rental_data['car_id']])

        rentals[rental_data['id']] = booking

    for option_data in input_data['options']:
        rentals[option_data['rental_id']].addOption(option_data['type'])

    for rental_booking in rentals.values():
        commission = Commission(rental_booking.calcRentalPrice(),
            rental_booking.num_of_days, rental_booking.options)
        actions = []
        actions.append(Action('driver', 'debit', commission.calcDriver()).toDict())
        actions.append(Action('owner', 'credit', commission.calcOwner()).toDict())
        actions.append(Action('insurance', 'credit', commission.calcInsurance()).toDict())
        actions.append(Action('assistance', 'credit', commission.calcAssistance()).toDict())
        actions.append(Action('drivy', 'credit', commission.calcDrivy()).toDict())

        output['rentals'].append({'id': rental_booking.rental_id,
            'options': rental_booking.options, 'actions': actions})

with open('data/output.json', 'w') as outfile:
    json.dump(output, outfile)
