from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()


class Tool(Base, SerializerMixin):
    __tablename__ = "tool"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    gpio = Column(Integer, nullable=False)
    tool_type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'tool',
        'polymorphic_on': tool_type
    }


class GardenTool(Tool, SerializerMixin):
    __tablename__ = "garden_tool"

    __mapper_args__ = {
        'polymorphic_identity': 'garden_tool',
    }

    id = Column(Integer, ForeignKey("tool.id"), primary_key=True)
    plugin_core_id = Column(Integer, ForeignKey("plugin_core.id"), name="pcid", unique=True)


class Sensor(Tool, SerializerMixin):
    __tablename__ = "sensor"

    __mapper_args__ = {
        'polymorphic_identity': 'sensor',
    }

    id = Column(Integer, ForeignKey("tool.id"), primary_key=True)
    plugin_core_id = Column(Integer, ForeignKey("plugin_core.id"), name="pcid", unique=True)


class PluginCore(Base, SerializerMixin):
    __tablename__ = "plugin_core"

    id = Column(Integer, primary_key=True)
    requirement_name = Column(String, nullable=False)
    plugin_core_type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'plugin_core',
        'polymorphic_on': plugin_core_type
    }


class TimedPluginCore(PluginCore):
    __mapper_args__ = {
        'polymorphic_identity': 'timed_plugin_core',
    }
    tool = relationship("GardenTool", cascade="all, delete-orphan", uselist=False)


class SensedPluginCore(PluginCore):
    __mapper_args__ = {
        'polymorphic_identity': 'sensed_plugin_core',
    }
    tool = relationship("GardenTool", cascade="all, delete-orphan", uselist=False)
    sensor = relationship("Sensor", cascade="all, delete-orphan", uselist=False)


class Plant(Base, SerializerMixin):
    __tablename__ = "plant"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    lifelines = relationship("Lifeline", cascade="all, delete-orphan")


class Lifeline(Base, SerializerMixin):
    __tablename__ = "lifeline"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    plant_id = Column(Integer, ForeignKey("plant.id"), name="pid")
    requirements = relationship("Requirement", cascade="all, delete-orphan")


class Requirement(Base, SerializerMixin):
    __tablename__ = "requirement"

    id = Column(String, primary_key=True)
    lifeline_id = Column(Integer, ForeignKey("lifeline.id"), name="lid")
    requirement_type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'requirement',
        'polymorphic_on': requirement_type
    }


class TimedRequirement(Requirement):
    __mapper_args__ = {
        'polymorphic_identity': 'timed_requirement',
    }

    time_intervals = relationship("TimeInterval", cascade="all, delete-orphan")


class SensedRequirement(Requirement):
    __tablename__ = "sensed_requirement"
    __mapper_args__ = {
        'polymorphic_identity': 'sensed_requirement',
    }

    id = Column(String, ForeignKey('requirement.id'), primary_key=True)
    min_value = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)


class TimeInterval(Base, SerializerMixin):
    __tablename__ = "time_interval"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    requirement_id = Column(String, ForeignKey("requirement.id"), name="rid")
