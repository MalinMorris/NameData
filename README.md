# United States Name Data Trends

Every year the Social Security Administration releases the most popular names given to babies in the United States, with data dating back to 1880. The goal of this project is to create a simple way to search for a name's trend over time, as well as analyze other trends over the dataset.

## Credits
Data comes from the United States Social Security Administration (shorted to SSA) and the code was created by Malin Morris.

## SSA's Notes About the Name Data
- The SSA office opened in 1935, so names from before those years are not taken from birth certificates as they are now
- Names are separated into Male and Female based on the sex recorded at birth
- Names are limited to between 2 and 15 characters
- Only characters in the English alphabet are allowed, so no digits, apostraphes, hyphens or punctuation
- Additionally, the name Mary-Anne, Mary Anne, and Maryanne would all be recorded as Maryanne
- For privacy, only names with at least 5 occurences every year are recorded

## My Notes About the Name Data
- Name counts in previous years can be updated, presumably with children registered with Social Security outside their birth year, and so all name files are redownloaded on the Friday before Mother's Day release of the newest year of data
- If performing data preprocessing on the names themselves (i.e. extracting letters to create a machine learning model), ensure to handle the special case of the name Nan, which appeared only for girls, and is often interpreted as NAN, not a number