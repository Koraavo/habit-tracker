from Final import *
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import StringIO
import sys


@pytest.fixture(scope="session")
def database():
    """
        In this test, we use a pytest fixture called database to create an in-memory SQLite database.
        The database fixture is scoped at the session level, ensuring that the database is created only once for all the tests in the session.
        The fixture yields the database engine, and after the test(s) complete, the teardown phase disposes of the engine.
    """
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    # Create the tables
    Base.metadata.create_all(engine)
    yield engine
    # Teardown: Close the engine
    engine.dispose()


def test_create_database(database):
    # Verify if the Habits table exists
    assert database.dialect.has_table(database, "habits")

    # Verify if the Checkpoints table exists
    assert database.dialect.has_table(database, "checkpoints")


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

    # Verify if the habit is an instance of the Habit class
    assert isinstance(habit, Habit)

    # Verify if the habit has the correct task and frequency
    assert habit.task == "Exercise"
    assert habit.frequency == Frequency.DAILY

    # Verify if the habit is added to the session
    assert habit in session


def test_add_checkpoint(session):
    # Create a habit
    habit = create_habit("Exercise", Frequency.DAILY)

    # Add a checkpoint to the habit
    start_date = datetime.now()
    add_checkpoint(habit, start_date)

    # Verify if the habit has a checkpoint with the correct start date
    assert len(habit.checkpoints) == 1
    assert habit.checkpoints[0].start_date == start_date


def test_generate_random_habits(session):
    # Generate random habits
    generate_random_habits()

    # Verify if five habits are added to the session
    habits = session.query(Habit).all()
    assert len(habits) == 5

    # Verify if each habit has the correct task and frequency
    for habit in habits:
        assert habit.task in ["Exercise", "Read a book", "Drink water", "Meditate", "Write in a journal"]
        assert habit.frequency in [Frequency.WEEKLY, Frequency.DAILY]


def test_generate_fake_checkpoints(session):
    # Create a habit with a daily frequency
    habit1 = Habit(task="Exercise", frequency=Frequency.DAILY)
    session.add(habit1)

    # Create a habit with a weekly frequency
    habit2 = Habit(task="Read a book", frequency=Frequency.WEEKLY)
    session.add(habit2)

    # Commit the session to persist the habits
    session.commit()

    # Generate fake checkpoints
    generate_fake_checkpoints()

    # Verify if checkpoints are added to the habits
    assert len(habit1.checkpoints) > 0
    assert len(habit2.checkpoints) > 0

    # Verify if the generated checkpoints have the correct dates
    for checkpoint in habit1.checkpoints:
        assert isinstance(checkpoint.start_date, datetime)
        assert (datetime.now().date() - checkpoint.start_date.date()).days <= 29

    for checkpoint in habit2.checkpoints:
        assert isinstance(checkpoint.start_date, datetime)
        assert (datetime.now().date() - checkpoint.start_date.date()).days <= 21


# Unit test for get_habits
def test_get_habits(database):
    # Create some sample habits in the database
    habit1 = Habit(task='Exercise', frequency=Frequency.DAILY)
    habit2 = Habit(task='Read a book', frequency=Frequency.WEEKLY)
    database.add(habit1)
    database.add(habit2)
    database.commit()

    # Capture the printed output
    stdout = sys.stdout
    sys.stdout = StringIO()

    # Call the get_habits function
    habits = get_habits()

    # Get the captured output
    output = sys.stdout.getvalue()

    # Reset the standard output
    sys.stdout = stdout

    # Assert the printed output
    expected_output = "Existing Habits:\n1. Exercise (daily)\n2. Read a book (weekly)\n"
    assert output == expected_output

    # Assert the returned habits
    assert habits == [habit1, habit2]


# Unit test for habits_with_checkpoints
def test_habits_with_checkpoints(database):
    # Create a habit with checkpoints in the database
    habit = Habit(task='Exercise', frequency=Frequency.DAILY)
    checkpoint1 = Checkpoint(start_date=datetime(2023, 6, 1))
    checkpoint2 = Checkpoint(start_date=datetime(2023, 6, 3))
    habit.checkpoints = [checkpoint1, checkpoint2]
    database.add(habit)
    database.commit()

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
    checkpoint1 = Checkpoint(start_date=datetime(2023, 6, 1))
    checkpoint2 = Checkpoint(start_date=datetime(2023, 6, 2))
    checkpoint3 = Checkpoint(start_date=datetime(2023, 6, 3))
    checkpoint4 = Checkpoint(start_date=datetime(2023, 6, 6))
    habit1.checkpoints = [checkpoint1, checkpoint2, checkpoint3, checkpoint4]

    # Calculate the longest streak
    longest_streak1 = get_longest_streak_for_habit(habit1)

    # Assert the result
    assert longest_streak1 == 3

    # Create a habit with weekly checkpoints
    habit2 = Habit(task='Read a book', frequency=Frequency.WEEKLY)
    checkpoint5 = Checkpoint(start_date=datetime(2023, 5, 29))
    checkpoint6 = Checkpoint(start_date=datetime(2023, 6, 5))
    checkpoint7 = Checkpoint(start_date=datetime(2023, 6, 12))
    checkpoint8 = Checkpoint(start_date=datetime(2023, 6, 19))
    habit2.checkpoints = [checkpoint5, checkpoint6, checkpoint7, checkpoint8]

    # Calculate the longest streak
    longest_streak2 = get_longest_streak_for_habit(habit2)

    # Assert the result
    assert longest_streak2 == 2


# Unit test for get_longest_run_streak
def test_get_longest_run_streak():
    # Create sample habits with checkpoints
    habit1 = Habit(task='Exercise', frequency=Frequency.DAILY)
    checkpoint1 = Checkpoint(start_date=datetime(2023, 6, 1))
    checkpoint2 = Checkpoint(start_date=datetime(2023, 6, 2))
    checkpoint3 = Checkpoint(start_date=datetime(2023, 6, 3))
    checkpoint4 = Checkpoint(start_date=datetime(2023, 6, 6))
    habit1.checkpoints = [checkpoint1, checkpoint2, checkpoint3, checkpoint4]

    habit2 = Habit(task='Read a book', frequency=Frequency.WEEKLY)
    checkpoint5 = Checkpoint(start_date=datetime(2023, 5, 29))
    checkpoint6 = Checkpoint(start_date=datetime(2023, 6, 5))
    checkpoint7 = Checkpoint(start_date=datetime(2023, 6, 12))
    checkpoint8 = Checkpoint(start_date=datetime(2023, 6, 19))
    habit2.checkpoints = [checkpoint5, checkpoint6, checkpoint7, checkpoint8]

    # Call the get_longest_run_streak function
    longest_weekly_streak, weekly_streak_habits, longest_daily_streak, daily_streak_habits = get_longest_run_streak(
        [habit1, habit2])

    # Assert the results
    assert longest_weekly_streak == 2
    assert weekly_streak_habits == [habit2]
    assert longest_daily_streak == 3
    assert daily_streak_habits == [habit1]


# Unit test for get_broken_streak_habits
def test_get_broken_streak_habits():
    # Create a habit with a broken streak
    habit1 = Habit(task='Exercise', frequency=Frequency.DAILY)
    checkpoint1 = Checkpoint(start_date=datetime(2023, 6, 1))
    checkpoint2 = Checkpoint(start_date=datetime(2023, 6, 2))
    checkpoint3 = Checkpoint(start_date=datetime(2023, 6, 4))  # Gap of one day
    checkpoint4 = Checkpoint(start_date=datetime(2023, 6, 5))
    habit1.checkpoints = [checkpoint1, checkpoint2, checkpoint3, checkpoint4]

    # Create a habit with no broken streak
    habit2 = Habit(task='Read a book', frequency=Frequency.WEEKLY)
    checkpoint5 = Checkpoint(start_date=datetime(2023, 5, 29))
    checkpoint6 = Checkpoint(start_date=datetime(2023, 6, 5))
    checkpoint7 = Checkpoint(start_date=datetime(2023, 6, 12))
    checkpoint8 = Checkpoint(start_date=datetime(2023, 6, 19))
    habit2.checkpoints = [checkpoint5, checkpoint6, checkpoint7, checkpoint8]

    # Call the get_broken_streak_habits function
    broken_streak_habits = get_broken_streak_habits([habit1, habit2])

    # Assert the result
    assert broken_streak_habits == [habit1]
