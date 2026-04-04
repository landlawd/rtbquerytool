RTB Register Query Tools

Note: You need just a little IT/programming knowledge to use thse script.  Just enough to install the runtime environment (python, selenium and chrome driver), edit a config file, and run the python script.

<b>Data analysis</b>

Analysis based on use of these tools can be found in the discussion thread on AskAboutMoney https://www.askaboutmoney.com/threads/rtb-rent-register.243258, notably the following posts:

<table>
  <tr>
    <td>Posts regarding data gathered<br>using rtbscraper tool</td>
    <td>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1987140
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1987143
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1987294
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1987309
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1987951
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1987990
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1987992
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1988010
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1988041
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1988702</td>
  </tr>
  <tr>
    <td>Posts regarding RTB register not returning <br>results as their page describes</td>
    <td> https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1988668
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1988702</td>
  </tr>
  <tr>
    <td>Posts with analysis of rent distribution<br> in various surveyed areas</td>
    <td>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1989805
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1989809
    <br>https://www.askaboutmoney.com/threads/rtb-rent-register.243258/post-1989871
    </td>
  </tr>
</table>

<b>RTB Query Tool</b>
<p>
Usage: python rtbscraper.py &lt;config_file, see config_template.py&gt;
<br>Example: python rtbscraper.py config_dublin8_ed
<br>Output: csv file containing all found matching properties

This python script takes a config file containing the details of a reference property (eircode, dwelling type, BER, bedroom number, and floor space) and the ranges you want to query for similar properties (multiple eircodes in same ED, dwelling types, BER ratings, numbers of bedrooms and range of floor space).

The output is a csv file.  The first 10 rows are the hits from the RTB Register for the reference property, including match score.  Subsequent rows are all further properties returned from querying the additional ranges.
Each property found is added only once (this is why further match scores are not included).
The Tenancy Start date and Year updated are parsed out of the RT Number, so they are only as accurate as the RT number suggests.

The latest version contains optimized logic to reduce the number of queries (break floor space loop when no new results)

Everything else is written in the code file header comments. 

Output data from large-scale test runs are stored in the data folder.

Use at your own risk.

<b>RTB Matchfinder tool</b>
<p>
Usage: python matchfinder.py  &lt;config_file&gt;
<br>Example: python matchfinder.py matchfinder_testdata_pembroke.py
<br>Output: csv file containing 10 best matches following the advertised RTB algorithm, e.g. comparables_Pembroke.csv

This python script takes an already scraped data set and simulates the RTB algorithm as described on their webpage to find 10 matching properties (https://rtb.ie/rtb-rent-register/).

Note that the RTB rent register tool itself does not correctly follow their own algorithm as described, so the results of this matchfinder tool will not actually match the RTB rent register inself.
It seems the RTB rent register query tool also considers proximity to the reference property address, perhaps the electoral subdivision is used for this, and it does not sort as described.
