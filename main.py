
import pandas as pd
from sklearn.linear_model import LinearRegression

"""---Start Global Variables---"""
# commonly changed variables
OutdoorTemp = 50  # Farenheight
CostPerTherm = 2.21
ElecTier1 = .34
ElecTier2 = .43
CurrentElecTier = ElecTier2  # leave None to average, or input ElecTier1 or ElecTier2
# setup variables
AFUE = 80
DataHi = (45, 3.62)
DataLo = (17, 2.44)
"""---End Global Variables---"""


# for multi-tier or TOD electric rates
def ElectricTier():
    if CurrentElecTier is None:
        costperkwh = (ElecTier1 + ElecTier2) / 2.0
    else:
        costperkwh = CurrentElecTier
    print('electric rate: ', costperkwh)
    return costperkwh


# calculated COP of heat pump at current temp (mostly made by Bing chat)
def FindCOP(outtemp, data1, data2):
    if outtemp == DataHi[0]:
        return DataHi[1]
    elif outtemp == DataLo[0]:
        return DataLo[1]
    else:
        estimated = True
   
    # Create data frame
    df = pd.DataFrame({'Temp': [DataHi[0], DataLo[0]],
                       'COP': [DataHi[1], DataLo[1]]})

    # Fit linear regression model
    model = LinearRegression()
    model.fit(df[['Temp']], df['COP'])

    # Get slope and intercept coefficients
    modelCoef = model.coef_[0] #m
    modelIncpt = model.intercept_ #b

    # Calculate COP for any outdoor temperature x
    outFloat = float(outtemp) #x
    calc = modelCoef * outFloat + modelIncpt

    print(f'The COP of your heat pump at {outFloat} F is {calc:.2f}')
    if estimated == True:
        print('the COP was estimated')
    return calc

# formats AFUE to use in calculation
def AFUEloss(afue):
    if 70 <= afue <= 98:
        afueloss = (1 - (afue * 0.01)) + 1
        return afueloss
    else:
        print('AFUE must be between 70 and 98.  entry of:', afue, ' is not valid')
        exit(0)

"""takes energy costs and efficency of furnace/pump
and decides what fuel to use at a given moment"""
def PumpOrBurn(costtherm, costelec, cop, afueloss):
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
AFUECalc = AFUEloss(AFUE)
COP = (FindCOP(OutdoorTemp, DataHi, DataLo))
Output = PumpOrBurn(CostPerTherm, CostPerKWH, COP, AFUECalc)
print(Output)
