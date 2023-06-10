import pytest
from unittest.mock import patch
from io import StringIO
from Final import *
from datetime import datetime
import os

@pytest.fixture
def db_session():
    # Create an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()

    yield session

    # Clear the database after each test
    session.rollback()
    Base.metadata.drop_all(bind=session.bind)


def test_create_habit():
    habit = create_habit("Exercise", Frequency.DAILY)
    assert habit.task == "Exercise"
    assert habit.frequency == Frequency.DAILY


def test_add_checkpoint():
    habit = create_habit("Exercise", Frequency.DAILY)
    start_date = datetime(2023, 5, 1, hour=9, minute=30)  # Specify the hour and minute
    add_checkpoint(habit, start_date)
    checkpoint = habit.checkpoints[0]
    assert checkpoint.start_date == start_date


def test_generate_random_habits(db_session):
    with patch('random.randint', return_value=0):  # Mock random.randint to generate the first task
        generate_random_habits()
    habits = db_session.query(Habit).all()
    assert len(habits) == 5


def test_generate_fake_checkpoints(db_session):
    habit = create_habit("Exercise", Frequency.DAILY)
    db_session.add(habit)
    db_session.commit()

    with patch('random.randint', return_value=0):  # Mock random.randint to generate checkpoints with the same dates
        generate_fake_checkpoints()

    checkpoints = habit.checkpoints
    assert len(checkpoints) == 1
    assert checkpoints[0].start_date.date() == datetime.now().date()


def test_get_longest_streak_for_habit():
    habit = create_habit("Exercise", Frequency.DAILY)
    start_date = datetime(2023, 5, 1)
    add_checkpoint(habit, start_date)
    streak = get_longest_streak_for_habit(habit)
    assert streak == 1


def test_get_longest_run_streak():
    habit1 = create_habit("Exercise", Frequency.DAILY)
    habit2 = create_habit("Read a book", Frequency.DAILY)
    start_date = datetime(2023, 5, 1)
    add_checkpoint(habit1, start_date)
    add_checkpoint(habit2, start_date)
    longest_weekly_streak, _, longest_daily_streak, _ = get_longest_run_streak([habit1, habit2])
    assert longest_weekly_streak == 0
    assert longest_daily_streak == 1


def test_get_broken_streak_habits():
    habit1 = create_habit("Exercise", Frequency.DAILY)
    habit2 = create_habit("Read a book", Frequency.DAILY)
    start_date = datetime(2023, 5, 1)
    add_checkpoint(habit1, start_date)
    broken_streak_habits = get_broken_streak_habits([habit1, habit2])
    assert broken_streak_habits == [habit2]


def test_delete_habit(db_session):
    habit = create_habit("Exercise", Frequency.DAILY)
    db_session.add(habit)
    db_session.commit()
    delete_habit(habit)
    habits = db_session.query(Habit).all()
    assert len(habits) == 0


def test_menu():
    with patch('sys.stdout', new=StringIO()) as fake_output, \
            patch('builtins.input', side_effect=['1', 'Exercise', '1', '2', '3']):
        main()

    output = fake_output.getvalue()
    assert "Habit Manager" in output
    assert "1. Create a new habit" in output
    assert "2. List all habits" in output
    assert "3. Quit" in output
    assert "Enter your choice: " in output
    assert "Enter the habit task: " in output
    assert "Enter the habit frequency (1 for DAILY, 2 for WEEKLY): " in output
    assert "Goodbye!" in output
