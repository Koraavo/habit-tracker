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
        print(start_date)
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