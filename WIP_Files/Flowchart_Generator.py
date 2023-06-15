from pyflowchart import Flowchart
with open('LongestHabitStreak.py') as f:
    code = f.read()
flowchart = Flowchart.from_code(code, field="", inner=True, simplify=False)
print(flowchart.flowchart())