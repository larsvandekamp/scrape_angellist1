# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AngelStartItem(Item):
	
	CompanyName = Field()
	HighConcept = Field()
	item_link = Field()
	item_tag = Field()
	product = Field()
	founders = Field()
	investors = Field()
	referer = Field()
	advisors = Field()
	team = Field()
