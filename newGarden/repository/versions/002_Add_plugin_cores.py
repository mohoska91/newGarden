from sqlalchemy.orm import Session

from model import TimedPluginCore, SensedPluginCore, Sensor, PluginCore, GardenTool

AIR = "air"
WATER = "water"
LIGHT = "light"

plugin_cores = [
    TimedPluginCore(
        id=1,
        requirement_name=LIGHT,
        tool=GardenTool(
            gpio=14,
            name="lamp"
        )
    ),
    TimedPluginCore(
        id=2,
        requirement_name=AIR,
        tool=GardenTool(
            gpio=3,
            name="fan"
        )
    ),
    SensedPluginCore(
        id=3,
        requirement_name=WATER,
        tool=GardenTool(
            gpio=7,
            name="pump"
        ),
        sensor=Sensor(
            name="Stemma",
            gpio=15
        )
    ),
]


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    session = Session(bind=migrate_engine)
    session.add_all(plugin_cores)
    session.commit()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    session = Session(bind=migrate_engine)
    for entity in session.query(PluginCore).all():
        session.delete(entity)
    session.commit()
