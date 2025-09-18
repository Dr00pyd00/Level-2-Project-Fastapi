import logging
from pythonjsonlogger import jsonlogger

# Basic config:
logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
# create the instance used
logger = logging.getLogger('AppLogger')


#==== .log storage ====#

# create handler file
log_handler = logging.FileHandler('./logs.log')

# format

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

log_handler.setFormatter(formatter)

# add handler to the logger:
logger.addHandler(log_handler)



#==== JSON storage ====#

# create the handler file
log_handler_json = logging.FileHandler('./logs.json')

# JSON format:
formatter = jsonlogger.JsonFormatter( # type: ignore
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)

log_handler_json.setFormatter(formatter)

# add handler to the logger:
logger.addHandler(log_handler_json)



