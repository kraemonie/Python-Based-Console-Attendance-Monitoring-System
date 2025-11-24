import datetime
import os

# Stores accounts in memory
# Format:
# username : { "password": ..., "student_id": ... }
ACCOUNTS = {
    "admin": {
        "password": "admin123",  # Fixed admin password
        "student_id": "Administrator"
    }
}
today = datetime.date.today().strftime("%b %d, %Y")
ATTENDANCE_FILE = f"Attendance Log ({today}).txt"

ATTENDANCE_DATA = []

def register_account():
    print("\n--- Register New Account ---")

    username = input("Enter new username: ").strip()
    if username in ACCOUNTS:
        print("Username already exists!\n")
        return

    password = input("Enter new password: ").strip()
    student_id = input("Enter student name / student ID: ")

    ACCOUNTS[username] = {
        "password": password,
        "student_id": student_id
    }

    print(f"Account created for user '{username}'!\n")


def log_attendance(student_id):
    if has_logged_today(student_id):
        print(f"\nYou have already logged attendance today!\n")
        return
    
    now = datetime.datetime.now()
    dt_string = now.strftime("%b %d, %Y - %I:%M %p") #dt_string = now.strftime("%Y-%m-%d %H:%M:%S") other format
    #file_exists = os.path.isfile(ATTENDANCE_FILE)

    ATTENDANCE_DATA.append(f"User ID: {student_id} - Time: {dt_string}\n")
    print(f"\nAttendance marked for Student {student_id} at {dt_string}\n")


def login():
    print("\n--- LOGIN ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in ACCOUNTS and ACCOUNTS[username]["password"] == password:
        print("\nLogin successful!\n")
        return username  # Return username instead of student_id
    else:
        print("\nInvalid username or password.\n")
        return None


def view_attendance():
    print("\n--- Attendance Records ---")

    if len(ATTENDANCE_DATA) >0:
        for entry in ATTENDANCE_DATA:
            print(entry.strip())
        print()
        
    if not os.path.isfile(ATTENDANCE_FILE):
            if len(ATTENDANCE_DATA) == 0:
                print("\nNo attendance records found.\n")
            return

    try:
        with open(ATTENDANCE_FILE, mode='r') as file:
            lines = file.readlines()

            if len(lines) == 0:
                if len(ATTENDANCE_DATA) == 0:
                    print("Attendance log is currently empty.\n")
                return

            print("Attendance Saved\n")
            for line in lines:
                print(line.strip())
            print()
    except IOError as e:
        print(f"Error reading file: {e}\n")



def clear_attendance():
    with open(ATTENDANCE_FILE, 'w') as file:
        file.write("")  #pano ba mag none d2
    print("\nAttendance log cleared!\n")



def view_accounts():
    print("\n--- Registered Accounts ---")
    for username, info in ACCOUNTS.items():
        print(f"Username: {username} | Password: {info['password']} | Student ID: {info['student_id']}")
    print()

def has_logged_today(student_id):
    if not os.path.isfile(ATTENDANCE_FILE):
        return False

    today = datetime.datetime.now().strftime("%b %d, %Y")

    try:
        with open(ATTENDANCE_FILE, 'r') as file:
            for line in file:
                if student_id in line and today in line:
                    return True
    except IOError:
        pass

    return False
    
def after_view_attendance():  
    while True:
        print("1 - Save the file")
        print("2 - Back")
        choice = input("Enter choice: ").strip()
    
        if choice == "1":
            save_file()
            print(f"\nAttendance log saved as {ATTENDANCE_FILE}.\n")
            break
        
        elif choice == "2":
            break
    
        else:
            print("\nInvalid choice. Try again.\n")

def save_file():
    with open(ATTENDANCE_FILE, 'a') as file:
        for entry in ATTENDANCE_DATA:
            file.write(entry + "\n")
    
    ATTENDANCE_DATA.clear()
    

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1 - View all accounts")
        print("2 - View attendance list")
        print("3 - Clear attendance log")
        print("4 - Register new account")
        print("5 - Logout")
        admin_choice = input("Choose an option: ").strip()

        if admin_choice == "1":
            view_accounts()
        elif admin_choice == "2":
            view_attendance()
            after_view_attendance()
        elif admin_choice == "3":
            clear_attendance()
        elif admin_choice == "4":
            register_account()
        elif admin_choice == "5":
            print("\nAdmin logged out.\n")
            break
        else:
            print("\nInvalid choice. Try again.\n")


    

def main():
    print("--- Group 3's Python Console Attendance System ---")

    while True:
        print("\nOptions:")
        print("1 - Login and log attendance")
        print("2 - View attendance list")
        print("3 - Quit")

        user_action = input("Choose an option (1/2/3): ").strip()

        if user_action == "1":
            username = login()
            if username:
                if username == "admin":
                    admin_menu()
                else:
                    student_id = ACCOUNTS[username]["student_id"]
                    log_attendance(student_id)
                    

        elif user_action == "2":
            view_attendance()
            after_view_attendance()

        elif user_action == "3":
            print("Exiting program...")
            break

        else:
            print("\nInvalid choice. Try again.\n")


if __name__ == "__main__":
    main()

