import datetime
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from habit import Frequency, Checkpoint, Habit


def get_longest_streak_for_habit(habit):
    """Calculate the longest streak of consecutive checkpoints for a habit.

    Calculates and returns the longest streak of consecutive checkpoints for the given habit.

    Args:
        habit (Habit): The Habit object for which to calculate the longest streak.

    Returns:
        int: The length of the longest streak of consecutive checkpoints.
    """
    checkpoints = sorted(habit.checkpoints, key=lambda x: (x.checkpoint_date.month, x.checkpoint_date.day))
    streak = 0
    max_streak = 0
    previous_start_date = None

    for checkpoint in checkpoints:
        start_date = checkpoint.checkpoint_date.date()
        # print(start_date)
        if habit.frequency == Frequency.WEEKLY:
            if previous_start_date is None or (start_date - previous_start_date).days == 7:
                streak += 1
            else:
                max_streak = max(max_streak, streak)
                streak = 1
            previous_start_date = start_date

        elif habit.frequency == Frequency.DAILY:
            if previous_start_date is None or (start_date - previous_start_date).days == 1:
                streak += 1
            else:
                max_streak = max(max_streak, streak)
                streak = 1
            previous_start_date = start_date

    max_streak = max(max_streak, streak)
    return max_streak


def get_longest_run_streak(habits):
    """Calculate the longest run streak for habits with weekly and daily frequencies.

    Calculates and returns the longest run streak for habits with weekly frequency and daily frequency.
    A run streak is defined as the longest consecutive streak of checkpoints for each frequency type.

    Args:
        habits: retrieved from the database.

    Returns:
        Tuple[int, List[Habit], int, List[Habit]]: A tuple containing the longest weekly streak,
        the list of habits with the longest weekly streak, the longest daily streak, and the list
        of habits with the longest daily streak.
    """
    longest_weekly_streak = 0
    longest_weekly_streak_habits = []
    longest_daily_streak = 0
    longest_daily_streak_habits = []

    for habit in habits:
        max_streak = get_longest_streak_for_habit(habit)

        if habit.frequency == Frequency.WEEKLY:
            if max_streak > longest_weekly_streak:
                longest_weekly_streak = max_streak
                longest_weekly_streak_habits = [habit]
            elif max_streak == longest_weekly_streak:
                longest_weekly_streak_habits.append(habit)

        elif habit.frequency == Frequency.DAILY:
            if max_streak > longest_daily_streak:
                longest_daily_streak = max_streak
                longest_daily_streak_habits = [habit]
            elif max_streak == longest_daily_streak:
                longest_daily_streak_habits.append(habit)

    return longest_weekly_streak, longest_weekly_streak_habits, longest_daily_streak, longest_daily_streak_habits


def get_broken_streak_habits(habits):
    """Retrieve habits with broken streaks.

        Retrieves habits from the database and identifies the habits with broken streaks,
        where a streak is considered broken if there is a gap between consecutive checkpoints
        for each frequency type (weekly or daily).

        Returns:
            List[Habit]: A list of habits with broken streaks.
    """
    broken_streak_habits = []

    for habit in habits:
        checkpoints = sorted(habit.checkpoints, key=lambda x: (x.checkpoint_date.month, x.checkpoint_date.day))
        previous_end_date = None
        streak_broken = False

        for checkpoint in checkpoints:
            start_date = checkpoint.checkpoint_date.date()
            if habit.frequency == Frequency.WEEKLY:
                if previous_end_date is not None and (
                        start_date - previous_end_date != timedelta(weeks=1)
                        or start_date.weekday() != previous_end_date.weekday()
                ):
                    streak_broken = True
                    break

            elif habit.frequency == Frequency.DAILY:
                if previous_end_date is not None and (start_date - previous_end_date != timedelta(days=1)):
                    streak_broken = True
                    break

            previous_end_date = start_date

        if streak_broken:
            broken_streak_habits.append(habit)

    return broken_streak_habits


def plot_habits_with_checkpoints(habits):
    """Create a graph showing each habit and its specific checkpoints.

    Args:
        habits (List[Habit]): The list of habits to be plotted.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    # Get the date range for the graph
    all_dates = []
    for habit in habits:
        for checkpoint in habit.checkpoints:
            all_dates.append(checkpoint.checkpoint_date.date())
    if all_dates:
        start_date = min(all_dates)
        end_date = max(all_dates)
    else:
        # If there are no checkpoints, use a default date range of 60 days
        start_date = datetime.now().date() - timedelta(days=30)
        end_date = datetime.now().date() + timedelta(days=30)
    # Generate a list of all dates within the range
    all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    for habit in habits:
        print(f"{habit.id}. {habit.task}")
    while True:
        choice = input("Enter the habit numbers to display (separated by comma): ")
        selected_ids = [int(h.strip()) for h in choice.split(",")]
        selected_habits = [habit for habit in habits if habit.id in selected_ids]
        if len(selected_habits) == len(selected_ids):
            break
        else:
            print("Invalid habit number(s). Please try again.")

    for i, habit in enumerate(selected_habits):
        checkpoints = sorted(habit.checkpoints, key=lambda x: (x.checkpoint_date.month, x.checkpoint_date.day))
        if checkpoints:
            dates = [checkpoint.checkpoint_date.date() for checkpoint in checkpoints]
            y_values = [i] * len(checkpoints)

            # Find the index of the first checkpoint in all_dates
            first_date_index = all_dates.index(dates[0])

            plt.plot(dates, y_values, marker='o', linestyle='', markersize=6, label=habit.task)

            # Plot grey dots for the habit after the first checkpoint
            for date in all_dates[first_date_index:]:
                plt.plot(date, i, marker='o', color='grey', alpha=0.3)

    plt.yticks(np.arange(len(selected_habits)), [habit.task for habit in selected_habits])
    plt.xlabel('Date (Month-Day)')
    plt.ylabel('Habit')
    plt.title('Habits with Checkpoints')
    # get the dates and format it with month and day without the year
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    plt.gcf().autofmt_xdate()  # Rotate and align the x-axis labels for better visibility
    plt.tight_layout()
    plt.show()
