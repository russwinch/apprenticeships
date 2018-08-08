1 - Web scraping
===
a. All results from https://www.instituteforapprenticeships.org/apprenticeship-standards/ are
scraped and stored in the file step1a.json.

*The 'recommended training' field was excluded as there is only one apprenticeship that
used it*

To run: ```scrapy runspider scrape_ifa.py -o step1a.json```


b. All results from https://findapprenticeshiptraining.sfa.bis.gov.uk/Apprenticeship/SearchResults?Keywords=
are scraped and stored in the file ```step1b.json```

To run: ```scrapy runspider scrape_findapp.py -o step1b.json```

TODO:
- fix 'show more' in long lists of suitable_job_roles and qualifications
- should be combined into file 1 with a function to run both to json files
---

2 - Matching datasets
===
a. The two datasets are iterated over and matched on:
- a composite key comprised of the lowercase name and the number of the level
- the url on the Institiue for Apprenticeships site (some pages on the Find Apprenticeship
Training site have a link to the corresponding page on the IfA).

The url match is the more effective method, with the key matching just picking
up 1 additional apprenticeship. There were less matches than expected, it is advisable
to look into this further in case further data cleaning could yield more matches.

b. Matches from the two datasets are merged. The logic appends data from the second file
to the first file, with preference to the first file when the same fields exist in both.

To run both parts: ```python matching.py```

Files are saved as ```step2a.json``` and ```step2b.json```

---

3 - Summarise data
===
A summary of the dataset is available in the Jupyter notebook ```summarise.ipynb```

This covers the overall picture of the data and highlights some key fields,
showing the shape of the data and where there are missing values.

---

Additional
===
Some unit tests have been written for step2 and can be found in ```/tests``` but coverage is not complete.

Tests can be run with ```pytest``` from the root folder of the project.
