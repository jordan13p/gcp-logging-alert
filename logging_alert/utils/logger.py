import json

class StructuredLogger:
    component = "arbitrary-property"

    @staticmethod
    def log_error(error_message):
        entry = dict(
            severity="ERROR",
            message=error_message,
            component=StructuredLogger.component
        )
        print(json.dumps(entry))

    @staticmethod
    def log_info(info_message):
        entry = dict(
            severity="INFO",
            message=info_message,
            component=StructuredLogger.component
        )
        print(json.dumps(entry))
