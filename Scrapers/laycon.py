import twint
import nest_asyncio


nest_asyncio.apply()

c = twint.Config()

c.Search = 'laycon'
c.Since = '2020-09-18 00:00:00'
c.Until = '2020-09-18 23:59:59'
c.Store_csv = True
c.Output = 'Scraped_tweets/laycon.csv'

twint.run.Search(c)