import datetime
import random
from habit import Habit, Frequency, Checkpoint
from analytics import habits_with_checkpoints, plot_habits_with_checkpoints, get_broken_streak_habits, get_longest_streak_for_habit, get_longest_run_streak
from datetime import datetime, timedelta
from db import session

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def create_habit(task, frequency):
    """Create a new habit with the given task and frequency.

        Args:
            task (str): The description of the habit's task.
            frequency (Frequency): The frequency at which the habit is performed.

        Returns:
            Habit: The newly created Habit object.

    """
    return Habit(task=task, frequency=frequency)


def add_checkpoint(habit, date):
    """Add a new checkpoint to a habit.

        Args:
            habit (Habit): The Habit object to which the checkpoint will be added.
            date (datetime): The start date of the checkpoint.
    """
    checkpoint = Checkpoint(checkpoint_date=date)
    habit.checkpoints.append(checkpoint)
    session.commit()

def get_habits():
    """Get all habits from the database and print them.

        This function retrieves all habits from the database, orders them by their IDs,
        and prints their IDs, tasks, and frequencies.

    """
    habits = session.query(Habit).order_by(Habit.id).all()
    print("Existing Habits:")
    for habit in habits:
        print(f"{habit.id}. {habit.task} ({habit.frequency.value})")
    return habits

def generate_random_habits():
    """Generate five random habits if they don't already exist in the database.

        Random habits are created with pre-defined tasks and frequencies. Each habit
        is checked in the database, and if it doesn't exist, it is created and added.

    """
    # Generate five random habits
    tasks = ["Exercise", "Read a book", "Drink water", "Meditate", "Write in a journal"]
    # respective frequencies for each habit
    frequencies = [Frequency.WEEKLY, Frequency.WEEKLY, Frequency.DAILY, Frequency.DAILY, Frequency.DAILY]
    # create a habit, add it to the session and commit the session
    for task, frequency in zip(tasks, frequencies):
        # this code iterates over two lists,
        # if a habit with a matching task already exists in the database,
        # if not, create and add a new habit to the database.
        habit = session.query(Habit).filter_by(task=task).first()
        if not habit:
            print(f"Creating habit: {task} ({frequency.value})")
            habit = create_habit(task, frequency)
            session.add(habit)
            session.commit()


def generate_fake_checkpoints():
    """Generate fake checkpoints for the existing habits.

        This function generates checkpoints for each existing habit based on its frequency.
        For habits with a daily frequency, random daily checkpoints within a range are generated.
        For habits with a weekly frequency, random weekly checkpoints within a range are generated.
        The generated checkpoints are added to the respective habits using the add_checkpoint function.

    """
    # Generate fake checkpoints for the existing habits
    habits = session.query(Habit).all()
    for habit in habits:
        if not habit.checkpoints:
            print(f"Generating checkpoints for habit: {habit.task} ({habit.frequency.value})")
            if habit.frequency == Frequency.DAILY:
                print("Generating daily checkpoints...")
                num_checkpoints = random.randint(28, 35)
                today = datetime.now().date()
                checkpoint_dates = set()

                for _ in range(num_checkpoints):
                    # generates a random number of days (between 0 and 29),
                    # subtracts that duration from the current date (today),
                    # and assigns the resulting date to the variable start_date.
                    start_date = today - timedelta(days=random.randint(0, 29))
                    checkpoint_dates.add(start_date)

                # Check if any future start_dates with the same date already exist
                existing_start_dates = {checkpoint.checkpoint_date.date() for checkpoint in habit.checkpoints}
                valid_checkpoints = []
                for start_date in checkpoint_dates:
                    if start_date not in existing_start_dates:
                        valid_checkpoints.append(start_date)
                checkpoint_dates = valid_checkpoints

                for start_date in checkpoint_dates:
                    add_checkpoint(habit, start_date)
                    print(f"Generated checkpoint: {start_date}")

                print(f"Generated {len(checkpoint_dates)} daily checkpoints for habit: {habit.task}")

            elif habit.frequency == Frequency.WEEKLY:
                print("Generating weekly checkpoints...")
                num_weeks = random.randint(4, 5)
                today = datetime.now().date()
                checkpoint_dates = set()

                for _ in range(num_weeks):
                    start_date = today - timedelta(weeks=random.randint(0, 3))
                    checkpoint_dates.add(start_date)

                # Check if any future start_dates with the same date already exist
                existing_start_dates = {checkpoint.start_date.date() for checkpoint in habit.checkpoints}
                valid_checkpoints = []
                for start_date in checkpoint_dates:
                    if start_date not in existing_start_dates:
                        valid_checkpoints.append(start_date)
                checkpoint_dates = valid_checkpoints

                for start_date in checkpoint_dates:
                    add_checkpoint(habit, start_date)
                    print(f"Generated checkpoint: {start_date}")

                print(f"Generated {len(checkpoint_dates)} weekly checkpoints for habit: {habit.task}")
        else:
            # if habits already exist, just show the habits with their checkpoints
            habits_with_checkpoints(habits)

def delete_habit(habit_id):
    """Delete a habit based on the provided habit ID.

    Args:
        habit_id (int): The ID of the habit to be deleted.

    Returns:
        None
    """
    habit = session.query(Habit).get(habit_id)
    if habit:
        session.delete(habit)
        session.commit()
        print("Habit deleted successfully!")
    else:
        print("Invalid habit ID!")


def get_user_input(message):
    """Prompt the user for input and retrieve the entered value.

        Args:
            message (str): The message to display as a prompt for user input.

        Returns:
            str or None: The user input as a string, or None if the user enters 'q' to go back to the main menu.
    """
    user_input = input(message + " (press 'q' to go back to the main menu): ")
    if user_input.lower() == "q":
        return None
    return user_input


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
        5. Current daily habits
        6. Current weekly habits
        7. Get longest run streak
        8. Longest streak for habit
        9. Delete a habit
        10. Habits with broken streaks
        11. Show graphs for habits
        0. Quit
    """
    while (choice := input(menu + "Choose an option from the menu: ")) != '0':
        if choice == "1":
            task = get_user_input("Enter the habit task: ")
            if task:
                while True:
                    frequency_input = get_user_input("Enter the habit frequency (daily/weekly): ")
                    try:
                        frequency = Frequency(frequency_input.lower())
                        break
                    except ValueError:
                        print("Invalid frequency. Please enter 'daily' or 'weekly'.")
                habit = create_habit(task, frequency)
                session.add(habit)
                session.commit()
                print("Habit added successfully!")
            else:
                print("Invalid task! Habit not created.")
                continue
        elif choice == "2":
            habits = session.query(Habit).order_by(Habit.id).all()
            print("Existing Habits:")
            for habit in habits:
                print(f"{habit.id}. {habit.task} ({habit.frequency.value})")
            while True:
                habit_id = get_user_input("Enter the habit ID to add a checkpoint: ")
                try:
                    habit_id = int(habit_id)
                    habit = session.query(Habit).get(habit_id)
                    if habit:
                        break
                    else:
                        print("Invalid habit ID. Please enter a valid habit ID.")
                except ValueError:
                    print("Invalid habit ID. Please enter a valid integer.")
            while True:
                start_date_str = input("Enter the start date (YYYY-MM-DD HH:MM): ")
                try:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
                    existing_checkpoint = session.query(Checkpoint).filter_by(habit_id=habit_id,
                                                                              checkpoint_date=start_date).first()
                    if existing_checkpoint:
                        print("Checkpoint already exists for this habit and start date.")
                        break
                    else:
                        add_checkpoint(habit, start_date)
                        print("Checkpoint added successfully!")
                        break
                except ValueError:
                    print("Invalid date format. Please enter the date in the format YYYY-MM-DD HH:MM.")
        elif choice == "3":
            get_habits()
        elif choice == "4":
            habits = session.query(Habit).order_by(Habit.id).all()
            habits_with_checkpoints(habits)
        elif choice == "5":
            daily_habits = session.query(Habit).filter_by(frequency=Frequency.DAILY).all()
            print("Current daily habits:")
            for habit in daily_habits:
                print(f"- Habit: {habit.task}")

        elif choice == "6":
            weekly_habits = session.query(Habit).filter_by(frequency=Frequency.WEEKLY).all()
            print("Current weekly habits:")
            for habit in weekly_habits:
                print(f"- Habit: {habit.task}")
        elif choice == "7":
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
        elif choice == "8":
            habits = session.query(Habit).order_by(Habit.id).all()
            get_habits()
            habit_id = get_user_input("Enter the habit ID to see the longest streak: ")
            if not habit_id:
                continue
            habit_id = int(habit_id)
            habit = session.query(Habit).get(habit_id)
            if habit:
                max_streak = get_longest_streak_for_habit(habit)
                print(f"Longest streak for habit '{habit.task}' ({habit.frequency.value}): {max_streak}")
            else:
                print("Invalid habit ID!")
        elif choice == "9":
            get_habits()
            habit_id = get_user_input("Enter the habit ID to delete: ")
            if not habit_id:
                continue
            habit_id = int(habit_id)
            delete_habit(habit_id)
        elif choice == "10":
            habits = session.query(Habit).all()
            broken_streak_habits = get_broken_streak_habits(habits)
            print("Habits with broken streaks:")
            for habit in broken_streak_habits:
                print(f"- Habit: {habit.task} ({habit.frequency.value})")
        elif choice == "11":
            habits = session.query(Habit).order_by(Habit.id).all()
            plot_habits_with_checkpoints(habits)
        else:
            print("Invalid choice! Please try again.")

    exit("Bye!")


if __name__ == "__main__":
    main()
