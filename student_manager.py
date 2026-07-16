import random
import string
import os
from database_cloud import cloud_set_student, cloud_get_student
from qr_manager import generate_qr

PHOTO_DIR = "photos"


# ---------------------------------------------------------
#  UTILITIES
# ---------------------------------------------------------

def generate_student_id():
    """
    Generates a random 6-digit numeric student ID.
    Example: 483920
    """
    return ''.join(random.choices(string.digits, k=6))


def init_photo_dir():
    """
    Creates the local photo directory if needed.
    Only used if you want to store photos locally.
    """
    if not os.path.exists(PHOTO_DIR):
        os.makedirs(PHOTO_DIR)


# ---------------------------------------------------------
#  STUDENT CREATION (FIREBASE-ONLY)
# ---------------------------------------------------------

def create_student(name, grade, photo_path=None):
    """
    Creates a new student profile:
    - Generates student ID
    - Generates QR code
    - Saves photo locally (optional)
    - Saves student record to Firebase
    - Returns student object
    """

    # Generate random 6-digit ID
    student_id = generate_student_id()

    # Generate QR code (returns file path)
    qr_path = generate_qr(student_id)

    # Handle optional photo
    saved_photo_path = ""
    if photo_path:
        init_photo_dir()
        ext = os.path.splitext(photo_path)[1]
        saved_photo_path = os.path.join(PHOTO_DIR, f"{student_id}{ext}")
        os.replace(photo_path, saved_photo_path)

    # Save to Firebase
    cloud_set_student(student_id, {
        "student_id": student_id,
        "name": name,
        "grade": grade,
        "photo_path": saved_photo_path,
        "qr_path": qr_path,
        "last_checkin": ""   # ⭐ CRITICAL FIX
    })

    # Return student object
    return {
        "student_id": student_id,
        "name": name,
        "grade": grade,
        "photo_path": saved_photo_path,
        "qr_path": qr_path,
        "last_checkin": ""
    }


# ---------------------------------------------------------
#  STUDENT RETRIEVAL (FIREBASE-ONLY)
# ---------------------------------------------------------

def get_student(student_id):
    """
    Always fetch student info from Firebase.
    Prevents stale cache issues.
    """
    return cloud_get_student(student_id)
