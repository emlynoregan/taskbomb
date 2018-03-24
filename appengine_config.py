import logging
logging.info("Enter appengine_config.py")

from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')

logging.info("Leave appengine_config.py")
