###Database communication and needed function and error checks ###
# helper.py
# Database layer — fetches and stores, no high level logic

from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash

auth_db = SQL("sqlite:///databases/auth.db")
main_db = SQL("sqlite:///databases/main.db")


# ── Auth functions ────────────────────────────────────────────

def check_user(email, password, status):
    
    try:
        auth_user = auth_db.execute("SELECT * FROM users WHERE email = ?  AND status = ?", email,status)

        if auth_user:
            check_password = check_password_hash (auth_user[0]["password"],password)
            if check_password:
                return True
        return False
    except Exception as e:
        print(f"Error checking user: {e}")
        return False


def check_admin(email, password, status):
    try:
        auth_admin = auth_db.execute("SELECT * FROM users WHERE email = ?  AND status > 1 AND state =1", email)
       
        if auth_admin:
             check_password = check_password_hash(auth_admin[0]["password"], password)
             if check_password:
                return True
             return False
        return False
    except Exception as e:
        print(f"Error checking admin: {e}")
        return False


def register_user(email, password, status):
    try:
        password = generate_password_hash(password)
        auth_db.execute("INSERT INTO users (email, password, status) VALUES (?, ?, ?)", email, password, status)
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False


def register_admin(email, password, status):
    try:
        password = generate_password_hash(password)
        auth_db.execute("INSERT INTO users (email, password, status, state) VALUES (?, ?, ?, ?)", email, password, status, 0)
        return True
    except Exception as e:
        print(f"Error registering admin: {e}")
        return False

# ── User functions ────────────────────────────────────────────

def get_profile(email):
    try:
        profile_id = main_db.execute("SELECT p_id FROM users WHERE email = ?", email)
        profile = main_db.execute("SELECT * FROM profiles WHERE p_id = ?", profile_id[0]["p_id"])
        if profile:
            return profile[0]
        return None
    except Exception as e:
        print(f"Error getting profile: {e}")
        return None


def update_profile(email, data):
    try:
        profile_id = main_db.execute("SELECT p_id FROM users WHERE email = ?", email)
        update = main_db.execute("UPDATE profiles SET name = ?, age = ?, bio = ? WHERE p_id = ?", data["name"], data["age"], data["bio"], profile_id[0]["p_id"])###need edite affter finsh data base
        if update:
            return True
        return False
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False


def get_subjects(email):
    try:    
        profile_id = main_db.execute("SELECT p_id FROM users WHERE email = ?", email)
        profile = main_db.execute("SELECT * FROM profiles WHERE p_id = ?", profile_id[0]["p_id"])
        profile_subjects = profile[0]["subjects"]
        if profile_subjects:
            subject = main_db.execute("SELECT SUB_ID FROM SUB_TABLE WHERE SUB_ID IN (?) AND SUB_STATUS>0", profile_subjects)
            Subjects = [s["SUB_ID"] for s in subject]
            return Subjects
        return None
    except Exception as e:
        print(f"Error getting subjects: {e}")
        return None



def choose_subject(email, subject_id):
    try:
        profile_id = main_db.execute("SELECT p_id FROM users WHERE email = ?", email)
        profile = main_db.execute("SELECT * FROM profiles WHERE p_id = ?", profile_id[0]["p_id"])
        profile_subjects = profile[0]["subjects"]
        if profile_subjects:
            updated_subjects = profile_subjects + "," + str(subject_id)
        else:
            updated_subjects = str(subject_id)
        update = main_db.execute("UPDATE profiles SET subjects = ? WHERE p_id = ?", updated_subjects, profile_id[0]["p_id"])
        if update:
            return True
        return False
    except Exception as e:
        print(f"Error choosing subject: {e}")
        return False




def create_profile(email, status):
    try:
        main_db.execute("INSERT INTO profiles (email) VALUES (?)", email)
        profile_id = main_db.execute("SELECT p_id FROM profiles WHERE email = ?", email)
        p_id = profile_id[0]["p_id"]
        main_db.execute("INSERT INTO users (email, p_id, status) VALUES (?, ?, ?)", email, p_id, status)
        return p_id
    except Exception as e:
        print(f"Error creating profile: {e}")
        return None

def search_subjects(query, year, semester):
    if not query and not year and not semester:
        res = main_db.execute("SELECT * FROM subjects")
    elif query and not year and not semester:
        res = main_db.execute("SELECT * FROM subjects WHERE name LIKE ? OR code LIKE ?", f"%{query}%", f"%{query}%")
    elif not query and year and not semester:
        res = main_db.execute("SELECT * FROM subjects WHERE year = ?", year)
    elif not query and not year and semester:
        res = main_db.execute("SELECT * FROM subjects WHERE semester = ?", semester)
    elif query and year and not semester:
        res = main_db.execute("SELECT * FROM subjects WHERE (name LIKE ? OR code LIKE ?) AND year = ?", f"%{query}%", f"%{query}%", year)
    elif query and not year and semester:
        res = main_db.execute("SELECT * FROM subjects WHERE (name LIKE ? OR code LIKE ?) AND semester = ?", f"%{query}%", f"%{query}%", semester)
    elif not query and year and semester:
        res = main_db.execute("SELECT * FROM subjects WHERE year = ? AND semester = ?", year, semester)
    else:
        res = main_db.execute("SELECT * FROM subjects WHERE (name LIKE ? OR code LIKE ?) AND year = ? AND semester = ?", f"%{query}%", f"%{query}%", year, semester)
    return res

def get_recommendations(email):
    pass

# ── Rating functions ──────────────────────────────────────────

def rate(email, entity_type, entity_id, rating):
    try:
        profile_id = main_db.execute("SELECT p_id FROM users WHERE email = ?", email)
        if entity_type == "subject":
            main_db.execute("INSERT INTO ratings (p_id, sub_id, rating) VALUES (?, ?, ?)", profile_id[0]["p_id"], entity_id, rating)
        elif entity_type == "course":
            main_db.execute("INSERT INTO ratings (p_id, course_id, rating) VALUES (?, ?, ?)", profile_id[0]["p_id"], entity_id, rating)
        else:
            print(f"Invalid entity type: {entity_type}")
            return False
        return True
    except Exception as e:
        print(f"Error rating {entity_type}: {e}")
        return False