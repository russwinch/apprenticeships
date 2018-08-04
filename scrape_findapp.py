import scrapy


class FindAppSpider(scrapy.Spider):
    """
    Spider for the apprenticeships finder on https://findapprenticeshiptraining.sfa.bis.gov.uk/
    """
    name = "find_app"
    start_urls = [
        'https://findapprenticeshiptraining.sfa.bis.gov.uk/Apprenticeship/SearchResults?Keywords='
        ]
    custom_settings = {
            'DOWNLOAD_DELAY': 0.25  # seems to prevent 404s
            }

    def parse(self, response):
        """
        Iterate over each link in the apprenticeship standard search results.
        """
        for standard in response.css('article.result a'):
            yield response.follow(standard, self.parse_find_apprenticeships)

        next_page = response.css('div.page-navigation a.next::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_find_apprenticeships(self, response):
        """
        Scrape and parse the detail page for each apprenticeship.

        With ids in the css, the keys can be hardcoded and the values easily
        extracted. Assessment orgs are a special case with some apprenticeships
        having multiple.
        """
        def clean_extract(css):
            """
            Removes carrige returns, newlines and whitespace before
            concatenating the items in a list. Used on items scraped with
            extract().
            """
            clean_list = [e.strip() for e in css.extract() if e.strip()]
            return ' '.join(clean_list)

        data = response.css('dl.data-list')

        assessment_orgs = response.xpath('//*[@id="content"]/section/dl/dd[8]/details/table/tbody')
        if assessment_orgs:
            assessment = []
            for org in assessment_orgs:
                assessment.append({
                    'name': org.css('td.organisation-name a::text').extract_first(),
                    'url': org.css('td.organisation-name a::attr(href)').extract_first(),
                    'phone_number': org.css('td.phone-number::text').extract_first(),
                    'email': org.css('td.email a::text').extract_first()
                })
        else:
            assessment = data.css('dd#no-assessment-organisations p::text').extract_first()

        yield {
            'name': response.css('h1.heading-xlarge::text').extract_first().strip(),
            'level': data.css('dd#level *::text').extract_first(),
            'length': data.css('dd#length::text').extract_first(),
            'entry_requirements': clean_extract(data.css('dd#entry_requirements *::text')),
            'job-roles': clean_extract(data.css('dd.job-roles *::text')),
            'learnings': response.css('dd#will-learn li::text').extract(),
            'qualifications': clean_extract(data.css('*#qualifications *::text, *.qualifications *::text')),
            'professional_registration': data.css('dd#professional-registration *::text').extract_first(),
            'assessment': assessment,
            'ifa_url': data.css('dd#more-information a::attr(href)').extract_first()
        }
