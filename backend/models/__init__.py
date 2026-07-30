from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SerializerMixin:
    """Gives every model a safe .to_dict() that never crashes on odd types."""

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            result[column.name] = value
        return result


# Import models so `db.create_all()` picks them up.
from models.user import User  # noqa: E402,F401
from models.tree import Tree  # noqa: E402,F401
from models.forest import ForestSite  # noqa: E402,F401
from models.carbon import CarbonLog  # noqa: E402,F401
from models.carbon_credit import CarbonCredit  # noqa: E402,F401
from models.emergency import EmergencyReport  # noqa: E402,F401
from models.pickup import Pickup  # noqa: E402,F401
from models.compost import CompostUnit  # noqa: E402,F401
from models.department import Department  # noqa: E402,F401
from models.drone import DroneMission  # noqa: E402,F401
from models.flood import FloodZone  # noqa: E402,F401
from models.heat import HeatZone  # noqa: E402,F401
from models.sensor import SensorReading  # noqa: E402,F401
from models.learning import LearningArticle  # noqa: E402,F401
from models.volunteer import Volunteer, VolunteerSignup  # noqa: E402,F401
from models.achievement import Achievement, UserAchievement  # noqa: E402,F401
from models.audit import AuditLog  # noqa: E402,F401
from models.reward import Reward, Badge, UserBadge, RedemptionHistory  # noqa: E402,F401
from models.notification import Notification  # noqa: E402,F401
from models.feedback import Feedback  # noqa: E402,F401
from models.complaint import Complaint  # noqa: E402,F401
