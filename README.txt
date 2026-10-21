=====================================================================
                   P22. HABIT TRACKER - README
=====================================================================

STUDENT INFORMATION
-------------------
Name: YOUR NAME
Register Number: YOUR REG NO
Course: Programming in Python
Assignment Title: P22. Habit Tracker (Terminal Text-Menu Project)


PROJECT OVERVIEW
----------------
P22 Habit Tracker is a pure Python 3 terminal-based application designed
for tracking personal habits, monitoring streaks across months, years,
and leap years, displaying weekly performance grids, and calculating
30-day completion statistics.

The project is written strictly following beginner-friendly programming
standards taught in introductory college Python courses:
- Plain loops (for, while), conditional statements (if/elif/else),
  dictionaries, and lists.
- NO classes, NO lambdas, NO list comprehensions, NO decorators,
  NO type hints, and NO walrus operators.
- ABSOLUTELY ZERO import statements (no datetime, no os, no sys, no math).
  All date calculations, validations, and calendars are implemented
  from scratch by hand.


HOW TO RUN THE PROGRAM
----------------------
1. Ensure Python 3 is installed on your computer.
2. Open a terminal / command prompt in this project directory.
3. Run the command:
      python main.py
4. When prompted, enter today's date in DD-MM-YYYY format (e.g. 21-10-2026).
5. Use the numerical text menu (options 1 to 8) to navigate the app.


DATA STORAGE FORMAT
-------------------
All data is stored in plain text files using the pipe ('|') delimiter:

1. habits.txt:
   Format: HabitID|HabitName|WeeklyTarget|Status
   Example: H1|Morning walk|5|ACTIVE
   - Status can be ACTIVE or PAUSED.
   - Habit IDs are auto-generated (H1, H2, H3...).

2. log.txt:
   Format: HabitID|Date
   Example: H1|21-10-2026
   - Dates are stored as DD-MM-YYYY strings.

3. weekly_report.txt (Bonus):
   - Automatically generated each time the user views Option 5 (Weekly Grid).
   - Formatted as a readable text report with days of the week and completion ratios.


FEATURES COMPLETED
------------------
1. Add a Habit (Option 1):
   - User inputs a habit name and a weekly target (1 to 7 days).
   - Validates that names are non-empty and do not contain '|'.
   - Auto-generates unique IDs (H1, H2, H3...) based on the highest existing ID.
   - Automatically saves to habits.txt.

2. Pause / Resume or Delete a Habit (Option 2):
   - Toggle status between ACTIVE and PAUSED.
   - Delete habit: safely removes habit from habits.txt and permanently cleans
     up all corresponding log entries from log.txt after user confirmation.

3. Mark a Habit Done for a Date (Option 3):
   - Allows quick marking for today (press Enter) or custom DD-MM-YYYY date.
   - Rejects marking PAUSED habits.
   - Prevents duplicate completion entries for the same habit on the same date.
   - Updates current streak immediately and congratulates user when a milestone
     badge is unlocked.

4. View Streaks & Milestone Badges (Option 4):
   - Computes Current Streak counting back from today (or from yesterday if today
     is not yet marked).
   - Computes Longest Streak across all history by sorting dates chronologically.
   - Accurately tracks streaks across month ends (e.g. 30-09 to 01-10),
     year boundaries (e.g. 31-12 to 01-01), and leap days (e.g. 28-02-2028 to 29-02-2028).

5. Weekly Grid for Any Week (Option 5):
   - User inputs any date in DD-MM-YYYY format (or presses Enter for today).
   - Calculates the Monday of that week using hand-written weekday() arithmetic.
   - Displays a clean visual grid (Y for done, - for not done) across Mon-Sun
     along with Done/Target ratios.

6. 30-Day Completion Percentage (Option 6):
   - Calculates habit adherence over a rolling 30-day window ending on today.
   - Shows completed days out of 30 and formatted completion percentages.

7. Overdue Habits (Option 7):
   - Identifies all ACTIVE habits that have not been completed for 3 or more days.
   - Explicitly flags active habits that have never been logged yet.
   - Ignores paused habits.

8. Exit (Option 8):
   - Cleanly closes the program.

9. Robust Error Handling:
   - Works on the very first run when files don't exist (catches FileNotFoundError).
   - Validates integers with clear out-of-range and invalid input prompts.
   - Rejects the '|' delimiter to protect file integrity.
   - Validates calendar dates (correct month lengths, leap years, valid ranges).


BONUS FEATURES COMPLETED
------------------------
1. Auto-Saving Weekly Reports:
   Every time Option 5 (Weekly Grid) is displayed, the complete formatted table
   is saved to weekly_report.txt.
2. Milestone Badges:
   Badges are awarded and displayed in Option 4 for maintaining streaks:
   - 7-Day Bronze Badge (Habit Starter)
   - 21-Day Silver Badge (Habit Master)
   - 50-Day Gold Badge (Habit Legend)


DATE ARITHMETIC IMPLEMENTATION (HAND-WRITTEN)
---------------------------------------------
- is_leap_year(year): Hand-written Gregorian calendar leap year rule.
- days_in_month(month, year): Days in February (28 or 29) and remaining months.
- is_valid_date(text): Validates DD-MM-YYYY format and real calendar dates.
- to_number(date): Converts DD-MM-YYYY to YYYYMMDD integer for comparisons.
- next_day(date) & prev_day(date): Accurately rolls dates across month/year/leap bounds.
- days_between(d1, d2): Counts signed elapsed days between two dates.
- weekday(date): Uses anchor date 12-10-2026 (a known Monday) with modulo 7
  arithmetic, correctly handling dates before and after the anchor.


KNOWN PROBLEMS / LIMITATIONS
----------------------------
- None. The program handles edge cases, empty datasets, invalid dates,
  non-numeric entries, and delimiter injections cleanly without crashing.
