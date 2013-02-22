from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy import log
from angellist.items import  AngelStartItem
import re
from scrapy.selector import HtmlXPathSelector

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

reLink = re.compile(r'href="(.*?)".*?class="(.*?)"')


class Startup(BaseSpider):
	name = 'startup'

	def start_requests(self):
		for page in range(1, 162):
			yield Request('https://angel.co/startups?tab=startups&page=%d&per_page=16&skip_loading=true&include_ids='%page, callback = self.startList_parse)	



	def startList_parse(self, response):
			sel = HtmlXPathSelector(response)
			links = sel.select('//div[@class="name"]/a/@href').extract()
			for link in links:
				yield Request(link, callback=self.startup_parse)

	def startup_parse(self, response):
		print(response.url)
		item = AngelStartItem()
		sel = HtmlXPathSelector(response)
		startup = sel.select('//div[@class=" ds2 startups fpr47 profile_startup_header _a"]')
		item['CompanyName'] = CompanyName = startup.select('.//div[@class="name"]/span/text()')[0].extract()

		item['HighConcept'] = HighConcept = startup.select('.//div[@class="high_concept"]/p/text()')[0].extract()
		
		Links = startup.select('.//div[@class="links"]//a').extract()
		item['item_link'] = item_link = {}
		for link in Links:
			address, type_a = reLink.search(link).group(1, 2)
			item_link[type_a] = address

		Tags = startup.select('.//div[@class="tag"]/a').extract()
		item['item_tag'] = item_tag = {}
		for tag in Tags:
			address, address_tag = reLink.search(tag).group(1, 2)
			item_tag[address_tag] = address


		item['product'] = sel.select('//div[@class="section content"]//p/text()')[0].extract()
	

		#founders
		founders = sel.select('//div[@class="g-module no_shadow profile_section endorsers founder dsr31 startup_roles fgp57 group _a"]//li[@class="role_information g-feed_item dsr31 startup_roles fsw49 show _a"]')
		item_founder = item['founders'] = {}
		for line in founders:
			name, address, pitch = self.set_person(line)
			item_founder[name] = {'address': address, 'pitch': pitch}


		investors = sel.select('//div[@id="past_investors_section"]//li[@class="role_information g-feed_item dsr31 startup_roles fsw49 show _a"]')
		item_investor = item['investors'] = {}
		for line in investors:
			name, address, pitch = self.set_person(line)
			item_investor[name] = {'address': address, 'pitch': pitch}

			


		advisors = sel.select('//div[@id="advisors_section"]//li[@class="role_information g-feed_item dsr31 startup_roles fsw49 show _a"]')
		item_advisor = item['advisors'] = {}

		for line in advisors:
			name, address, pitch = self.set_person(line)
			item_advisor[name] = {'address': address, 'pitch': pitch}



		employees = sel.select('//div[@id="employees_section"]//li[@class="role_information g-feed_item dsr31 startup_roles fsw49 show _a"]')
		item_employ = item['team'] = {}

		for line in employees:
			name, address, pitch = self.set_person(line)
			item_employ[name] = {'address': address, 'pitch': pitch}

		referrers  = sel.select('//div[@id="referrers_section"]//li[@class="role_information g-feed_item dsr31 startup_roles fsw49 show _a"]')
		item_ref = item['referer'] = {}
		for line in referrers:
			name, address, pitch = self.set_person(line)
			item_ref[name] = {'address': address, 'pitch': pitch}


		yield item	

	def set_person(self, person):
			try:	
				name = person.select('.//div[@class="name"]/a/text()')[0].extract()
			except IndexError:
				name = person.select('.//div[@class="name"]/text()')[0].extract()
			try:	
				address = person.select('.//div[@class="name"]/a/@href')[0].extract()
			except IndexError:
				address = ''


			try:
				pitch = person.select('.//div[@class="pitch"]/*')[0].extract()
			except IndexError:
				pitch = person.select('.//div[@class="pitch"]/text()')[0].extract()

			return name, address, pitch
			
