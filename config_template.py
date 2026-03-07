# --------------------------------------------------
# RTB SCRAPER INPUT DATA
# 
# 1) Location criteria: Eircode.  Optionally also local authority and electoral area, but in the code they are now autopopulated from the address.
# 2) Reference property details: Dwelling type, BER, Bedrooms and Floor size
# 3) Ranges to search for comparable properties: Dwelling type, BER, Bedrooms and Floor size
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


# Query data - template

EIRCODE = "D03W5N0" 
# local_authority_value = "xx" # not currently used in the code
# electoral_area_value = "xxxxxxxxx" # not currently used in the code

reference_dwelling_type = "100"  # House
reference_ber = "7" # C1
reference_bedrooms = 3
reference_floor_space = 83

# other values to query
dwelling_types = ["100"]  # House
ber_values = ["4","5"] 
bedrooms = [3,4]
floor_range = range(80,90) # queries from low value to high value minus one, using the incremement below
floor_space_incr = 5
