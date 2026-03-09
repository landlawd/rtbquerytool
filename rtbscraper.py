# --------------------------------------------------
# Prerequisities to run this script:
#   Python (https://www.python.org/downloads/)
#   Selenium  (pip install -U selenium)
#   Chrome Browser
#   Chrome Driver (https://googlechromelabs.github.io/chrome-for-testing/.  Must match the browser version. Stored in same folder as this file.)
#   
# Usage: python rtbscraper.py <config_file>
# Example: python rtbscraper.py config_D949123
#
# Notes:
#   This code should be fairly resilient. I managed to run it for 416 queries which took 57 minutes (One property type, 9 BER codes, 
#   2 numbers of bedrooms, floor range 85 to 110, incremement floor space by 1). 
#   Having said that, I don't recommend running it for a long time with a very wide criteria.  
#   For one thing, if it fails, you have no output because it writes to csv only at the end (possible enhancement noted below).
#   Also, there is a quickly diminishing return. In the above test of 416 queries, the result set already had 85 entries after 48 queries, 
#   and just 126 after 416. 
#
#   Finally: be careful about the risk of getting blocked by the RTB.  I establish a foreign VPN connection when running the script 
#   so I don't get my home IP blocked.
#   
# Enhancement ideas:
#   * Continuously output to the csv file to make the program more resilient to crashes or time-outs.
# 
# Author: Landlawd 2026.03.07
#   2026.03.09 added multiple eircodes for comparable propertiees
#   2026.03.09 improved logic to reduce number of queries (break floor space loop when no new results)
# --------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import sys
import importlib

# --------------------------------------------------
# LOAD THE CONFIG FILE
# --------------------------------------------------

if len(sys.argv) < 2:
    print("Usage: python rtbscraper.py <config_file>")
    print("Example: python rtbscraper.py config_D949123")
    sys.exit(1)

config_name = sys.argv[1].replace(".py", "")

try:
    config = importlib.import_module(config_name)
except ModuleNotFoundError:
    print(f"Error: Configuration file '{config_name}.py' not found.")
    print("Make sure the file exists in the same directory and do NOT include '.py' in the command.")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error loading config file: {e}")
    sys.exit(1)

print(f"Loaded configuration: {config_name}")

# --------------------------------------------------
# Function to build a list of floor spaces from min to max, iterating from the outside in.
# This will support more efficient querying (ability to break out if no new results found)
# --------------------------------------------------

def build_floor_sequence(min_floor, max_floor, step):
    # Build ascending list from min to max using step
    ascending = list(range(min_floor, max_floor + 1, step))

    # Create outside-in sequence
    floors = []
    left = 0
    right = len(ascending) - 1

    while left <= right:
        if left == right:
            floors.append(ascending[left])
        else:
            floors.append(ascending[left])
            floors.append(ascending[right])
        left += 1
        right -= 1

    return floors

# --------------------------------------------------
# LOAD THE QUERY DATA FROM THE CONFIG FILE
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

reference_eircode = config.reference_eircode
#local_authority_value = config.local_authority_value  # Not used, autopopulated
#electoral_area_value = config.electoral_area_value    # Not used, autopopulated
reference_dwelling_type = config.reference_dwelling_type
reference_ber = config.reference_ber
reference_bedrooms = config.reference_bedrooms
reference_floor_space = config.reference_floor_space

comparable_eircodes = config.comparable_eircodes
dwelling_types = config.dwelling_types
ber_values = config.ber_values
bedrooms = config.bedrooms
floor_range = config.floor_range
floor_space_incr = config.floor_space_incr

# Create an outside-in sequence of floor spaces to query
start_floor = floor_range.start
end_floor = floor_range.stop
floors_to_use = build_floor_sequence(
    start_floor,
    end_floor,
    floor_space_incr
)

print(f"BER query sequence: {ber_values}")
print(f"Floor space query sequence: {floors_to_use}")

# --------------------------------------------------
# Function for Step 1 (enter EIRCODE and choose address) and moving to Step 2
# --------------------------------------------------
def step_1_search(eircode):

    # -------------------------
    # STEP 1 - choose address using eircode and move to step 2
    # -------------------------

    print(f"Entering Eircode: {eircode}")
    eircode_input = wait.until(
        EC.element_to_be_clickable((By.ID, "autoaddress-input"))
    )
    eircode_input.clear()
    eircode_input.send_keys(eircode)

    # Wait for real suggestion (not the 'Select an address' item)
    first_suggestion = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "li.autoaddress-dropdown-item[id^='autoaddress-item']")
        )
    )

    # Scroll into view (important for Autoaddress widget)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_suggestion)
    time.sleep(0.3)

    # Real click (do NOT use JS first)
    first_suggestion.click()
    print("Address selected")

    print("Waiting for Continue button...")
    continue_button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(., 'Continue')]")
        )
    )

    # Scroll into view (prevents intercept issues)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", continue_button)
    time.sleep(0.3)

    try:
        continue_button.click()
    except:
        print("Continue click intercepted, retrying with JS click...")
        driver.execute_script("arguments[0].click();", continue_button)

    print("Continue clicked.")

    # -------------------------
    # Make sure Step 2 is ready
    # -------------------------

    print("Waiting for Step 2 filters...")
    wait.until(EC.presence_of_element_located((By.ID, "dwellingTypeSelect")))
    print("Step 2 loaded.")

    # -------------------------
    # Override the autopopulated Local Authority And Electoral Area
    # Not currently used!
    # -------------------------

    # Set Local Authority  (override default using value from config file)
    # la_select = driver.find_element(By.ID, "laSelect")
    # driver.execute_script(
    #    "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
    #    la_select, local_authority_value
    # )

    # Set Electoral Area  (override default using value from config file)
    # lea_select = driver.find_element(By.ID, "leaSelect")
    # driver.execute_script(
    #    "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
    #    lea_select, electoral_area_value
    # )

    # print("Local Authority and Electoral Area set.")


# --------------------------------------------------
# Function for resetting query criteria before entering a new EIRCODE
# --------------------------------------------------
def reset_step1():
    """
    Click the 'New Search' button to reset criteria between eircodes.
    """
    new_search_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "comparablesNewSearchBtn"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", new_search_btn)
    time.sleep(0.2)
    new_search_btn.click()
    time.sleep(0.5)


# -------------------------
# Create a function to be used inside the loop that will perform a single query and add the results to the array
# -------------------------

def run_search(dwelling, ber, bed, floor, save_match_score,
               call_counter, all_results, unique_result_keys):

    call_counter += 1
    initial_count = len(all_results)

    search_label = f"D={dwelling} BER={ber} Bed={bed} Floor={floor}"

    print(f"[{call_counter}] {search_label}")

    wait.until(EC.element_to_be_clickable((By.ID, "NumberOfBedrooms")))

    dwelling_select = driver.find_element(By.ID, "dwellingTypeSelect")
    ber_select = driver.find_element(By.ID, "BerSelect")
    bed_input = driver.find_element(By.ID, "NumberOfBedrooms")
    floor_input = driver.find_element(By.ID, "FloorSpace")

    # Set filters
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
        dwelling_select, dwelling
    )

    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
        ber_select, ber
    )

    bed_input.clear()
    bed_input.send_keys(str(bed))

    floor_input.clear()
    floor_input.send_keys(str(floor))

    time.sleep(1) # short pause before selecting, extend this if necessary (originally I had 3 seconds but 1 seems to work fine)

    # Re-locate filters container each loop
    filters_container = driver.find_element(By.ID, "dwellingTypeSelect").find_element(By.XPATH, "./ancestor::form")

    # Locate Search button by ID (precise and stable)
    search_button = wait.until(
        EC.presence_of_element_located((By.ID, "comparablesProxyBtn"))
    )

    # Scroll into view (prevents intercept issues)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
    time.sleep(0.5)

    # Wait until clickable
    wait.until(EC.element_to_be_clickable((By.ID, "comparablesProxyBtn")))

    # Try real click first, if it fails fallback to JS click.  Retry 3 tims if necessary.
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            search_button.click()
            break
        except Exception as e:
            print(f"Click attempt {attempt+1} failed: {e}. Retrying with JS click...")
            driver.execute_script("arguments[0].click();", search_button)
            time.sleep(0.2) # short pause for scrolling animation/render, extend if necessary (originally I had 0.5)

    # Allow results to update
    time.sleep(0.5)

    # Collect the results. Put in a try block in case no results shown. I have seen "Invalid API response" message in the webpage.
    try:
        # Wait for the results table to appear. I have seen "Invalid API response" shown and no results, supposedly because there are no matching properties
        wait_table.until(EC.visibility_of_element_located(
           (By.CSS_SELECTOR, "#comparablesProxyResult table.results-table tbody")
        ))

        # Retry loop for stale elements
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Grab all rows
                rows = driver.find_elements(By.CSS_SELECTOR, "#comparablesProxyResult table.results-table tbody tr")
                print(f"   Rows detected: {len(rows)}")

                for tr in rows: # rows collected from the current search
                    try:
                        cells = tr.find_elements(By.TAG_NAME, "td")
                        row_data = [cell.text for cell in cells]

                        # Build duplicate-check key excluding Match Score
                        key = "|".join([text.strip() for i, text in enumerate(row_data) if i != 9])

                        if key not in unique_result_keys:
                            unique_result_keys.add(key)

                            # Build output row excluding Match Score
                            output_row = [text for i, text in enumerate(row_data) if i != 9]

                            # Insert Match Score depending on flag
                            if save_match_score:
                                match_score = row_data[9]
                            else:
                                match_score = ""

                            # Insert it back at column 9
                            output_row.insert(9, match_score)

                            all_results.append(output_row)

                    except Exception as e_cell:
                        print(f"     Skipping a row due to error: {e_cell}")

                break  # success, exit retry loop

            except Exception as e_retry:
                print(f"   Retry {attempt+1}/{max_retries} failed with error: {e_retry}")
                time.sleep(1) # short wait before retry

        # Print cumulative number of unique rows collected so far
        print(f"   Total unique rows so far: {len(all_results)}\n")

    except TimeoutException:
        print("No results table found (invalid API response). Skipping this search and moving on.")

    except Exception as e_outer:
        print(f"Unexpected error while scraping results: {e_outer}. Moving to next search.")

    new_rows_added = len(all_results) - initial_count
    return call_counter, new_rows_added

# --------------------------------------------------
# Ok, let's get ready to go....
# --------------------------------------------------

# Record start time
start_time = time.time()

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20) # main wait for page navigation, elements like the Eircode field, Continue button, and Step 2 filters. It needs to be long enough (20 s is safe) because the page can be slow to load.
wait_table = WebDriverWait(driver, 3)  # 3 seconds to wait for results table to appear (it doesn't always). But don't want to wait too long... move on.


# -------------------------
# STEP 0 - open site and close cookies popup
# -------------------------

print("Opening RTB site...")
print("Sometimes it hangs here, the cookies window is not closed and the script doesn't move on.  If this happens, kill and run again...")
driver.get("https://rtb.ie/rtb-rent-register/")


# Close cookies
try:
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
    )
    cookie_button.click()
    print("Cookies popup closed.")
except:
    print("No cookie popup.")


# -------------------------
# First collect the results for the reference property, including match score
# Includes both Step 1 and Step 2 searches
# -------------------------

all_results = []
unique_result_keys = set()  # to track duplicates

seen_rows = set()
call_counter = 0

print("\nRunning reference property search...\n")
step_1_search(reference_eircode)
call_counter, _ = run_search(
    reference_dwelling_type,
    reference_ber,
    reference_bedrooms,
    reference_floor_space,
    save_match_score=1,
    call_counter=call_counter,
    all_results=all_results,
    unique_result_keys=unique_result_keys
)

# -------------------------
# Next loop through all the search criteria for comparable properties, excluding match scores
# Includes both Step 1 and Step 2 searches
# -------------------------


print("\nRunning additonal property searches...\n")

for idx, eircode in enumerate(comparable_eircodes, start=1):
    print(f"\nComparable eircode {idx}/{len(comparable_eircodes)}: {eircode}")

    # Reset step 1 search so new eircode can be entered
    reset_step1()

    # Perform step 1 search using eircode and move to step 2
    step_1_search(eircode)

    # Repeat step 2 search using all combinations of query criteria
    for dwelling in dwelling_types:
        for ber in ber_values:
            for bed in bedrooms:

                consecutive_empty = 0

                for floor in floors_to_use:

                    call_counter, new_rows = run_search(
                        dwelling,
                        ber,
                        bed,
                        floor,
                        save_match_score=0,
                        call_counter=call_counter,
                        all_results=all_results,
                        unique_result_keys=unique_result_keys
                    )

                    # If no new rows twice in a row, then break out of this inner loop and continue with the next number of bedroooms.
                    # This is to stop wasting calls with no return.  This is also why the floors to use are radial rather than simply incrementing.
                    if new_rows == 0:
                        consecutive_empty += 1
                    else:
                        consecutive_empty = 0

                    if consecutive_empty >= 2: # Why 2? Because sometimes one expansion gives no new results but next gives new results.
                        print("Stopping floor expansion for this combination — no new results in last two queries.\n")
                        break

# -------------------------
# FINAL SUMMARY AND OUTPUT TO CSV
# -------------------------

print("=================================")
print(f"Total API Calls: {call_counter}")
print(f"Unique Results: {len(all_results)}")
print("=================================")

# -------------------------
# Post-process all_results to add presumed Tenancy start and Tenancy Update by parsing out from the RT registration number
# -------------------------
processed_results = []

for row in all_results:
    rt_number = row[3]  # RT Number is column index 3
    tenancy_start = ""
    tenancy_update = ""

    # Split by dashes
    parts = rt_number.split("-")

    # Tenancy start: always from first part after first dash (MMYY)
    if len(parts) >= 2:
        start_part = parts[1]  # e.g., '0126'
        if len(start_part) == 4 and start_part.isdigit():
            month = start_part[:2]
            year = start_part[2:]
            tenancy_start = f"{month}/20{year}" # assume 21st century :)

        # Tenancy update: only if third dash exists and last 2 digits present
            if len(parts) >= 4:
                update_part = parts[3]  # e.g., '25' in RT-0918-01392489-25
                if len(update_part) == 2 and update_part.isdigit():
                    tenancy_update = "20" + update_part

    # Append new columns to row
    processed_results.append(row + [tenancy_start, tenancy_update])


# Write all unique results to CSV
filename = f"combined_results_{reference_eircode}.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Local Authority", "Local Electoral Area", "Dwelling Type", "RT Number",
        "Number of Bedrooms", "Number of Bed Spaces", "BER", "Rent (Month)",
        "Floor Space m2", "Match Score", "ED Name", "Tenancy Start", "Tenancy Updated"
    ])
    writer.writerows(processed_results)

print(f"Saved to {filename}\n")

# -------------------------
# THE END
# -------------------------n

# Record end time
end_time = time.time()

# Compute elapsed time
elapsed_seconds = end_time - start_time

# Format nicely in hours, minutes, seconds
hours, remainder = divmod(elapsed_seconds, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Total runtime: {int(hours)}h {int(minutes)}m {seconds:.2f}s\n")

input("Press Enter to close browser...") # Originally added for testing useful that the Chrome window doesn't disappear until you are ready to close it

driver.quit()
