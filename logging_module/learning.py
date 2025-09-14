import logging

# logging.basicConfig(filename="my_log.log", encoding="utf-8", filemode="w")

# logging.debug("DEBUG")
# logging.info("INFO")
# logging.warning("WARNING")
# logging.error("ERROR")
# logging.critical("CRITICAL")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s [Line: %(lineno)d %(filename)s]",
)
x = 10 + 10
logging.info(f"The result is {x}")
