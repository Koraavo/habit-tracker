# With which habits did I struggle most last month?

import datetime
import random
from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum as EnumColumn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import schedule
import time
import threading

engine = create_engine('sqlite:///habits2.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Creating frequency as a class with an Enum for daily and weekly
class Frequency(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'


# The habit class inherits from base (a declarative class by sql alchemy)
# id is the primary key, with type integer
# tasks would be strings
# frequency is an enumeration of values taken from frequency class
# The checkpoints defines the relationship between checkpoint class and habit class
# One habit can have multiple checkpoints
# the relationship function defines this relationship
# The backref parameter specifies the name of the attribute that will be added to the Checkpoint class to access the associated Habit object.
# The cascade parameter specifies the cascading behavior,
# where "all, delete-orphan" indicates that associated Checkpoint objects should be deleted
# when the corresponding Habit object is deleted.

class Habit(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    frequency = Column(EnumColumn(Frequency))
    checkpoints = relationship("Checkpoint", backref="habit", cascade="all, delete-orphan")


class Checkpoint(Base):
    __tablename__ = 'checkpoints'
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey('habits.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)


Base.metadata.create_all(engine)


def create_habit(task, frequency):
    return Habit(task=task, frequency=frequency)


def add_checkpoint(habit, start_date, end_date):
    checkpoint = Checkpoint(start_date=start_date, end_date=end_date)
    habit.checkpoints.append(checkpoint)
    session.commit()


def generate_random_habits():
    # Generate five random habits
    tasks = ["Exercise", "Read a book", "Drink water", "Meditate", "Write in a journal"]
    frequencies = [Frequency.WEEKLY, Frequency.WEEKLY, Frequency.DAILY, Frequency.DAILY, Frequency.DAILY]
    for task, frequency in zip(tasks, frequencies):
        habit = session.query(Habit).filter_by(task=task).first()
        if not habit:
            habit = create_habit(task, frequency)
            session.add(habit)
            session.commit()


# def generate_fake_checkpoints():
#     # Generate fake checkpoints for the existing habits
#     habits = session.query(Habit).all()
#     for habit in habits:
#         print(f"Generating checkpoints for habit: {habit.task} ({habit.frequency.value})")
#         if not habit.checkpoints:
#             if habit.frequency == Frequency.DAILY:
#                 print("Generating daily checkpoints...")
#                 num_checkpoints = random.randint(28, 35)
#                 today = datetime.datetime.now().date()
#                 checkpoint_dates = set()
#
#                 for _ in range(num_checkpoints):
#                     start_date = today - datetime.timedelta(days=random.randint(0, 29))
#                     end_date = start_date + datetime.timedelta(hours=random.randint(1, 12))
#                     checkpoint_dates.add((start_date, end_date))
#
#                     # Print progress after generating each checkpoint
#                     print(f"Generated checkpoint: {start_date} - {end_date}")
#
#                 for start_date, end_date in checkpoint_dates:
#                     add_checkpoint(habit, start_date, end_date)
#                 print(f"Generated {len(checkpoint_dates)} daily checkpoints for habit: {habit.task}")
#
#             elif habit.frequency == Frequency.WEEKLY:
#                 print("Generating weekly checkpoints...")
#                 num_weeks = random.randint(4, 5)
#                 today = datetime.datetime.now().date()
#                 checkpoint_dates = set()
#
#                 for _ in range(num_weeks):
#                     start_date = today - datetime.timedelta(weeks=random.randint(0, 3))
#                     end_date = start_date + datetime.timedelta(hours=random.randint(1, 12))
#                     checkpoint_dates.add((start_date, end_date))
#
#                     # Print progress after generating each checkpoint
#                     print(f"Generated checkpoint: {start_date} - {end_date}")
#
#                 for start_date, end_date in checkpoint_dates:
#                     add_checkpoint(habit, start_date, end_date)
#                 print(f"Generated {len(checkpoint_dates)} weekly checkpoints for habit: {habit.task}")



def generate_fake_checkpoints():
    # Generate fake checkpoints for the existing habits
    habits = session.query(Habit).all()
    for habit in habits:
        print(f"Generating checkpoints for habit: {habit.task} ({habit.frequency.value})")
        if not habit.checkpoints:
            if habit.frequency == Frequency.DAILY:
                print("Generating daily checkpoints...")
                num_checkpoints = random.randint(28, 35)
                today = datetime.datetime.now().date()
                checkpoint_dates = set()

                for _ in range(num_checkpoints):
                    start_date = today - datetime.timedelta(days=random.randint(0, 29))
                    end_date = start_date + datetime.timedelta(hours=random.randint(1, 12))
                    checkpoint_dates.add((start_date, end_date))

                # Check if any future start_dates with the same date already exist
                existing_start_dates = {checkpoint.start_date for checkpoint in habit.checkpoints}
                valid_checkpoints = []
                for start_date, end_date in checkpoint_dates:
                    if start_date not in existing_start_dates:
                        valid_checkpoints.append((start_date, end_date))
                checkpoint_dates = valid_checkpoints

                for start_date, end_date in checkpoint_dates:
                    add_checkpoint(habit, start_date, end_date)
                    print(f"Generated checkpoint: {start_date} - {end_date}")

                print(f"Generated {len(checkpoint_dates)} daily checkpoints for habit: {habit.task}")

            elif habit.frequency == Frequency.WEEKLY:
                print("Generating weekly checkpoints...")
                num_weeks = random.randint(4, 5)
                today = datetime.datetime.now().date()
                checkpoint_dates = set()

                for _ in range(num_weeks):
                    start_date = today - datetime.timedelta(weeks=random.randint(0, 3))
                    end_date = start_date + datetime.timedelta(hours=random.randint(1, 12))
                    checkpoint_dates.add((start_date, end_date))

                # Check if any future start_dates with the same date already exist
                existing_start_dates = {checkpoint.start_date for checkpoint in habit.checkpoints}
                valid_checkpoints = []
                for start_date, end_date in checkpoint_dates:
                    if start_date not in existing_start_dates:
                        valid_checkpoints.append((start_date, end_date))
                checkpoint_dates = valid_checkpoints

                for start_date, end_date in checkpoint_dates:
                    add_checkpoint(habit, start_date, end_date)
                    print(f"Generated checkpoint: {start_date} - {end_date}")

                print(f"Generated {len(checkpoint_dates)} weekly checkpoints for habit: {habit.task}")


def get_habits():
    habits = session.query(Habit).order_by(Habit.id).all()
    print("Existing Habits:")
    for habit in habits:
        print(f"{habit.id}. {habit.task} ({habit.frequency.value})")


def habits_with_checkpoints(habits):
    print("Habits and their checkpoints:")
    for habit in habits:
        print(f"\nHabit: {habit.task} ({habit.frequency.value})")
        checkpoints = sorted(habit.checkpoints, key=lambda x: x.start_date)  # Sort checkpoints based on start date
        print("Checkpoints:")
        for checkpoint in checkpoints:
            print(f"Start Date: {checkpoint.start_date}, End Date: {checkpoint.end_date}")


def get_longest_run_streak(habits):
    longest_weekly_streak = 0
    longest_weekly_streak_habits = []
    longest_daily_streak = 0
    longest_daily_streak_habits = []

    for habit in habits:
        checkpoints = sorted(habit.checkpoints, key=lambda x: x.start_date)
        weekly_streak = 0
        max_weekly_streak = 0
        daily_streak = 0
        max_daily_streak = 0
        previous_end_date = None

        for checkpoint in checkpoints:
            start_date = checkpoint.start_date.date()
            end_date = checkpoint.end_date.date()

            if habit.frequency == Frequency.WEEKLY:
                if previous_end_date is None or start_date - previous_end_date == datetime.timedelta(
                        weeks=1) and start_date.weekday() == previous_end_date.weekday():
                    weekly_streak += 1
                else:
                    max_weekly_streak = max(max_weekly_streak, weekly_streak)
                    weekly_streak = 1
                previous_end_date = end_date

            elif habit.frequency == Frequency.DAILY:
                if previous_end_date is None or start_date - previous_end_date == datetime.timedelta(days=1):
                    daily_streak += 1
                else:
                    max_daily_streak = max(max_daily_streak, daily_streak)
                    daily_streak = 1
                previous_end_date = end_date

        max_weekly_streak = max(max_weekly_streak, weekly_streak)
        max_daily_streak = max(max_daily_streak, daily_streak)

        if max_weekly_streak > longest_weekly_streak:
            longest_weekly_streak = max_weekly_streak
            longest_weekly_streak_habits = [habit]
        elif max_weekly_streak == longest_weekly_streak:
            longest_weekly_streak_habits.append(habit)

        if max_daily_streak > longest_daily_streak:
            longest_daily_streak = max_daily_streak
            longest_daily_streak_habits = [habit]
        elif max_daily_streak == longest_daily_streak:
            longest_daily_streak_habits.append(habit)

    return longest_weekly_streak, longest_weekly_streak_habits, longest_daily_streak, longest_daily_streak_habits


def get_broken_streak_habits(habits):
    broken_streak_habits = []

    for habit in habits:
        checkpoints = sorted(habit.checkpoints, key=lambda x: x.start_date)
        previous_end_date = None
        streak_broken = False

        for checkpoint in checkpoints:
            start_date = checkpoint.start_date.date()
            end_date = checkpoint.end_date.date()

            if habit.frequency == Frequency.WEEKLY:
                if previous_end_date is not None and (
                        start_date - previous_end_date != datetime.timedelta(weeks=1) or
                        start_date.weekday() != previous_end_date.weekday()
                ):
                    streak_broken = True
                    break

            elif habit.frequency == Frequency.DAILY:
                if previous_end_date is not None and (start_date - previous_end_date != datetime.timedelta(days=1)):
                    streak_broken = True
                    break

            previous_end_date = end_date

        if streak_broken:
            broken_streak_habits.append(habit)

    return broken_streak_habits


def delete_habit(habit_id):
    habit = session.query(Habit).get(habit_id)
    if habit:
        session.delete(habit)
        session.commit()
        print("Habit deleted successfully!")
    else:
        print("Invalid habit ID!")


def get_user_input(message):
    user_input = input(message + " (press 'q' to go back to the main menu): ")
    if user_input.lower() == "q":
        return None
    return user_input


def send_daily_reminder(habit):
    # Add code to send a reminder for the daily habit
    print(f"Reminder: Don't forget to {habit.task} today!")


def send_weekly_reminder(habit):
    # Add code to send a reminder for the weekly habit
    print(f"Reminder: Don't forget to {habit.task} this week!")


def schedule_daily_reminder(habit):
    reminder_time = get_user_input("Enter the reminder time for the habit (HH:MM AM/PM): ")
    if not reminder_time:
        return

    # Schedule the reminder at the specified time
    schedule.every().day.at(reminder_time).do(send_daily_reminder, habit=habit)

    print(f"Daily reminder for habit '{habit.task}' scheduled at {reminder_time}")


def schedule_weekly_reminder(habit):
    reminder_time = get_user_input("Enter the reminder time for the habit (HH:MM AM/PM): ")
    if not reminder_time:
        return

    # Schedule the reminder every 7 days at the specified time
    schedule.every(7).days.at(reminder_time).do(send_weekly_reminder, habit=habit)

    print(f"Weekly reminder for habit '{habit.task}' scheduled at {reminder_time}")


def run_scheduler():
    check_schedule = True
    while check_schedule:
        schedule.run_pending()
        time.sleep(1)


# scheduler_thread = threading.Thread(target=run_scheduler)
# scheduler_thread.start()

def main():
    # Generate random habits and checkpoints
    generate_random_habits()
    generate_fake_checkpoints()
    menu = """
    Menu:
        1. Create a habit
        2. Add a checkpoint
        3. Show all habits
        4. Habits and Checkpoints
        5. Get longest run streak
        6. Delete a habit
        7. Current daily habits
        8. Current weekly habits
        9. Habits with broken streaks
        0. Quit
    """
    while (choice := input(menu + "Choose an option from the menu: ")) != '0':
        if choice == "1":
            task = get_user_input("Enter the habit task: ")
            if task:
                frequency_input = get_user_input("Enter the habit frequency (daily/weekly): ")
                if frequency_input.lower() == "daily":
                    frequency = Frequency.DAILY
                elif frequency_input.lower() == "weekly":
                    frequency = Frequency.WEEKLY
            else:
                print("Invalid task or frequency! Habit not created.")
                continue
            habit = create_habit(task, frequency)
            session.add(habit)
            session.commit()
            print("Habit added successfully!")

            if frequency == Frequency.DAILY:
                schedule_daily_reminder(habit)
            elif frequency == Frequency.WEEKLY:
                schedule_weekly_reminder(habit)

        elif choice == "2":
            habits = session.query(Habit).order_by(Habit.id).all()
            print("Existing Habits:")
            for habit in habits:
                print(f"{habit.id}. {habit.task} ({habit.frequency.value})")
            habit_id = get_user_input("Enter the habit ID to add a checkpoint")
            if not habit_id:
                continue
            habit_id = int(habit_id)
            habit = session.query(Habit).get(habit_id)
            if habit:
                start_date_str = input("Enter the start date (YYYY-MM-DD HH:MM): ")
                end_date_str = input("Enter the end date (YYYY-MM-DD HH:MM): ")
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
                add_checkpoint(habit, start_date, end_date)
                print("Checkpoint added successfully!")
            else:
                print("Invalid habit ID!")
        elif choice == "3":
            get_habits()
        elif choice == "4":
            habits = session.query(Habit).order_by(Habit.id).all()
            habits_with_checkpoints(habits)
        elif choice == "5":
            habits = session.query(Habit).all()
            longest_weekly_streak, longest_weekly_streak_habits, longest_daily_streak, longest_daily_streak_habits = get_longest_run_streak(
                habits)
            print(f"Longest weekly streak: {longest_weekly_streak}")
            print("Habits with the longest weekly streak:")
            for habit in longest_weekly_streak_habits:
                print(f"- Habit: {habit.task} ({habit.frequency.value})")

            print(f"Longest daily streak: {longest_daily_streak}")
            print("Habits with the longest daily streak:")
            for habit in longest_daily_streak_habits:
                print(f"- Habit: {habit.task} ({habit.frequency.value})")

        elif choice == "6":
            get_habits()
            habit_id = get_user_input("Enter the habit ID to delete: ")
            if not habit_id:
                continue
            habit_id = int(habit_id)
            delete_habit(habit_id)

        elif choice == "7":
            daily_habits = session.query(Habit).filter_by(frequency=Frequency.DAILY).all()
            print("Current daily habits:")
            for habit in daily_habits:
                print(f"- Habit: {habit.task}")

        elif choice == "8":
            weekly_habits = session.query(Habit).filter_by(frequency=Frequency.WEEKLY).all()
            print("Current weekly habits:")
            for habit in weekly_habits:
                print(f"- Habit: {habit.task}")
        elif choice == "9":
            habits = session.query(Habit).all()
            broken_streak_habits = get_broken_streak_habits(habits)
            print("Habits with broken streaks:")
            for habit in broken_streak_habits:
                print(f"- Habit: {habit.task} ({habit.frequency.value})")
        else:
            print("Invalid choice! Please try again.")

    exit("Bye!")


if __name__ == "__main__":
    main()
    # scheduler_thread = threading.Thread(target=run_scheduler)
    # scheduler_thread.start()
