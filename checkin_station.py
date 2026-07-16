from datetime import datetime
from database_cloud import cloud_set_status, cloud_log_attendance, cloud_get_student
from student_manager import get_student


def auto_check(student_id):
    """
    Auto check-in / check-out logic using Firebase only.

    Behavior:
    - If student has no active status → CHECK-IN
    - If student is currently checked in → CHECK-OUT
    """

    # Get student info
    student = get_student(student_id)
    if not student:
        return {"status": "error", "message": "Student not found"}

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current status from Firebase
    status_ref = cloud_get_student(student_id)
    current_status = status_ref.get("status") if status_ref else None

    # ---------------------------------------------------------
    # CHECK-OUT LOGIC
    # ---------------------------------------------------------
    if current_status and current_status.get("state") == "in":
        checkin_time = current_status.get("time")

        # Calculate duration
        t1 = datetime.strptime(checkin_time, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        minutes = (t2 - t1).seconds // 60
        duration = f"{minutes//60}:{minutes%60:02d}"

        # Update Firebase status
        cloud_set_status(student_id, {
            "state": "out",
            "time": now
        })

        # Log attendance entry
        cloud_log_attendance(student_id, {
            "checkin": checkin_time,
            "checkout": now,
            "duration": duration
        })

        return {
            "status": "checkout",
            "student": student,
            "time": now,
            "duration": duration
        }

    # ---------------------------------------------------------
    # CHECK-IN LOGIC
    # ---------------------------------------------------------
    else:
        # Update Firebase status
        cloud_set_status(student_id, {
            "state": "in",
            "time": now
        })

        return {
            "status": "checkin",
            "student": student,
            "time": now
        }
