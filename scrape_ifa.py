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
        Scrape and parse the detail page for each apprenticeship.

        With no ids in the css, divs with the detail class are iterated over to
        produce the keys and the following div is the value.
        """
        data = response.xpath('/html/body/main/div[2]/div/div[1]/div[2]/div[1]')
        standard = {
                'name': response.xpath('/html/body/main/div[1]/div/div/h1').css('::text').extract_first().strip(),
                'ifa_url': response.url
                }
        for detail in data.css('div.detail'):
            key = detail.css('span.heading::text').extract_first()
            value = detail.xpath('span[2]').css('::text').extract_first()
            if key:  # to exclude any nulls
                standard[key[:-2].lower()] = value.strip()

        yield standard
