import twint
import nest_asyncio


nest_asyncio.apply()

c = twint.Config()

c.Search = 'dorathy'
c.Since = '2020-09-10 00:00:00'
c.Until = '2020-09-12 23:59:59'
c.Store_csv = True
c.Output = 'Scraped_tweets/dorathy.csv'

twint.run.Search(c)