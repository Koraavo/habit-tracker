# Habit Tracker
A habit tracker is used to track habits. These habits could be either daily habits or weekly habits.

Five Dummy habits along with their checkpoints have initially been created for test.

Since the project is created in python, python 3.7 or above should be installed to run the code.
This should automatically install pip. If pip is not installed, please install pip.

### How to install
1. Clone/Download the source code
<code> git clone https://github.com/Koraavo/habit-tracker.git </code>

2. You can either install PyCharm and let it take care of everything or
3. install and set up a virtual environment. 
You can follow the this article on setting up a virtual env: 
https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/

4. The requirements file has been generated using the following command:
<code>pip freeze > requirements.txt</code> 

In order to run the code, you would need to install the python packages from the requirements file
You can use the pip package manager to do this.

5. To start, open up a terminal or a command prompt and navigate to the directory of your Python project. 
Once you are there, type the following command:
<code>pip install -r requirements.txt</code> 

The code is split in four python files:
- main.py - this is the main file that should be run. 
All other information is imported into this file
- habit.py - All the necessary classes (habit, frequency and checkpoint)
- db.py - initiating sqlite via sql alchemy
- analytics.py - all the analytical functions are stored here

The habit tracker is capable of the following:
- create a habit
- add checkpoints for the habits
- Show all habits
- Show the habits along with their checkpoints
- Current daily habits
- Current weekly habits
- Get longest run streak among daily and weekly habits
- longest run streak for a habit
- delete a habit
- get habits with broken streaks
- show a graph of selected habits

SQL Alchemy is used to create a database and store the data.

You can run the file in the terminal or the command prompt by typing 
<code>python3 main.py</code> or in PyCharm by right clicking on the file and selecting run.

In order to complete a daily task, you would need to add a checkpoint in the year-month-date hour:min format
This is how the habit is also tracked.

### Run Tests
1. In order to run the tests, you would need to install pytest.

2. If you are using PyCharm, you can simply install pytest along with the rest of the requirements 
or install the module using the command <code>pip install pytest</code>

3. Some basic tests are created in the test_application.py file.
The file is renamed with test in the beginning for pytest to detect the file automatically

4. You can run the command <code>pytest</code> in your terminal/command prompt from the same folder where your files exist to execute the tests.

