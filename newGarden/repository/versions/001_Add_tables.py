from model import Base


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    Base.metadata.create_all(migrate_engine)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    Base.metadata.drop_all(migrate_engine)
