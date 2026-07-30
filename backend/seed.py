"""
Seeds the SQLite database with lightweight demo data so every page in the
frontend has something real to display the moment the backend starts.

Called automatically by app.py the first time the database is empty.
Can also be run directly:  python seed.py
"""

from datetime import datetime, timedelta


def run_seed(db):
    from models.achievement import Achievement, UserAchievement
    from models.audit import AuditLog
    from models.carbon import CarbonLog
    from models.carbon_credit import CarbonCredit
    from models.compost import CompostUnit
    from models.department import Department
    from models.drone import DroneMission
    from models.emergency import EmergencyReport
    from models.flood import FloodZone
    from models.forest import ForestSite
    from models.heat import HeatZone
    from models.learning import LearningArticle
    from models.notification import Notification
    from models.pickup import Pickup
    from models.reward import Badge, Reward
    from models.sensor import SensorReading
    from models.tree import Tree
    from models.user import User
    from models.volunteer import Volunteer

    now = datetime.utcnow()

    # ---------------------------------------------------------------
    # Users (one demo account per role)
    # ---------------------------------------------------------------
    citizen = User(name="Aarav Shah", email="citizen@miya25.test", role="citizen",
                   phone="9998887771", city="Bhavnagar", points=420, level="Grove Guardian")
    citizen.set_password("Citizen@123")

    gov = User(name="Priya Mehta", email="gov@miya25.test", role="gov",
               phone="9998887772", city="Bhavnagar", points=0, level="Officer")
    gov.set_password("Gov@123")

    admin = User(name="System Admin", email="admin@miya25.test", role="admin",
                 phone="9998887773", city="Bhavnagar", points=0, level="Administrator")
    admin.set_password("Admin@123")

    extra_citizens = [
        User(name="Kavya Patel", email="kavya@miya25.test", role="citizen", city="Bhavnagar", points=610, level="Forest Champion"),
        User(name="Rohan Joshi", email="rohan@miya25.test", role="citizen", city="Bhavnagar", points=310, level="Grove Guardian"),
        User(name="Meera Rana", email="meera@miya25.test", role="citizen", city="Bhavnagar", points=185, level="Sapling"),
    ]
    for u in extra_citizens:
        u.set_password("Citizen@123")

    db.session.add_all([citizen, gov, admin, *extra_citizens])
    db.session.commit()

    # ---------------------------------------------------------------
    # Forest sites (Bhavnagar area)
    # ---------------------------------------------------------------
    forests = [
        ForestSite(name="Victoria Park Urban Forest", latitude=21.7580, longitude=72.1435,
                   area_hectares=8.2, tree_count=1450, canopy_cover_percent=55, status="active",
                   description="A well-established urban forest patch inside Victoria Park, Bhavnagar."),
        ForestSite(name="Ghogha Road Green Belt", latitude=21.7830, longitude=72.1560,
                   area_hectares=6.5, tree_count=4200, canopy_cover_percent=38, status="active",
                   description="A young avenue plantation belt along Ghogha Road."),
        ForestSite(name="Velavadar Buffer Grassland", latitude=21.8371, longitude=72.0128,
                   area_hectares=340.0, tree_count=9800, canopy_cover_percent=22, status="restored",
                   description="Buffer grassland near Velavadar Blackbuck National Park."),
    ]
    db.session.add_all(forests)
    db.session.commit()

    # ---------------------------------------------------------------
    # Trees
    # ---------------------------------------------------------------
    species_pool = ["Neem", "Peepal", "Banyan", "Tamarind", "Gulmohar", "Mango", "Amla"]
    trees = []
    for i in range(30):
        trees.append(
            Tree(
                species=species_pool[i % len(species_pool)],
                common_name=species_pool[i % len(species_pool)],
                latitude=21.75 + (i % 10) * 0.004,
                longitude=72.14 + (i % 7) * 0.004,
                location_name="Bhavnagar",
                health_status=["healthy", "healthy", "healthy", "stressed"][i % 4],
                height_m=round(1.0 + (i % 12) * 0.6, 1),
                age_years=round(0.5 + (i % 12) * 0.8, 1),
                co2_absorbed_kg=round(8 + (i % 12) * 3.5, 1),
                forest_site_id=forests[i % len(forests)].id,
                planted_on=now - timedelta(days=30 * (i % 12)),
            )
        )
    # A couple already adopted, to demo the adopt-tree flow having history
    trees[0].adopted_by_user_id = citizen.id
    trees[0].adopted_at = now - timedelta(days=10)
    trees[3].adopted_by_user_id = extra_citizens[0].id
    trees[3].adopted_at = now - timedelta(days=25)

    db.session.add_all(trees)
    db.session.commit()

    # ---------------------------------------------------------------
    # Carbon logs, carbon credits
    # ---------------------------------------------------------------
    db.session.add_all([
        CarbonLog(user_id=citizen.id, transport_kg=520, electricity_kg=980, diet_kg=1900,
                   waste_kg=250, total_kg=3650, diet_type="mixed"),
        CarbonLog(user_id=extra_citizens[0].id, transport_kg=310, electricity_kg=760, diet_kg=1100,
                   waste_kg=200, total_kg=2370, diet_type="veg"),
    ])
    db.session.add_all([
        CarbonCredit(project_name="Victoria Park Urban Forest Credits", forest_site_id=forests[0].id,
                     credits_issued=1200, credits_sold=450, price_per_credit_inr=850, status="verified"),
        CarbonCredit(project_name="Ghogha Road Green Belt Credits", forest_site_id=forests[1].id,
                     credits_issued=800, credits_sold=120, price_per_credit_inr=820, status="verified"),
        CarbonCredit(project_name="Velavadar Buffer Grassland Credits", forest_site_id=forests[2].id,
                     credits_issued=3000, credits_sold=3000, price_per_credit_inr=900, status="sold"),
    ])
    db.session.commit()

    # ---------------------------------------------------------------
    # Emergency reports, complaints-adjacent pickups, compost units
    # ---------------------------------------------------------------
    db.session.add_all([
        EmergencyReport(user_id=citizen.id, category="illegal-cutting", title="Trees being cut near Ghogha Road",
                         description="Saw 3 trees cut down overnight near the green belt.",
                         latitude=21.783, longitude=72.156, location_name="Ghogha Road, Bhavnagar",
                         severity="high", status="acknowledged"),
        EmergencyReport(user_id=extra_citizens[1].id, category="fire", title="Small grass fire near Velavadar buffer",
                         description="Smoke visible from the highway, seems contained.",
                         latitude=21.83, longitude=72.02, location_name="Velavadar, Bhavnagar",
                         severity="medium", status="in-progress"),
    ])
    db.session.add_all([
        Pickup(user_id=citizen.id, waste_type="organic", quantity_kg=4.5, address="Kaliyabid, Bhavnagar",
               scheduled_date=now + timedelta(days=2), status="scheduled"),
        Pickup(user_id=extra_citizens[0].id, waste_type="e-waste", quantity_kg=2.0, address="Vidyanagar, Bhavnagar",
               scheduled_date=now - timedelta(days=3), status="collected"),
    ])
    db.session.add_all([
        CompostUnit(name="Kaliyabid Community Compost Unit", location_name="Kaliyabid, Bhavnagar",
                    latitude=21.7695, longitude=72.1435, capacity_kg=500, current_load_kg=210),
        CompostUnit(name="Vidyanagar Ward Compost Unit", location_name="Vidyanagar, Bhavnagar",
                    latitude=21.7552, longitude=72.1418, capacity_kg=350, current_load_kg=90),
    ])
    db.session.commit()

    # ---------------------------------------------------------------
    # Gov monitoring: departments, drones, flood/heat zones, sensors
    # ---------------------------------------------------------------
    db.session.add_all([
        Department(name="Bhavnagar Forest Department", head_name="R. K. Solanki",
                   contact_email="forest.dept@bhavnagar.gov.in", contact_phone="0278-2426501",
                   staff_count=42, budget_inr=8500000,
                   description="Manages afforestation, forest health and wildlife protection in Bhavnagar district."),
        Department(name="Bhavnagar Municipal Corporation - Environment Cell", head_name="S. Bhatt",
                   contact_email="environment@bmc.bhavnagar.gov.in", contact_phone="0278-2519540",
                   staff_count=28, budget_inr=6200000,
                   description="Handles urban greening, waste management and environmental compliance."),
        Department(name="Disaster Management Cell, Bhavnagar", head_name="A. Chauhan",
                   contact_email="dm-cell@bhavnagar.gov.in", contact_phone="1077",
                   staff_count=18, budget_inr=4100000,
                   description="Coordinates flood, fire and emergency response across the district."),
    ])
    db.session.add_all([
        DroneMission(mission_name="Canopy Health Survey - Victoria Park", forest_site_id=forests[0].id,
                     pilot_name="Vikram Rathod", status="completed", area_covered_hectares=8.2,
                     findings="No major canopy stress detected; minor pest activity on 4 trees.",
                     scheduled_at=now - timedelta(days=5)),
        DroneMission(mission_name="Illegal Cutting Patrol - Ghogha Belt", forest_site_id=forests[1].id,
                     pilot_name="Vikram Rathod", status="scheduled", area_covered_hectares=6.5,
                     findings="", scheduled_at=now + timedelta(days=2)),
    ])
    db.session.add_all([
        FloodZone(zone_name="Ghogha Circle Low-lying Area", latitude=21.774, longitude=72.148,
                  risk_level="moderate", water_level_m=0.4, population_at_risk=1200,
                  last_updated=now.isoformat()),
        FloodZone(zone_name="Coastal Belt near Alang", latitude=21.416, longitude=72.193,
                  risk_level="high", water_level_m=0.9, population_at_risk=3400,
                  last_updated=now.isoformat()),
    ])
    db.session.add_all([
        HeatZone(zone_name="Central Market Zone", latitude=21.768, longitude=72.150,
                 surface_temp_c=41.5, heat_risk="high", green_cover_percent=8),
        HeatZone(zone_name="Waghawadi Industrial Area", latitude=21.760, longitude=72.161,
                 surface_temp_c=43.2, heat_risk="extreme", green_cover_percent=5),
    ])
    sensors = []
    for i in range(10):
        sensors.append(
            SensorReading(
                sensor_code=f"BVN-SNS-{100+i}",
                sensor_type=["soil-moisture", "temperature", "humidity", "aqi"][i % 4],
                forest_site_id=forests[i % len(forests)].id,
                value=round(20 + i * 3.3, 1),
                unit=["%", "°C", "%", "AQI"][i % 4],
                battery_percent=round(60 + i * 3.5, 1),
                status="online" if i % 5 != 0 else "low-battery",
                recorded_at=now - timedelta(hours=i),
            )
        )
    db.session.add_all(sensors)
    db.session.commit()

    # ---------------------------------------------------------------
    # Learning articles, volunteer opportunities
    # ---------------------------------------------------------------
    db.session.add_all([
        LearningArticle(title="Why Urban Forests Matter for Bhavnagar", category="forests",
                         summary="How urban tree cover reduces heat and improves air quality in coastal cities.",
                         content="Urban forests like Victoria Park help Bhavnagar cool down, absorb carbon and support birdlife...",
                         read_minutes=4),
        LearningArticle(title="Composting at Home: A Beginner's Guide", category="waste",
                         summary="Turn kitchen waste into nutrient-rich compost in a few simple steps.",
                         content="Composting reduces landfill waste and creates rich soil for your garden...",
                         read_minutes=3),
        LearningArticle(title="Understanding Bhavnagar's Air Quality Index", category="air-quality",
                         summary="What AQI numbers mean and how to protect yourself on high-pollution days.",
                         content="The Air Quality Index (AQI) is a standardized way to communicate pollution levels...",
                         read_minutes=5),
    ])

    # ---------------------------------------------------------------
    # Medicinal plant learning articles (from Medicinal_Plants_Details.docx)
    # Each one has a real photo + a traditional-use description so the
    # Learning Centre can showcase them as photo cards.
    # ---------------------------------------------------------------
    SAFETY_NOTE = (
        "These are traditional uses. Serious illness, poisoning, severe bleeding, "
        "breathing difficulty, fractures, or major burns require professional medical care."
    )

    medicinal_plant_articles = [
        dict(title="Amla (Indian Gooseberry)", image="amla.jpg", category_label="Tree",
             medicinal_use="Rich in Vitamin C; supports immunity and digestion.",
             emergency_use="Eat fresh fruit or drink fresh juice to help with dehydration recovery and general weakness. Not a substitute for emergency care."),
        dict(title="Ashoka", image="ashoka.jpg", category_label="Tree",
             medicinal_use="Traditionally used in Ayurveda for women's health.",
             emergency_use="Not typically used as first aid. Seek medical care for emergencies."),
        dict(title="Aspilia africana", image="aspilia-africana.jpg", category_label="Herb",
             medicinal_use="Traditionally used for wound care.",
             emergency_use="Clean the wound with safe water, then fresh crushed leaves have been traditionally applied to minor cuts. Medical evaluation is recommended."),
        dict(title="Banyan", image="banyan.jpg", category_label="Tree",
             medicinal_use="Latex and bark used traditionally.",
             emergency_use="Latex has been traditionally applied to minor cuts; use only after cleaning the wound."),
        dict(title="Gulmohar", image="gulmohar.jpg", category_label="Tree",
             medicinal_use="Mostly ornamental; limited traditional medicinal use.",
             emergency_use="Not recommended for emergency self-treatment."),
        dict(title="Shepherd's Purse", image="shepherds-purse.jpg", category_label="Herb",
             medicinal_use="Traditionally associated with reducing minor bleeding.",
             emergency_use="Fresh aerial parts have traditionally been used on small cuts. Persistent bleeding requires urgent care."),
        dict(title="Tulsi (Holy Basil)", image="tulsi.jpg", category_label="Herb",
             medicinal_use="Helps with cough, cold and sore throat.",
             emergency_use="Chew washed leaves or prepare a warm infusion for mild cough/cold symptoms."),
        dict(title="White Yarrow (Achillea millefolium)", image="white-yarrow.jpg", category_label="Herb",
             medicinal_use="Traditionally used for minor wounds.",
             emergency_use="Clean wound then apply crushed clean leaves to minor cuts only."),
        dict(title="Witch Hazel", image="witch-hazel.jpg", category_label="Shrub",
             medicinal_use="Astringent; relieves skin irritation.",
             emergency_use="Commercial witch hazel extract can soothe minor insect bites or skin irritation."),
        dict(title="Yellow Yarrow", image="yellow-yarrow.jpg", category_label="Herb",
             medicinal_use="Similar uses to white yarrow.",
             emergency_use="Traditionally used on minor cuts after cleaning."),
    ]

    db.session.add_all([
        LearningArticle(
            title=p["title"],
            category="medicinal-plants",
            summary=p["medicinal_use"],
            content=(
                f"Category: {p['category_label']}\n\n"
                f"Medicinal Use: {p['medicinal_use']}\n\n"
                f"Emergency Use: {p['emergency_use']}\n\n"
                f"Note: {SAFETY_NOTE}"
            ),
            read_minutes=2,
            image_url=f"/static/plant_photos/{p['image']}",
        )
        for p in medicinal_plant_articles
    ])
    db.session.add_all([
        Volunteer(title="Weekend Tree Plantation Drive - Ghogha Road", organizer="Green Bhavnagar Foundation",
                  location_name="Ghogha Road, Bhavnagar", date=now + timedelta(days=6),
                  slots_total=40, slots_filled=18, category="tree-plantation",
                  description="Help plant 500 saplings along the Ghogha Road green belt."),
        Volunteer(title="Victoria Park Cleanup Drive", organizer="Bhavnagar Nature Club",
                  location_name="Victoria Park, Bhavnagar", date=now + timedelta(days=3),
                  slots_total=25, slots_filled=25, category="cleanup",
                  description="A morning cleanup and awareness walk through Victoria Park."),
    ])
    db.session.commit()

    # ---------------------------------------------------------------
    # Achievements, badges, rewards
    # ---------------------------------------------------------------
    achievements = [
        Achievement(title="First Tree Adopted", description="Adopted your first tree.", icon="tree-deciduous",
                    points_reward=50, category="trees"),
        Achievement(title="Carbon Conscious", description="Logged your carbon footprint for the first time.",
                    icon="leaf", points_reward=30, category="carbon"),
        Achievement(title="Community Reporter", description="Submitted your first emergency report.",
                    icon="alert-triangle", points_reward=40, category="emergency"),
        Achievement(title="Green Volunteer", description="Signed up for a volunteering drive.",
                    icon="hand-heart", points_reward=35, category="volunteer"),
    ]
    db.session.add_all(achievements)
    db.session.commit()

    db.session.add(UserAchievement(user_id=citizen.id, achievement_id=achievements[0].id))
    db.session.add(UserAchievement(user_id=citizen.id, achievement_id=achievements[1].id))

    db.session.add_all([
        Badge(title="Seedling", description="Just getting started on your green journey.", icon="sprout",
              points_required=0),
        Badge(title="Grove Guardian", description="Consistently contributing to Bhavnagar's green cover.",
              icon="shield", points_required=300),
        Badge(title="Forest Champion", description="A top contributor to the city's environmental goals.",
              icon="trophy", points_required=600),
    ])
    db.session.add_all([
        Reward(title="₹100 Grocery Voucher", description="Redeemable at partner grocery stores in Bhavnagar.",
               cost_points=200, category="voucher", stock=50),
        Reward(title="Reusable Cotton Tote Bag", description="An eco-friendly MIYA25-branded tote bag.",
               cost_points=100, category="merchandise", stock=100),
        Reward(title="Tree Adoption Certificate", description="A personalized certificate for a tree you've adopted.",
               cost_points=50, category="certificate", stock=200),
        Reward(title="₹500 Eco-Store Voucher", description="Redeemable at Bhavnagar eco-friendly product stores.",
               cost_points=800, category="voucher", stock=20),
    ])
    db.session.commit()

    # ---------------------------------------------------------------
    # Notifications
    # ---------------------------------------------------------------
    db.session.add_all([
        Notification(user_id=citizen.id, title="Welcome to MIYA25!",
                     message="Thanks for joining Bhavnagar's green citizen network.", category="general"),
        Notification(user_id=citizen.id, title="Tree Adopted", message="You successfully adopted a Neem tree.",
                     category="reward"),
        Notification(user_id=None, title="Heat Advisory - Bhavnagar", message="Temperatures may cross 40°C this week. Stay hydrated.",
                     category="emergency"),
    ])
    db.session.add(
        AuditLog(user_id=admin.id, actor_name=admin.name, action="Seeded initial demo data",
                 resource="database", ip_address="127.0.0.1")
    )
    db.session.commit()


if __name__ == "__main__":
    # Allows `python seed.py` to be run standalone against an existing app context.
    from app import app
    from models import db as _db

    with app.app_context():
        run_seed(_db)
        print("Seed data inserted.")
