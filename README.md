Kiss Metrics Crawler
========================

A simple demo of Python's Scrapy Library


## Begin Scraping
`scrapy crawl kissmetrics > log/output.log`

Note: Adjust the max_pages variable in kissmetrics_spider.py as needed.

## Run analysis
`python analytics/analyze_titles.py`

This will output results into `analytics/output/`
