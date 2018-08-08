import re
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
            'DOWNLOAD_DELAY': 0.4  # seems to help prevent 404s
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
        Scrape and parse the detail page for each apprenticeship standard.

        With ids in the css, the keys can be hardcoded and the values easily
        extracted. Assessment orgs are a special case with some apprenticeships
        having multiple.
        """
        def clean_extract(css, slicer=None, return_list=False):
            """
            Removes carrige returns, newlines and whitespace before
            concatenating the items in a list. Used on items scraped with
            extract().

            :css: the css object from Scrapy
            :slicer: a slice object to be applied before joining. Useful for cutting off
                default text
            :return_list: items are returned as a list
            """
            cleaned_list = [e.strip() for e in css.extract() if e.strip()]
            if slicer:
                cleaned_list = cleaned_list[slicer]
            if return_list:
                return cleaned_list
            return ' '.join(cleaned_list)

        data = response.css('dl.data-list')

        standard = {}
        assessment_orgs = response.xpath('//*[@id="content"]/section/dl/dd[8]/details/table/tbody')
        if assessment_orgs:  # sometimes there are contact details for orgs
            standard['endpoint_assessment'] = []
            for org in assessment_orgs:
                standard['endpoint_assessment'].append({
                    'name': org.css('td.organisation-name a::text').extract_first(),
                    'url': org.css('td.organisation-name a::attr(href)').extract_first(),
                    'phone_number': org.css('td.phone-number::text').extract_first(),
                    'email': org.css('td.email a::text').extract_first()
                })
        else:
            standard['endpoint_assessment'] = data.css('dd#no-assessment-organisations p::text').extract_first()

        max_funding = data.css('dd#funding-cap::text').extract_first()
        if max_funding:  # extract the amount and convert to an integer
            ref = re.compile('£(\d*),(\d*)')
            fund_match = ref.search(max_funding)
            max_funding = int(''.join(fund_match.groups()))
        standard['max_funding'] = max_funding

        level = data.css('dd#level *::text').extract_first()
        if level:  # extract the level and convert to an integer
            rel = re.compile('\d*')
            level_match = rel.match(level)
            level = int(level_match.group())
        standard['level'] = level

        standard['name'] = response.css('h1.heading-xlarge::text').extract_first().strip()
        standard['source'] = ['Find Apprenticeship Training']
        standard['length'] = data.css('dd#length::text').extract_first()
        standard['entry_requirements'] = clean_extract(data.css('dd#entry_requirements *::text'), slice(1, None))
        standard['suitable_job_roles'] = clean_extract(data.css('dd.job-roles *::text'), slice(-1), return_list=True)
        standard['expected_learnings'] = response.css('dd#will-learn li::text').extract()
        standard['qualifications'] = clean_extract(data.css('*#qualifications *::text, *.qualifications *::text'))
        standard['professional_registration'] = data.css('dd#professional-registration *::text').extract_first()
        standard['ifa_url'] = data.css('dd#more-information a::attr(href)').extract_first()

        # replace any empty strings with nulls in the final output
        for key, value in standard.items():
            value = value or None
            standard[key] = value

        yield standard
