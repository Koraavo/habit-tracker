import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from habit import Base, Habit, Frequency, Checkpoint
from main import create_habit, add_checkpoint, generate_random_habits, generate_fake_checkpoints, habits_with_checkpoints
from analytics import get_broken_streak_habits, get_longest_streak_for_habit, get_longest_run_streak
from io import StringIO
import sys


@pytest.fixture(scope="session")
def database():
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    # Create the tables
    Base.metadata.create_all(engine)
    yield engine
    # Teardown: Close the engine
    engine.dispose()

@pytest.fixture(scope="function")
def session(database):
    # Create a new session for each test
    Session = sessionmaker(bind=database)
    session = Session()
    yield session
    # Teardown: Rollback the session and close it
    session.rollback()
    session.close()

def test_create_habit(session):
    # Create a habit
    habit = create_habit("Exercise", Frequency.DAILY)

    # Add the habit to the session
    session.add(habit)
    session.commit()

    # Verify if the habit is an instance of the Habit class
    assert isinstance(habit, Habit)

    # Verify if the habit has the correct task and frequency
    assert habit.task == "Exercise"
    assert habit.frequency == Frequency.DAILY

    # Verify if the habit is added to the session
    assert session.query(Habit).get(habit.id) is not None


def test_add_checkpoint(session):
    # Create a habit
    habit = create_habit("Exercise", Frequency.DAILY)

    # Add a checkpoint to the habit
    checkpoint_date = datetime.now()
    add_checkpoint(habit, checkpoint_date)

    # Verify if the habit has a checkpoint with the correct start date
    assert len(habit.checkpoints) == 1
    assert habit.checkpoints[0].checkpoint_date == checkpoint_date


def test_generate_random_habits(session):
    # Generate random habits
    print("Generating random habits...")
    generate_random_habits()

    # Verify if five habits are added to the session
    habits = session.query(Habit).all()
    print(f"Number of habits in session: {len(habits)}")

    # Verify if each habit has the correct task and frequency
    for habit in habits:
        assert habit.task in ["Exercise", "Read a book", "Drink water", "Meditate", "Write in a journal"]
        assert habit.frequency in [Frequency.WEEKLY, Frequency.DAILY]

    # Verify if each habit is an instance of the Habit class
    assert all(isinstance(habit, Habit) for habit in habits)

    # Verify if each habit is added to the session
    assert all(session.query(Habit).get(habit.id) is not None for habit in habits)


def test_generate_fake_checkpoints(session):
    # Generate fake checkpoints
    generate_fake_checkpoints()  # Pass the session object as a parameter
    habits = session.query(Habit).all()
    # Verify if the generated checkpoints have the correct dates
    for habit in habits:
        assert all(isinstance(checkpoint.checkpoint_date, datetime) for checkpoint in habit.checkpoints)


# Unit test for habits_with_checkpoints
def test_habits_with_checkpoints(session):
    # Create a habit with checkpoints in the database
    habit = Habit(task='Exercise', frequency=Frequency.DAILY)
    checkpoint1 = Checkpoint(checkpoint_date=datetime(2023, 6, 1))
    checkpoint2 = Checkpoint(checkpoint_date=datetime(2023, 6, 3))
    habit.checkpoints = [checkpoint1, checkpoint2]
    session.add(habit)
    session.commit()

    # Capture the printed output
    stdout = sys.stdout
    sys.stdout = StringIO()

    # Call the habits_with_checkpoints function
    habits_with_checkpoints([habit])

    # Get the captured output
    output = sys.stdout.getvalue()

    # Reset the standard output
    sys.stdout = stdout

    # Assert the printed output
    expected_output = "Habits and their checkpoints:\n\nHabit: Exercise (daily)\nCheckpoints:\nStart Date: 2023-06-01 00:00:00\nStart Date: 2023-06-03 00:00:00\n"
    assert output == expected_output


# Unit test for get_longest_streak_for_habit
def test_get_longest_streak_for_habit():
    # Create a habit with daily checkpoints
    habit1 = Habit(task='Exercise', frequency=Frequency.DAILY)
    checkpoint1 = Checkpoint(checkpoint_date=datetime(2023, 6, 1))
    checkpoint2 = Checkpoint(checkpoint_date=datetime(2023, 6, 2))
    checkpoint3 = Checkpoint(checkpoint_date=datetime(2023, 6, 3))
    checkpoint4 = Checkpoint(checkpoint_date=datetime(2023, 6, 6))
    habit1.checkpoints = [checkpoint1, checkpoint2, checkpoint3, checkpoint4]

    # Calculate the longest streak
    longest_streak1 = get_longest_streak_for_habit(habit1)

    # Assert the result
    assert longest_streak1 == 3

    # Create a habit with weekly checkpoints
    habit2 = Habit(task='Read a book', frequency=Frequency.WEEKLY)
    checkpoint5 = Checkpoint(checkpoint_date=datetime(2023, 5, 29))
    checkpoint6 = Checkpoint(checkpoint_date=datetime(2023, 6, 5))
    checkpoint7 = Checkpoint(checkpoint_date=datetime(2023, 6, 12))
    checkpoint8 = Checkpoint(checkpoint_date=datetime(2023, 6, 19))
    habit2.checkpoints = [checkpoint5, checkpoint6, checkpoint7, checkpoint8]

    # Calculate the longest streak
    longest_streak2 = get_longest_streak_for_habit(habit2)

    # Assert the result
    assert longest_streak2 == 4


# Unit test for get_longest_run_streak
def test_get_longest_run_streak():
    # Create sample habits with checkpoints
    habit1 = Habit(task='Exercise', frequency=Frequency.DAILY)
    checkpoint1 = Checkpoint(checkpoint_date=datetime(2023, 6, 1))
    checkpoint2 = Checkpoint(checkpoint_date=datetime(2023, 6, 2))
    checkpoint3 = Checkpoint(checkpoint_date=datetime(2023, 6, 3))
    checkpoint4 = Checkpoint(checkpoint_date=datetime(2023, 6, 6))
    habit1.checkpoints = [checkpoint1, checkpoint2, checkpoint3, checkpoint4]

    habit2 = Habit(task='Read a book', frequency=Frequency.WEEKLY)
    checkpoint5 = Checkpoint(checkpoint_date=datetime(2023, 5, 29))
    checkpoint6 = Checkpoint(checkpoint_date=datetime(2023, 6, 5))
    checkpoint7 = Checkpoint(checkpoint_date=datetime(2023, 6, 12))
    checkpoint8 = Checkpoint(checkpoint_date=datetime(2023, 6, 19))
    habit2.checkpoints = [checkpoint5, checkpoint6, checkpoint7, checkpoint8]

    # Call the get_longest_run_streak function
    longest_weekly_streak, weekly_streak_habits, longest_daily_streak, daily_streak_habits = get_longest_run_streak(
        [habit1, habit2])

    # Assert the results
    assert longest_weekly_streak == 4
    assert weekly_streak_habits == [habit2]
    assert longest_daily_streak == 3
    assert daily_streak_habits == [habit1]


# Unit test for get_broken_streak_habits
def test_get_broken_streak_habits():
    # Create a habit with a broken streak
    habit1 = Habit(task='Exercise', frequency=Frequency.DAILY)
    checkpoint1 = Checkpoint(checkpoint_date=datetime(2023, 6, 1))
    checkpoint2 = Checkpoint(checkpoint_date=datetime(2023, 6, 2))
    checkpoint3 = Checkpoint(checkpoint_date=datetime(2023, 6, 4))  # Gap of one day
    checkpoint4 = Checkpoint(checkpoint_date=datetime(2023, 6, 5))
    habit1.checkpoints = [checkpoint1, checkpoint2, checkpoint3, checkpoint4]

    # Create a habit with no broken streak
    habit2 = Habit(task='Read a book', frequency=Frequency.WEEKLY)
    checkpoint5 = Checkpoint(checkpoint_date=datetime(2023, 5, 29))
    checkpoint6 = Checkpoint(checkpoint_date=datetime(2023, 6, 5))
    checkpoint7 = Checkpoint(checkpoint_date=datetime(2023, 6, 12))
    checkpoint8 = Checkpoint(checkpoint_date=datetime(2023, 6, 19))
    habit2.checkpoints = [checkpoint5, checkpoint6, checkpoint7, checkpoint8]

    # Call the get_broken_streak_habits function
    broken_streak_habits = get_broken_streak_habits([habit1, habit2])

    # Assert the result
    assert broken_streak_habits == [habit1]