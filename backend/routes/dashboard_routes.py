from flask import Blueprint, g

from models.carbon import CarbonLog
from models.emergency import EmergencyReport
from models.notification import Notification
from models.tree import Tree
from models.user import User
from utils.decorators import optional_auth
from utils.response import ok

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")


@dashboard_bp.route("/dashboard/summary", methods=["GET"])
@optional_auth
def dashboard_summary():
    """Backs useDashboardKPIs() / the citizen home page summary cards."""
    total_trees = Tree.query.count()
    total_co2 = Tree.query.with_entities(Tree.co2_absorbed_kg).all()
    total_co2_kg = sum(v[0] or 0 for v in total_co2)
    total_citizens = User.query.filter_by(role="citizen").count()
    open_reports = EmergencyReport.query.filter(EmergencyReport.status != "resolved").count()

    user = g.get("current_user")
    my_points = 0
    if user:
        u = User.query.get(user["user_id"])
        my_points = u.points if u else 0

    return ok(
        "Dashboard summary fetched.",
        {
            "total_trees_tracked": total_trees,
            "total_co2_absorbed_kg": round(total_co2_kg, 1),
            "total_citizens": total_citizens,
            "open_emergency_reports": open_reports,
            "my_points": my_points,
            "city": "Bhavnagar",
        },
    )


@dashboard_bp.route("/dashboard/recent-activity", methods=["GET"])
@optional_auth
def recent_activity():
    """Recent activity feed for /citizen/activity."""
    activities = []

    for log in CarbonLog.query.order_by(CarbonLog.created_at.desc()).limit(5).all():
        activities.append(
            {
                "type": "carbon_log",
                "message": f"Logged a carbon footprint of {round(log.total_kg)} kg CO2e",
                "timestamp": log.created_at.isoformat(),
            }
        )

    for report in EmergencyReport.query.order_by(EmergencyReport.created_at.desc()).limit(5).all():
        activities.append(
            {
                "type": "emergency_report",
                "message": f"Reported: {report.title}",
                "timestamp": report.created_at.isoformat(),
            }
        )

    for tree in Tree.query.filter(Tree.adopted_at.isnot(None)).order_by(Tree.adopted_at.desc()).limit(5).all():
        activities.append(
            {
                "type": "tree_adopted",
                "message": f"Adopted a {tree.species} tree in {tree.location_name}",
                "timestamp": tree.adopted_at.isoformat() if tree.adopted_at else None,
            }
        )

    activities.sort(key=lambda a: a["timestamp"] or "", reverse=True)
    return ok("Recent activity fetched.", activities[:15])


@dashboard_bp.route("/dashboard/statistics", methods=["GET"])
def statistics():
    """City-wide statistics for gov/admin dashboards."""
    total_trees = Tree.query.count()
    healthy_trees = Tree.query.filter_by(health_status="healthy").count()
    total_reports = EmergencyReport.query.count()
    resolved_reports = EmergencyReport.query.filter_by(status="resolved").count()

    return ok(
        "Statistics fetched.",
        {
            "total_trees": total_trees,
            "healthy_trees_percent": round((healthy_trees / total_trees) * 100, 1) if total_trees else 0,
            "total_emergency_reports": total_reports,
            "resolved_emergency_reports": resolved_reports,
            "resolution_rate_percent": round((resolved_reports / total_reports) * 100, 1) if total_reports else 0,
        },
    )
