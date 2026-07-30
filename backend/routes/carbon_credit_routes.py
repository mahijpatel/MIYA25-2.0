from flask import Blueprint

from models.carbon_credit import CarbonCredit
from utils.response import ok

carbon_credit_bp = Blueprint("carbon_credits", __name__, url_prefix="/api")


@carbon_credit_bp.route("/carbon-credits", methods=["GET"])
def list_carbon_credits():
    """Backs useCarbonCredits()."""
    credits = CarbonCredit.query.order_by(CarbonCredit.issued_on.desc()).all()
    total_issued = sum(c.credits_issued for c in credits)
    total_sold = sum(c.credits_sold for c in credits)
    return ok(
        "Carbon credits fetched.",
        {
            "projects": [c.to_dict() for c in credits],
            "summary": {
                "total_issued": total_issued,
                "total_sold": total_sold,
                "total_available": total_issued - total_sold,
            },
        },
    )
