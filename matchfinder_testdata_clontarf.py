# --------------------------------------------------
# RTB MATCHFINDER INPUT DATA
# 
# 1) Reference property details:
#       reference_eircode = an eircode, but not actually used in the current code
#       reference_dwelling_type = "House" or "Apartment / Flat"
#       reference_ber: one of A1, A2, A3, B1, B2, B3, C1, C2, C3, D1, D2, E1, E2, F, G, Exempt
#       reference_bedrooms: positive integer, e.g. 1,2,3,4,5, etc
#       reference_floor_space: positive integer
# 2) dataset: Name of csv file to use as the query data set
# 3) lea_name: Name of the local electoral area, will be used to generate the output filename
# --------------------------------------------------


# Query data - Clontarf

reference_eircode = "D03W5N0" # not currently used in the matchfinder tool
reference_dwelling_type = "House"
reference_ber = "C1"
reference_bedrooms = 3
reference_floor_space = 83

dataset="combined_results_Clontarf_Houses_70-140sqm_widerBER_20260311.csv"
lea_name = "Clontarf"
