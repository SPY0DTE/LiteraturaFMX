import nasdaqdatalink
import logging
NASDAQ_DATA_LINK_API_KEY="JYgHyx4az6Eo1Z2x81Ft"
logging.basicConfig()
data_link_log = logging.getLogger(NASDAQ_DATA_LINK_API_KEY)
data_link_log.setLevel(logging.DEBUG)

data = nasdaqdatalink.get_table('ZACKS/FC', ticker='AAPL')