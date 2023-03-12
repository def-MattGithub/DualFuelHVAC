# DualFuelHVAC
Calculates if it's cheaper to run your heat pump or furnace.  Proof of concept

Currently written for a two tier electric rate system and natural gas

------

Required Data Inputs:
 
  Commonly Changed Variables:
  
  -OutdoorTemp : Current outdoor temperature, in farenheight
  
  -CostPerTherm : Natural gas rate per therm, in dollars
  
  -ElecTier1 : base electric rate, in dollars per killowat hour
  
  -ElecTier2 : elevated electric rate.  Ex: Tier 2 or Peak demand rate.  Depends on your utility plan.
  
  -CurrentElecTier : which tier/rate are you being charged at in this moment.

 
 Setup Variables:
  
  -AFUE : Efficcency of your furnace.  Check the label on your furnace to find this.  This is usually 80 for modern cheap systems or it could be as high as 98.  It's a percentage of how much fuel energy can be converted to heat in your house.
  
  -Data Points : Many heat pumps only publish two data points consisting of 1. Outdoor Temperature      and 2. COP of the heat pump at that tempature.
  
  -DataHi : (Higher Temperature, COP at that temperature)  
  
  -DataLo : (Lower Temperature, COP at that temperature)

------


Ultimate goal is to integrate this into my Home Assistant and:
-Pull rates from utility provider API (PG&E requires an x509 cert from a public CA which I don't want to pay for, so I enter rates manually now)
-Pull current outdoor temperature from local sensor in Home Assistant
-Run the calculation either before each call for heat (for people with volatile rates), or likely a daily cron job for PG&E
-Set thermostat to use the cheapest heat source.  This may have to be manually done with Ecobee

