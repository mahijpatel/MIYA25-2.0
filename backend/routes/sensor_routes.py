from flask import Blueprint, request

from models.sensor import SensorReading
from utils.response import ok

sensor_bp = Blueprint("sensors", __name__, url_prefix="/api")


@sensor_bp.route("/sensor-readings", methods=["GET"])
def list_sensor_readings():
    """Backs useSensorReadings()."""
    query = SensorReading.query
    sensor_type = request.args.get("sensor_type")
    if sensor_type:
        query = query.filter_by(sensor_type=sensor_type)
    readings = query.order_by(SensorReading.recorded_at.desc()).limit(200).all()
    return ok("Sensor readings fetched.", [r.to_dict() for r in readings])
