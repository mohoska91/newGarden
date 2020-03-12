from datetime import datetime

from sqlalchemy.orm import Session

from model import Plant, Lifeline, TimedRequirement, TimeInterval, SensedRequirement

plants = [
    Plant(
        name="PlantA",
        description="",
        lifelines=[
            Lifeline(
                name="growing",
                description="",
                requirements=[
                    TimedRequirement(
                        id="air",
                        time_intervals=[
                            TimeInterval(
                                start_time=datetime.strptime("09:00:00", "%H:%M:%S").time(),
                                end_time=datetime.strptime("09:00:10", "%H:%M:%S").time()
                            )
                        ]
                    ),
                    TimedRequirement(
                        id="light",
                        time_intervals=[
                            TimeInterval(
                                start_time=datetime.strptime("00:00:00", "%H:%M:%S").time(),
                                end_time=datetime.strptime("20:00:00", "%H:%M:%S").time()
                            )
                        ]
                    ),
                    SensedRequirement(
                        id="water",
                        min_value=600,
                        max_value=800
                    )
                ]
            )
        ]
    ),
]


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    session = Session(bind=migrate_engine)
    session.add_all(plants)
    session.commit()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    session = Session(bind=migrate_engine)
    for entity in session.query(Plant).all():
        session.delete(entity)
    session.commit()
