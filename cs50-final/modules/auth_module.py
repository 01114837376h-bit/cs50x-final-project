# modules/auth/module.py
# Authentication logic layer
import sys
sys.path.append('.')
import helper as helper


def authenticate_user(email, password, status):
    try:
        if not email or not password or not status:
            return {"success": False, "message": "Email, password and status are required"}
        if int(status) > 1:
            check = helper.check_admin(email, password, status)
        else:
            check = helper.check_user(email, password, status)
        if check:
            return {"success": True, "message": "Authenticated"}
        return {"success": False, "message": "Invalid email or password"}
    except Exception as e:
        print(f"Error in authenticate_user: {e}")
        return {"success": False, "message": "Authentication failed unexpectedly"}


def register_user(email, password, status):
    try:
        if int(status) != 1:
            return {"success": False, "message": "Invalid status for regular user"}
        register = helper.register_user(email, password, status)
        if register:
            return {"success": True, "message": "User registered"}
        return {"success": False, "message": "Registration failed"}
    except Exception as e:
        print(f"Error in register_user: {e}")
        return {"success": False, "message": "Registration failed unexpectedly"}


def register_admin(email, password, status):
    try:
        if int(status) <= 1:
            return {"success": False, "message": "Invalid status for admin"}
        register = helper.register_admin(email, password, status)
        if register:
            return {"success": True, "message": "Admin registered"}
        return {"success": False, "message": "Admin registration failed"}
    except Exception as e:
        print(f"Error in register_admin: {e}")
        return {"success": False, "message": "Admin registration failed unexpectedly"}


def set_profile(email, status):
    try:
        result = helper.create_profile(email, status)
        if result:
            return {"success": True, "message": "Profile created", "p_id": result}
        return {"success": False, "message": "Profile creation failed"}
    except Exception as e:
        print(f"Error in set_profile: {e}")
        return {"success": False, "message": "Profile creation failed unexpectedly"}