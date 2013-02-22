#Scrapy settings for angellist project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'angellist'

SPIDER_MODULES = ['angellist.spiders']
NEWSPIDER_MODULE = 'angellist.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'
LOG_FILE = 'crawl.log'
DOWNLOAD_DELAY = 0.25
FEED_URI = 'file:///angelStartup.json'
FEED_FORMAT = 'json'


