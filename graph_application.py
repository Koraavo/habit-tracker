import matplotlib.pyplot as plt
import numpy as np
from Final import *
from datetime import datetime, timedelta
from matplotlib.ticker import FixedLocator


def plot_habits_with_checkpoints(habits):
    """Create a graph showing each habit and its specific checkpoints.

    Args:
        habits (List[Habit]): The list of habits to be plotted.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    # Get the date range for the graph
    start_date = datetime.now().date() - timedelta(days=30)  # Start date is 30 days ago
    end_date = datetime.now().date() + timedelta(days=60) # End date is today

    # Generate a list of all dates within the range
    all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # Get the number of habits
    num_habits = len(habits)

    # Select specific habits to be displayed
    selected_habits = []
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
        checkpoints = sorted(habit.checkpoints, key=lambda x: (x.start_date.month, x.start_date.day))
        if checkpoints:
            dates = [checkpoint.start_date.date() for checkpoint in checkpoints]
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
    plt.tight_layout()

    # Convert x-axis ticks from numpy float64 to datetime objects
    x_ticks = plt.gca().get_xticks()
    x_ticks_datetime = [start_date + timedelta(days=int(x)) for x in x_ticks]

    # Format x-axis ticks to show only month and day
    plt.gca().xaxis.set_major_locator(FixedLocator(x_ticks))
    plt.gca().xaxis.set_major_formatter(plt.FixedFormatter([date.strftime("%m-%d") for date in x_ticks_datetime]))

    plt.show()


# Call the function to generate the graph
habits = session.query(Habit).order_by(Habit.id).all()
plot_habits_with_checkpoints(habits)
