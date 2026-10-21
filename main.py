# =====================================================================
# Student Name: YOUR NAME
# Register Number: YOUR REG NO
# Project Title: P22. Habit Tracker
# Course: Programming in Python
# Description: A beginner-friendly terminal text-menu habit tracker
#              written without any external or built-in modules.
# =====================================================================

HABITS_FILE = "habits.txt"
LOG_FILE = "log.txt"
REPORT_FILE = "weekly_report.txt"
MAX_TARGET = 7
OVERDUE_DAYS = 3
WINDOW_DAYS = 30

# ---------------------------------------------------------------------
# DATE FUNCTIONS (Written by hand, no datetime library)
# ---------------------------------------------------------------------

def is_leap_year(year):
    # Century years must be divisible by 400
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


def days_in_month(month, year):
    # February has 29 days in a leap year, 28 in a regular year
    if month == 2:
        if is_leap_year(year):
            return 29
        else:
            return 28
    # Months with 30 days
    if month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    # All other months have 31 days
    return 31


def is_valid_date(text):
    # Validate format DD-MM-YYYY
    parts = text.split("-")
    if len(parts) != 3:
        return False
    day_str = parts[0]
    month_str = parts[1]
    year_str = parts[2]
    if len(day_str) != 2 or len(month_str) != 2 or len(year_str) != 4:
        return False
    if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
        return False
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)
    if year < 1900 or year > 2100:
        return False
    if month < 1 or month > 12:
        return False
    max_days = days_in_month(month, year)
    if day < 1 or day > max_days:
        return False
    return True


def to_number(date):
    # Convert DD-MM-YYYY to YYYYMMDD integer for safe comparisons
    parts = date.split("-")
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    return year * 10000 + month * 100 + day


def next_day(date):
    # Calculate the next calendar day
    parts = date.split("-")
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    day = day + 1
    if day > days_in_month(month, year):
        day = 1
        month = month + 1
        if month > 12:
            month = 1
            year = year + 1
    day_str = str(day)
    if len(day_str) < 2:
        day_str = "0" + day_str
    month_str = str(month)
    if len(month_str) < 2:
        month_str = "0" + month_str
    return day_str + "-" + month_str + "-" + str(year)


def prev_day(date):
    # Calculate the previous calendar day
    parts = date.split("-")
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    day = day - 1
    if day < 1:
        month = month - 1
        if month < 1:
            month = 12
            year = year - 1
        day = days_in_month(month, year)
    day_str = str(day)
    if len(day_str) < 2:
        day_str = "0" + day_str
    month_str = str(month)
    if len(month_str) < 2:
        month_str = "0" + month_str
    return day_str + "-" + month_str + "-" + str(year)


def days_between(d1, d2):
    # Returns count of days from d1 to d2
    # Positive if d2 is after d1, negative if d2 is before d1
    if d1 == d2:
        return 0
    num1 = to_number(d1)
    num2 = to_number(d2)
    if num1 < num2:
        count = 0
        cur = d1
        while cur != d2:
            cur = next_day(cur)
            count = count + 1
        return count
    else:
        count = 0
        cur = d1
        while cur != d2:
            cur = prev_day(cur)
            count = count + 1
        return -count


def weekday(date):
    # 12-10-2026 is known to be a Monday (0=Mon, 1=Tue... 6=Sun)
    anchor = "12-10-2026"
    diff = days_between(anchor, date)
    day_num = diff % 7
    if day_num < 0:
        day_num = day_num + 7
    return day_num


# ---------------------------------------------------------------------
# FILE STORAGE FUNCTIONS
# ---------------------------------------------------------------------

def load_habits():
    # Load habits from habits.txt
    habit_list = []
    try:
        file = open(HABITS_FILE, "r")
        for line in file:
            line = line.strip()
            if line != "":
                parts = line.split("|")
                if len(parts) == 4:
                    item = {
                        "id": parts[0].strip(),
                        "name": parts[1].strip(),
                        "target": int(parts[2].strip()),
                        "status": parts[3].strip()
                    }
                    habit_list.append(item)
        file.close()
    except FileNotFoundError:
        pass
    return habit_list


def save_habits(habit_list):
    # Save habits to habits.txt
    file = open(HABITS_FILE, "w")
    for h in habit_list:
        line = h["id"] + "|" + h["name"] + "|" + str(h["target"]) + "|" + h["status"] + "\n"
        file.write(line)
    file.close()


def load_log():
    # Load completion history from log.txt
    log_data = []
    try:
        file = open(LOG_FILE, "r")
        for line in file:
            line = line.strip()
            if line != "":
                parts = line.split("|")
                if len(parts) == 2:
                    item = {
                        "id": parts[0].strip(),
                        "date": parts[1].strip()
                    }
                    log_data.append(item)
        file.close()
    except FileNotFoundError:
        pass
    return log_data


def save_log(log_data):
    # Save completion history to log.txt
    file = open(LOG_FILE, "w")
    for entry in log_data:
        line = entry["id"] + "|" + entry["date"] + "\n"
        file.write(line)
    file.close()


# ---------------------------------------------------------------------
# SAFE INPUT HELPER FUNCTIONS
# ---------------------------------------------------------------------

def read_text(prompt):
    # Read non-empty text and forbid '|' character
    while True:
        text = input(prompt).strip()
        if len(text) == 0:
            print("Error: Input cannot be empty. Please try again.")
        elif "|" in text:
            print("Error: The character '|' is not allowed. Please try again.")
        else:
            return text


def read_int(prompt, low, high):
    # Read an integer within [low, high]
    while True:
        text = input(prompt).strip()
        if len(text) == 0:
            print("Error: Input cannot be empty. Please enter a number.")
            continue
        try:
            val = int(text)
            if val < low or val > high:
                print("Error: Please enter a number between " + str(low) + " and " + str(high) + ".")
            else:
                return val
        except ValueError:
            print("Error: Invalid number. Please enter digits only.")


def read_date_input(prompt, default_date):
    # Read DD-MM-YYYY date or use default if Enter is pressed
    while True:
        text = input(prompt).strip()
        if text == "" and default_date != "":
            return default_date
        if not is_valid_date(text):
            print("Error: Invalid date format or date does not exist. Use DD-MM-YYYY.")
        else:
            return text


# ---------------------------------------------------------------------
# HABIT & STREAK LOGIC HELPERS
# ---------------------------------------------------------------------

def generate_habit_id(habit_list):
    # Generates next ID like H1, H2, H3 based on existing IDs
    max_num = 0
    for h in habit_list:
        hid = h["id"]
        num_str = hid[1:]
        if num_str.isdigit():
            num = int(num_str)
            if num > max_num:
                max_num = num
    return "H" + str(max_num + 1)


def find_habit(habit_list, habit_id):
    # Find habit dictionary by ID
    for h in habit_list:
        if h["id"].upper() == habit_id.upper():
            return h
    return None


def is_done_on_date(habit_id, date, log_data):
    # Check if a habit was marked done on a specific date
    for entry in log_data:
        if entry["id"].upper() == habit_id.upper() and entry["date"] == date:
            return True
    return False


def get_habit_dates(habit_id, log_data):
    # Get all unique dates logged for a habit
    dates = []
    for entry in log_data:
        if entry["id"].upper() == habit_id.upper():
            already = False
            for d in dates:
                if d == entry["date"]:
                    already = True
            if not already:
                dates.append(entry["date"])
    return dates


def get_current_streak(habit_id, log_data, today_date):
    # Counts back from today, or yesterday if today is not yet marked
    cur = today_date
    if is_done_on_date(habit_id, cur, log_data):
        streak = 0
        while is_done_on_date(habit_id, cur, log_data):
            streak = streak + 1
            cur = prev_day(cur)
        return streak
    else:
        cur = prev_day(today_date)
        streak = 0
        while is_done_on_date(habit_id, cur, log_data):
            streak = streak + 1
            cur = prev_day(cur)
        return streak


def get_longest_streak(habit_id, log_data):
    # Find longest streak by sorting logged dates and counting consecutive days
    dates = get_habit_dates(habit_id, log_data)
    if len(dates) == 0:
        return 0
    n = len(dates)
    for i in range(n):
        for j in range(0, n - i - 1):
            if to_number(dates[j]) > to_number(dates[j + 1]):
                temp = dates[j]
                dates[j] = dates[j + 1]
                dates[j + 1] = temp
    longest = 1
    current = 1
    for i in range(len(dates) - 1):
        if dates[i + 1] == next_day(dates[i]):
            current = current + 1
            if current > longest:
                longest = current
        else:
            current = 1
    return longest


def get_badges(streak_count):
    # Unlocks milestone badges for 7, 21, and 50 day streaks
    badges = []
    if streak_count >= 7:
        badges.append("7-Day Bronze")
    if streak_count >= 21:
        badges.append("21-Day Silver")
    if streak_count >= 50:
        badges.append("50-Day Gold")
    if len(badges) == 0:
        return "None"
    result = ""
    for i in range(len(badges)):
        if i > 0:
            result = result + ", "
        result = result + badges[i]
    return result


# ---------------------------------------------------------------------
# MENU OPTION FUNCTIONS (About 40 lines or fewer each)
# ---------------------------------------------------------------------

def option_add_habit(habit_list):
    print("\n--- Add a New Habit ---")
    name = read_text("Enter habit name: ")
    prompt = "Enter weekly target (1 to " + str(MAX_TARGET) + " days): "
    target = read_int(prompt, 1, MAX_TARGET)
    new_id = generate_habit_id(habit_list)
    new_habit = {
        "id": new_id,
        "name": name,
        "target": target,
        "status": "ACTIVE"
    }
    habit_list.append(new_habit)
    save_habits(habit_list)
    print("Success: Added '" + name + "' as " + new_id + " (Target: " + str(target) + " days/week).")


def delete_habit_logs(hid, log_data):
    # Remove all log entries belonging to a habit ID
    i = 0
    while i < len(log_data):
        if log_data[i]["id"].upper() == hid:
            del log_data[i]
        else:
            i = i + 1


def option_manage_habit(habit_list, log_data):
    print("\n--- Pause / Resume / Delete a Habit ---")
    if len(habit_list) == 0:
        print("No habits found. Please add a habit first.")
        return
    for h in habit_list:
        print("  [" + h["id"] + "] " + h["name"] + " (" + h["status"] + ")")
    print("Actions: 1. Pause | 2. Resume | 3. Delete | 4. Back")
    choice = read_int("Enter choice (1-4): ", 1, 4)
    if choice == 4:
        return
    hid = read_text("Enter Habit ID: ").upper()
    habit = find_habit(habit_list, hid)
    if habit is None:
        print("Error: Habit ID '" + hid + "' not found.")
        return
    if choice == 1:
        if habit["status"] == "PAUSED":
            print("Habit " + hid + " is already PAUSED.")
        else:
            habit["status"] = "PAUSED"
            save_habits(habit_list)
            print("Success: Habit " + hid + " is now PAUSED.")
    elif choice == 2:
        if habit["status"] == "ACTIVE":
            print("Habit " + hid + " is already ACTIVE.")
        else:
            habit["status"] = "ACTIVE"
            save_habits(habit_list)
            print("Success: Habit " + hid + " is now ACTIVE.")
    elif choice == 3:
        confirm = read_text("Delete habit " + hid + " and all its logs? (y/n): ").lower()
        if confirm == "y" or confirm == "yes":
            habit_list.remove(habit)
            save_habits(habit_list)
            delete_habit_logs(hid, log_data)
            save_log(log_data)
            print("Success: Deleted habit " + hid + " and all its log records.")
        else:
            print("Deletion cancelled.")


def option_mark_done(habit_list, log_data, today_date):
    print("\n--- Mark a Habit Done ---")
    if len(habit_list) == 0:
        print("No habits found. Please add a habit first.")
        return
    for h in habit_list:
        print("  [" + h["id"] + "] " + h["name"] + " (" + h["status"] + ")")
    hid = read_text("Enter Habit ID: ").upper()
    habit = find_habit(habit_list, hid)
    if habit is None:
        print("Error: Habit ID '" + hid + "' not found.")
        return
    if habit["status"] == "PAUSED":
        print("Error: Cannot mark a PAUSED habit done. Please resume it first.")
        return
    prompt = "Enter date (DD-MM-YYYY) [press Enter for today: " + today_date + "]: "
    done_date = read_date_input(prompt, today_date)
    if is_done_on_date(hid, done_date, log_data):
        print("Notice: Habit " + hid + " is already marked done on " + done_date + ".")
        return
    new_entry = {"id": hid, "date": done_date}
    log_data.append(new_entry)
    save_log(log_data)
    print("Success: Marked habit " + hid + " (" + habit["name"] + ") done for " + done_date + "!")
    streak = get_current_streak(hid, log_data, today_date)
    print("Current streak for " + hid + ": " + str(streak) + " day(s).")
    if streak == 7:
        print("[Bonus Badge] Congratulations! You reached a 7-day streak! (Bronze)")
    elif streak == 21:
        print("[Bonus Badge] Great commitment! You reached a 21-day streak! (Silver)")
    elif streak == 50:
        print("[Bonus Badge] Extraordinary dedication! You reached a 50-day streak! (Gold)")


def option_show_streaks(habit_list, log_data, today_date):
    print("\n--- Habit Streaks & Milestone Badges ---")
    if len(habit_list) == 0:
        print("No habits found.")
        return
    header = "ID".ljust(4) + " " + "Habit Name".ljust(19) + " " + "Current".ljust(11) + " " + "Longest".ljust(11) + " Badges"
    print(header)
    print("-" * 65)
    for h in habit_list:
        hid = h["id"]
        cur = get_current_streak(hid, log_data, today_date)
        longest = get_longest_streak(hid, log_data)
        if cur > longest:
            longest = cur
        badges = get_badges(longest)
        name_col = h["name"]
        if len(name_col) > 18:
            name_col = name_col[:15] + "..."
        name_col = name_col.ljust(19)
        id_col = hid.ljust(4)
        cur_col = (str(cur) + " days").ljust(11)
        long_col = (str(longest) + " days").ljust(11)
        print(id_col + " " + name_col + " " + cur_col + " " + long_col + " " + badges)
    print("-" * 65)


def option_weekly_grid(habit_list, log_data, today_date):
    print("\n--- Weekly Habit Grid ---")
    if len(habit_list) == 0:
        print("No habits found.")
        return
    prompt = "Enter date in week (DD-MM-YYYY) [press Enter for today: " + today_date + "]: "
    chosen_date = read_date_input(prompt, today_date)
    w = weekday(chosen_date)
    monday = chosen_date
    for i in range(w):
        monday = prev_day(monday)
    week_days = []
    cur = monday
    for i in range(7):
        week_days.append(cur)
        cur = next_day(cur)
    sunday = week_days[6]
    lines = ["Week " + monday + " to " + sunday,
             "Habit           Mon Tue Wed Thu Fri Sat Sun   Done/Target"]
    for h in habit_list:
        name = h["name"]
        if len(name) > 15:
            name = name[:12] + "..."
        row = name.ljust(16)
        done_count = 0
        for d in week_days:
            if is_done_on_date(h["id"], d, log_data):
                row = row + " Y  "
                done_count = done_count + 1
            else:
                row = row + " -  "
        lines.append(row + "  " + str(done_count) + "/" + str(h["target"]))
    report_text = ""
    for line in lines:
        print(line)
        report_text = report_text + line + "\n"
    file = open(REPORT_FILE, "w")
    file.write(report_text)
    file.close()
    print("\n[Bonus] Saved weekly report to " + REPORT_FILE)


def option_completion_percentage(habit_list, log_data, today_date):
    print("\n--- 30-Day Completion Percentage ---")
    if len(habit_list) == 0:
        print("No habits found.")
        return
    day_list = []
    cur = today_date
    for i in range(WINDOW_DAYS):
        day_list.append(cur)
        cur = prev_day(cur)
    oldest_day = day_list[WINDOW_DAYS - 1]
    print("Window: " + oldest_day + " to " + today_date + " (" + str(WINDOW_DAYS) + " days)")
    header = "ID".ljust(4) + " " + "Habit Name".ljust(19) + " " + "Status".ljust(10) + " " + "Done/Total".ljust(12) + " " + "Percentage".rjust(10)
    print(header)
    print("-" * 62)
    for h in habit_list:
        done_count = 0
        for d in day_list:
            if is_done_on_date(h["id"], d, log_data):
                done_count = done_count + 1
        pct = round((done_count * 100.0) / WINDOW_DAYS, 1)
        name_col = h["name"]
        if len(name_col) > 18:
            name_col = name_col[:15] + "..."
        name_col = name_col.ljust(19)
        id_col = h["id"].ljust(4)
        status_col = h["status"].ljust(10)
        done_col = (str(done_count) + "/" + str(WINDOW_DAYS)).ljust(12)
        pct_col = (str(pct) + "%").rjust(10)
        print(id_col + " " + name_col + " " + status_col + " " + done_col + " " + pct_col)
    print("-" * 62)


def option_overdue_habits(habit_list, log_data, today_date):
    print("\n--- Overdue Habits (Active Habits Not Done for " + str(OVERDUE_DAYS) + "+ Days) ---")
    overdue_found = False
    for h in habit_list:
        if h["status"] == "ACTIVE":
            dates = get_habit_dates(h["id"], log_data)
            if len(dates) == 0:
                overdue_found = True
                print("  [" + h["id"] + "] " + h["name"] + " - Never done yet! (Target: " + str(h["target"]) + " days/week)")
            else:
                latest = dates[0]
                for d in dates:
                    if to_number(d) > to_number(latest):
                        latest = d
                gap = days_between(latest, today_date)
                if gap >= OVERDUE_DAYS:
                    overdue_found = True
                    print("  [" + h["id"] + "] " + h["name"] + " - Last done on " + latest + " (" + str(gap) + " days ago)")
    if not overdue_found:
        print("Great news! All active habits are up to date (done within the last " + str(OVERDUE_DAYS) + " days).")


# ---------------------------------------------------------------------
# MAIN MENU LOOP
# ---------------------------------------------------------------------

def print_menu(today_date):
    # Print the available menu choices
    print("\n" + "=" * 55)
    print("                 MAIN MENU")
    print("=" * 55)
    print("Today's Date: " + today_date)
    print("1. Add a habit")
    print("2. Pause / resume or delete a habit")
    print("3. Mark a habit done for a date")
    print("4. View streaks and badges")
    print("5. View weekly grid")
    print("6. View 30-day completion percentage")
    print("7. View overdue habits (3+ days inactive)")
    print("8. Exit")
    print("=" * 55)


def main():
    print("=" * 55)
    print("             P22. HABIT TRACKER")
    print("=" * 55)
    print("Welcome to your personal habit tracking assistant.")
    
    # Prompt for today's date once at startup and validate it
    while True:
        today_date = input("Enter today's date (DD-MM-YYYY): ").strip()
        if is_valid_date(today_date):
            break
        print("Error: Invalid date format or date does not exist. Please use DD-MM-YYYY.")
    
    habit_list = load_habits()
    log_data = load_log()
    print("Data loaded successfully. " + str(len(habit_list)) + " habit(s), " + str(len(log_data)) + " log(s).")
    
    while True:
        print_menu(today_date)
        choice = read_int("Enter your choice (1-8): ", 1, 8)
        
        if choice == 1:
            option_add_habit(habit_list)
        elif choice == 2:
            option_manage_habit(habit_list, log_data)
        elif choice == 3:
            option_mark_done(habit_list, log_data, today_date)
        elif choice == 4:
            option_show_streaks(habit_list, log_data, today_date)
        elif choice == 5:
            option_weekly_grid(habit_list, log_data, today_date)
        elif choice == 6:
            option_completion_percentage(habit_list, log_data, today_date)
        elif choice == 7:
            option_overdue_habits(habit_list, log_data, today_date)
        elif choice == 8:
            print("\nThank you for using Habit Tracker. Goodbye!")
            break


if __name__ == "__main__":
    main()
