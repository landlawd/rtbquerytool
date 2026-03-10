# --------------------------------------------------
# RTB SCRAPER INPUT DATA
# 
# 1) Reference property details: Eircode, Dwelling type, BER, Bedrooms and Floor size.

# 2) Ranges to search for comparable properties: Eircodes (one or more), Dwelling type, BER, Bedrooms and Floor size
#    The number of permutations determine the script runtime... be careful!
# 
# The code contains the possibility to set the local authority and electoral area from the config file, but this is not currently used.
# To obtain these values, in the browser you must enter the eircode/address in step 1 and manually "inspect" the element in the page.
# 
# Reference values:
# Note: Querying all of these would take a very long time, especially since we have some "timer waits" built into this script. 
# ... plus a HIGH RISK of getting flagged as a DOS and getting IP-blocked.
#   dwelling_types = ["100", "101"]  # 100=House, 101=Apartment / Flat
#   BER values: 1=A1, 2=A2, 3=A3, 4=B1, 5=B2, 6=B3, 7=C1, 8=C2, 9=C3, 10=D1, 11=D2, 12=E1, 13=E2, 14=F, 15=G, 16=Exempt
#   ber_values = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]  
#   bedrooms = [1,2,3,4,5] # or more
#   floor_range = range(30,200) #  range is from x to y-1, e.g. 30 to 119
#   floor_space_incr = 5  # increment floor space by 5 on each query, more efficient than incrementing every 1.
# --------------------------------------------------


reference_eircode = "F94N232"
# local_authority_value = "5" # DONEGAL COUNTY COUNCIL
# electoral_area_value = "1350404" # Donegal
reference_dwelling_type = "100"  # House
reference_ber = "9" # C3
reference_bedrooms = 3
reference_floor_space = 100

# 2) Comparable properties to query.
# THE FIRST EIRCODE MUST BE THE SAME AS THE REFERENCE PROPERTY
# AND THE OTHER EIRCODES MUST ALL BE IN THE SAME ELECTORAL AREA
# (otherwise they won't be useful comparables!)
comparable_eircodes = ["F94N232", "F94AY99", "F94E8N4", "F94XY42","F94V088","F94TX33","F94E3P4","F94W2K6"]
dwelling_types = ["100"]  # House
ber_values = ["4","5","6","7","8","9","10","11","12"]
bedrooms = [1,2]
floor_range = range(45,70) # queries from low value to high, using the incremement below
# bedrooms = [3,4,5]
# floor_range = range(70,170) # queries from low value to high, using the incremement below
floor_space_incr = 5
