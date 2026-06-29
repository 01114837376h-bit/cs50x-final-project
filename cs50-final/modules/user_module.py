# modules/user/module.py
# User logic layer

import sys
sys.path.append('.')
import helper


def get_profile(email):
    try:
        if not email:
            return {"success": False, "message": "Email is required"}
        profile = helper.get_profile(email)
        if profile:
            return {"success": True, "message": "Profile found", "data": profile}
        return {"success": False, "message": "Profile not found"}
    except Exception as e:
        print(f"Error in get_profile: {e}")
        return {"success": False, "message": "Failed to get profile unexpectedly"}


def update_profile(email, data):
    try:
        if not email or not data:
            return {"success": False, "message": "Email and data are required"}
        update = helper.update_profile(email, data)
        if update:
            return {"success": True, "message": "Profile updated"}
        return {"success": False, "message": "Profile update failed"}
    except Exception as e:
        print(f"Error in update_profile: {e}")
        return {"success": False, "message": "Failed to update profile unexpectedly"}


def get_subjects(email):
    try:
        if not email:
            return {"success": False, "message": "Email is required"}
        subjects = helper.get_subjects(email)
        if subjects:
            return {"success": True, "message": "Subjects found", "data": subjects}
        return {"success": False, "message": "No subjects found"}
    except Exception as e:
        print(f"Error in get_subjects: {e}")
        return {"success": False, "message": "Failed to get subjects unexpectedly"}


def choose_subject(email, subject_id):
    try:
        if not email or not subject_id:
            return {"success": False, "message": "Email and subject ID are required"}
        choose = helper.choose_subject(email, subject_id)
        if choose:
            return {"success": True, "message": "Subject chosen"}
        return {"success": False, "message": "Failed to choose subject"}
    except Exception as e:
        print(f"Error in choose_subject: {e}")
        return {"success": False, "message": "Failed to choose subject unexpectedly"}


def get_recommendations(email):
    try:
        if not email:
            return {"success": False, "message": "Email is required"}
        recommendations = helper.get_recommendations(email)
        if recommendations:
            return {"success": True, "message": "Recommendations found", "data": recommendations}
        return {"success": False, "message": "No recommendations found"}
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        return {"success": False, "message": "Failed to get recommendations unexpectedly"}


def rate(thing, rating, email, thing_id):
    try:
        if not thing or not rating or not email or not thing_id:
            return {"success": False, "message": "All rating fields are required"}
        result = helper.rate(thing, rating, email, thing_id)
        if result:
            return {"success": True, "message": "Rating submitted"}
        return {"success": False, "message": "Failed to submit rating"}
    except Exception as e:
        print(f"Error in rate: {e}")
        return {"success": False, "message": "Failed to submit rating unexpectedly"}



def search_subjects(query, year, semester):
    try:
        subjects = helper.search_subjects(query, year, semester)
        if subjects:
            return {"success": True, "message": "Subjects found", "data": subjects}
        return {"success": False, "message": "No subjects found"}
    except Exception as e:
        print(f"Error in search_subjects: {e}")
        return {"success": False, "message": "Failed to search subjects unexpectedly"}