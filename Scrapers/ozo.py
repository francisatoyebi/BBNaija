import twint
import nest_asyncio


nest_asyncio.apply()

c = twint.Config()

c.Search = 'ozo'
c.Since = '2020-09-11'
c.Until = '2020-09-12'
c.Store_csv = True
c.Output = 'Scraped_tweets/ozo.csv'

twint.run.Search(c)