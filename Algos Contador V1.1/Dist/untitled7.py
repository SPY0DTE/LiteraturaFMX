import nasdaqdatalink
import logging

logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)  # optionally set level for
everything.  Useful to see dependency debug info as well.

data_link_log = logging.getLogger("nasdaqdatalink")
data_link_log.setLevel(logging.DEBUG)