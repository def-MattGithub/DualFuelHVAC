# import numpy
# import matplotlib.pyplot as plt


import pandas as pd
from sklearn.linear_model import LinearRegression


"""---Start Global Variables---"""
# commonly changed variables
OutdoorTemp = 40  # Farenheight
CostPerTherm = 2.68
ElecTier1 = .33
ElecTier2 = .40
CurrentElecTier = ElecTier2  # leave None to average, or input ElecTier1 or ElecTier2

# setup variables
AFUE = 80
DataHi = (45, 3.62)
DataLo = (17, 2.44)
"""---End Global Variables---"""


def ElectricTier():
    if CurrentElecTier is None:
        costperkwh = (ElecTier1 + ElecTier2) / 2.0
    else:
        costperkwh = CurrentElecTier
    print('electric rate: ', costperkwh)
    return costperkwh


# function mostly made by Bing Chat
def FindCOP(outtemp, data1, data2):
    if outtemp == 45:
        return 3.62
    elif outtemp == 17:
        return 2.44
    else:
        estimated = True
    # Create data frame
    df = pd.DataFrame({'Temp': [DataHi[0], DataLo[0]],
                       'COP': [DataHi[1], DataLo[1]]})

    # Fit linear regression model
    model = LinearRegression()
    model.fit(df[['Temp']], df['COP'])

    # Get slope and intercept coefficients
    m = model.coef_[0]
    b = model.intercept_

    # Calculate COP for any outdoor temperature x
    x = float(outtemp)
    y = m * x + b

    print(f'The COP of your heat pump at {x} F is {y:.2f}')
    if estimated == True:
        print('the COP was estimated')
    return y


# takes energy costs and efficency of furnace/pump
# and decides what fuel to use at a given moment
def PumpOrBurn(costtherm, costelec, cop, afue):
    # validate input, convert AFUE value to percentage
    if 80 <= afue <= 98:
        afueloss = (1 - (afue * 0.01)) + 1
    else:
        print('AFUE must be between 80 and 98.  entry of:', afue, ' is not valid')
        exit(0)

    # converts therm to killowat hours equivilant
    ThermtokWH = (costtherm / 29.3)
    WithLoss = (ThermtokWH * afueloss)
    print('Therm to kWh is: ', ThermtokWH, 'at 100% eff')
    print('with loss:', WithLoss)
    ElectricEquiv = (WithLoss * cop)
    print('Electric Equivilant in kWh is: ', ElectricEquiv)

    # compares equivilant prices
    diff = float(ElectricEquiv - costelec)
    print('The difference is:', diff)
    if diff >= float(0):
        print('Gas would have to be ', ((diff - CostPerTherm) * -1),
              ' or lower to be cheaper')
        return 'Pump'
    elif diff < float(0):
        print('Electricty would have to be', (diff + CostPerKWH),
              'to be cheaper')
        return 'Burn'
    else:
        print('there was an error somewhere')
        exit(1)


CostPerKWH = ElectricTier()
COP = (FindCOP(OutdoorTemp, DataHi, DataLo))
Output = PumpOrBurn(CostPerTherm, CostPerKWH, COP, AFUE)
print(Output)
