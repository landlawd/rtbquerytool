RTB Register Query Tool

Usage: python rtbscraper.py config_template

Note: You need just a little programming knowledge to use this script.  Just enough to install the runtime environment (python, selenium and chrome driver).

This python script takes a config file containing the details of a reference property (eircode, dwelling type, BER, bedroom number, and floor space) and the ranges you want to query for similar properties (multiple eircodes in same ED, dwelling types, BER ratings, numbers of bedrooms and range of floor space).

The output is a csv file.  The first 10 rows are the hits from the RTB Register for the reference property, including match score.  Subsequent rows are all further properties returned from querying the additional ranges.
Each property found is added only once (this is why further match scores are not included).
The Tenancy Start date and Year updated are parsed out of the RT Number, so they are only as accurate as the RT number suggests.

The latest version contains optimized logic to reduce the number of queries (break floor space loop when no new results)

Everything else is written in the code file header comments. 

Output data from large-scale test runs in the data folder.

Use at your own risk.
