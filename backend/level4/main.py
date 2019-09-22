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
        self.rental_price = rental_price
        self.num_of_days = num_of_days
        self.commission_amt = rental_price * 0.3

    def calcDriver(self):
        return self.rental_price

    def calcOwner(self):
        return self.rental_price * 0.7

    def calcInsurance(self):
        return self.commission_amt / 2

    def calcAssistance(self):
        # 1€/day with price represented in cents
        return self.num_of_days * 100

    def calcDrivy(self):
        return self.commission_amt - self.calcInsurance() - self.calcAssistance()

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

        commission = Commission(booking.calcRentalPrice(), booking.num_of_days)
        actions = []
        actions.append(Action('driver', 'debit', commission.calcDriver()).toDict())
        actions.append(Action('owner', 'credit', commission.calcOwner()).toDict())
        actions.append(Action('insurance', 'credit', commission.calcInsurance()).toDict())
        actions.append(Action('assistance', 'credit', commission.calcAssistance()).toDict())
        actions.append(Action('drivy', 'credit', commission.calcDrivy()).toDict())

        output['rentals'].append({'id': booking.rental_id, 'actions': actions})

with open('data/output.json', 'w') as outfile:
    json.dump(output, outfile)
