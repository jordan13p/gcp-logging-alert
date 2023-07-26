from flask import request, Blueprint
from ..utils.logger import StructuredLogger
from ..services.error_log_data import AlertMessage
from ..services.counts_data import CountsAlertMessage
from ..services.send_message import AlertSender


# Blueprint Configuration
logging_alert_bp = Blueprint("logging_alert_bp", __name__)


# health check
@logging_alert_bp.route("/healthz", methods=["GET"])
def healthz():
    StructuredLogger.log_info("Still alive...")
    return "{\"status\":\"ok\"}", 200


# all error log
@logging_alert_bp.route("/error_log", methods=["POST"])
def error_log():
    try:
        # pub/sub get data
        envelope = request.get_json()
        # StructuredLogger.log_info(envelope)
        
        # create AlertMessage object
        alert_message = AlertMessage(envelope)
        alert_message_data = alert_message.get_alert_message_data()
        # StructuredLogger.log_info(alert_message_data)

        # send message to telegram or discord
        send_message = AlertSender(alert_message_data)
        send_message.send_error_log_message()

        return "", 204

    except Exception as err:
        StructuredLogger.log_error(str(err))
        return "", 204


# counts error code
@logging_alert_bp.route("/counts", methods=["POST"])
def counts():
    try:
        # pub/sub get data
        envelope = request.get_json()
        # StructuredLogger.log_info(envelope)

        # create AlertMessage object
        counts_alert_message = CountsAlertMessage(envelope)
        alert_message_data = counts_alert_message.get_alert_message_data()
        # StructuredLogger.log_info(alert_message_data)

        # send message to telegram or discord
        send_message = AlertSender(alert_message_data)
        send_message.send_counts_log_message()

        return "", 204

    except Exception as err:
        StructuredLogger.log_error(str(err))
        return "", 204
