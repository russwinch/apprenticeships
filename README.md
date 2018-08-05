1. Web scraping
===============
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
---

2. Matching datasets
====================
a. The two datasets are iterated over and matched on:
- a composite key comprised of the lowercase name and the number of the level
- the url on the Institiue for Apprenticeships site (some pages on the Find Apprenticeship Training site have
a link to the corresponding page on the IfA).

The url match is the more effective method, with the key matching just picking
up 1 more apprenticeship.

To run: ```python matching.py matchonly```
