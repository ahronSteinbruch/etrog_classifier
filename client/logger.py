import logging
# from elasticsearch import Elasticsearch

import config


class Logger:
    _logger = None
    @classmethod
    def get_logger(cls, name=config.LOGGER_NAME, es_host=config.ES_HOST,
                   index="my_index_logs_name", level=logging.DEBUG):
        if cls._logger:
            return cls._logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            # es = Elasticsearch(es_host)
            # class ESHandler(logging.Handler):
                # def emit(self, record):
                    # try:
                        # es.index(index=index, document={
                        # "timestamp": datetime.utcnow().isoformat(),
                        #
                        # "level": record.levelname,
                        # "logger": record.name,
                        # "message": record.getMessage()
                        #
                        # })
                    # except Exception as e:
                    #     print(f"ES log failed: {e}")
            # logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())
            cls._logger = logger
            return logger