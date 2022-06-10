import csv
import random 

class Battery:
    def __init__(self, id):
        self.id = id
        self.percentCap = random.randint(75,100)
        self.energy = random.randint(500,800)
        self.percentCharge = random.randint(2000,4000)
        self.temp = random.randint(15,36)
        self.health = random.randint(75,100)
        self.totalVoltage = random.uniform(10,16.8)
        self.cellOneV =  random.uniform(3,4.2)
        self.cellTwoV =  random.uniform(3,4.2)
        self.cellThreeV= random.uniform(3,4.2)
        self.cellFourV = random.uniform(3,4.2)

data = []
headers = ['ID','Capacity (%)', 'Energy (Wh)', 'Charge Capacity (mAh)', 'Temperature (C)', 'BMS Health (%)', 'Total Voltage (V)', \
    'Cell 1 Voltage (V)', 'Cell 2 Voltage (V)', 'Cell 3 Voltage (V)', 'Cell 4 Voltage (V)']
for i in range(1,11):
    data.append(Battery(i))
with open('bmsData.csv', 'w', encoding='UTF8', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(headers)
    for dataPoint in data:
        csv_writer.writerow([dataPoint.id,dataPoint.percentCap,dataPoint.energy,\
            dataPoint.percentCharge,dataPoint.temp,dataPoint.health, dataPoint.totalVoltage, \
            dataPoint.cellOneV,dataPoint.cellTwoV, dataPoint.cellThreeV, dataPoint.cellFourV])

