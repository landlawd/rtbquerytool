RTB Register Query Tool

Usage: python rtbscraper.py config_template

Note: You need just a little programming knowledge to use this script.  Just enough to install the runtime environment (python, selenium and chrome driver).

This python script takes a config file containing an Eircode, the details of a reference property (dwelling type, BER, bedroom number, and floor space) and the ranges you want to query for similar properties (dwelling types, BER ratings, numbers of bedrooms and range of floor space).

The output is a csv file.  The first 10 rows are the hits from the RTB Register for the reference property, including match score.  Subsequent rows are all further properties returned from querying the additional ranges.
Each property found is added only once (this is why further match scores are not included).
The Tenancy Start date and Year updated are parsed out of the RT Number, so they are only as accurate as the RT number suggests.

The code currently takes a brute force approach, looping through all the possibilities. This means a sharply declining number of new properties found on each search. This is not efficient in terms of the number of queries and the runtime it takes to run, so I am conidering optimizing it.

Everything else is written in the code file header comments. 

Use at your own risk.
