import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as EnumColumn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Frequency(Enum):
    """An enumeration representing the frequency at which a habit is performed.

        Attributes:
            DAILY (str): The habit is performed daily.
            WEEKLY (str): The habit is performed weekly.
    """
    DAILY = 'daily'
    WEEKLY = 'weekly'


class Habit(Base):
    """
    A class representing a habit in the application.

    Attributes:
        id (int): The unique identifier for the habit.
        task (str): The description of the habit's task.
        frequency (Frequency): The frequency at which the habit is performed, either daily or weekly.
        checkpoints (List[Checkpoint]): The checkpoints associated with the habit, specifying the date.

    """

    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    frequency = Column(EnumColumn(Frequency))
    # checkpoints = relationship("Checkpoint", backref="habit", cascade="all, delete-orphan")
    # checkpoint class has the habit attribute that refers to the Habit object
    # delete checkpoints when habit is deleted, and also all orphaned checkpoints if any
    # the Habit class can access the associated Checkpoint objects through the checkpoints attribute,
    # and vice versa.It allows for convenient querying and
    # manipulation of related data between Habit and Checkpoint objects.
    checkpoints = relationship("Checkpoint", back_populates="habit", cascade="all, delete-orphan")


class Checkpoint(Base):
    """A class representing a checkpoint for a habit.

        Attributes:
            id (int): The unique identifier for the checkpoint.
            habit_id (int): The foreign key referencing the habit the checkpoint belongs to.
            date (datetime): The start date of the checkpoint.

    """
    __tablename__ = 'checkpoints'
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey('habits.id'))
    checkpoint_date = Column(DateTime)
    habit = relationship("Habit", back_populates="checkpoints")
