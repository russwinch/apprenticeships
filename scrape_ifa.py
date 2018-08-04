import scrapy


class IfaSpider(scrapy.Spider):
    name = "ifa"
    start_urls = [
        'https://www.instituteforapprenticeships.org/apprenticeship-standards/'
    ]

    @staticmethod
    def _extract_by_xpath(response, xpath):
        """Helper to return text from a response using the xpath"""
        return response.xpath(xpath).css('::text').extract_first()

    def parse(self, response):
        for standard in response.css('div.standard a'):
            yield response.follow(standard, self.parse_ifa_standard)

    def parse_ifa_standard(self, response):
        """https://www.instituteforapprenticeships.org/"""
        data = response.xpath('/html/body/main/div[2]/div/div[1]/div[2]/div[1]')
        standard = {'Name': self._extract_by_xpath(response, '/html/body/main/div[1]/div/div/h1')}
        for detail in data.css('div.detail'):
            key = detail.css('span.heading::text').extract_first()
            value = detail.xpath('span[2]').css('::text').extract_first()
            if key:
                standard[key[:-2]] = value

        yield standard

    def parse_find_apprenticeships(self, response):
        """https://findapprenticeshiptraining.sfa.bis.gov.uk/"""
        name = response.xpath('//*[@id="content"]/div/div[1]/div/h1')
        data = response.css('da.data-list')
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
            'name': name.css('h1::text').extract_first().strip(),
            'level': data.css('dd#level p::text').extract_first(),
            'length': data.css('dd#length::text').extract_first(),
            'entry_requirements': ' '.join(data.css('dd#entry_requirements p::text').extract()),
            'learnings': response.css('dd#will-learn li::text').extract(),
            'qualifications': data.css('dd#qualifications li::text').extract(),
            'professional_registration': data.css('dd#professional-registration p::text').extract_first(),
            'assessment': assessment,
            'ifa_link': data.css('dd#more-information a::attr(href)').extract_first()
        }
