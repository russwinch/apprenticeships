import scrapy


class IfaSpider(scrapy.Spider):
    """
    Spider for the apprenticeships on https://www.instituteforapprenticeships.org/
    """
    name = "ifa"
    start_urls = [
        'https://www.instituteforapprenticeships.org/apprenticeship-standards/'
        ]

    def parse(self, response):
        """
        Iterate over each link in the apprenticeship standard search results.
        """
        for standard in response.css('div.standard a'):
            yield response.follow(standard, self.parse_ifa_standard)

    def parse_ifa_standard(self, response):
        """
        Scrape and parse the detail page for each apprenticeship standard.

        With no ids in the css, divs with the detail class are iterated over to
        produce the keys and the following div is the value.
        """
        data = response.xpath('/html/body/main/div[2]/div/div[1]/div[2]/div[1]')

        standard = {}
        for detail in data.css('div.detail'):
            key = detail.css('span.heading::text').extract_first()
            value = detail.xpath('span[2]').css('::text').extract_first()
            if key:  # to exclude any null keys from empty spans
                standard[key] = value.strip()

        max_funding = standard.get('Maximum funding: ')
        if max_funding:
            max_funding = int(max_funding[1:])

        employers_involved = standard.get('Employers involved in creating the standard: ')
        if employers_involved:
            employers_involved = employers_involved.split(', ')

        level = standard.get('Level: ')
        if level:
            level = int(level)

        yield {
            'name': response.xpath('/html/body/main/div[1]/div/div/h1').css('::text').extract_first().strip(),
            'source': ['Institute for Apprenticeships'],
            'ifa_url': response.url,
            'reference_code': standard.get('Reference: '),
            'max_funding': max_funding,
            'employers_involved': employers_involved,
            'degree_type': standard.get('Degree: '),
            'approved_date': standard.get('Approved for delivery: '),
            'level': level,
            'version': standard.get('Version: '),
            'contact': standard.get('Trailblazer contact(s): '),
            'status': standard.get('Status: '),
            'data_updated': standard.get('Date updated: '),
            'length': standard.get('Typical duration: '),
            'route': standard.get('Route: '),
            }
