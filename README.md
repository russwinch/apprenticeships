1. Web scraping
---
a. All results from https://www.instituteforapprenticeships.org/apprenticeship-standards/ are
scraped and stored in the file step1a.json

To run: ```scrapy runspider scrape_ifa.py -o step1a.json```
TODO: 
- employers should be split to an array
- max-funding needs encoding fixed on the £ sign
- keys need renaming to match the other file


b. All results from https://findapprenticeshiptraining.sfa.bis.gov.uk/Apprenticeship/SearchResults?Keywords=
are scraped and stored in the file ```step1b.json```

To run: ```scrapy runspider scrape_finda.py -o step1b.json```
TODO:
- should be combined into file 1 with a function to run both to json files
