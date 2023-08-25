"""Auto Sign Schedular."""
# from flask import current_app
from flask_apscheduler import APScheduler
from api.model.employee import Employee
from api.service.greythr_automation import execute_sign_operation


def auto_sign_employees(app, action):
    """Auto Sign All Employees"""
    with app.app_context():
        employees = Employee.query.all()

        for employee in employees:
            try:
                execute_sign_operation(employee=employee, action=action)
            except Exception as err:
                print(f"Error while signing {employee}")
                print(f"[ERROR] {str(err)}")


def setup_schedulers(app, scheduler: APScheduler):
    """Setup schedulers."""
    with app.app_context():
        scheduler.add_job(
            id="auto_sign_in_employees",
            func=auto_sign_employees,
            args=[app, "SignIn"],
            trigger="cron",
            day_of_week="mon-fri",
            hour="9",
        )
        scheduler.add_job(
            id="auto_sign_out_employees",
            func=auto_sign_employees,
            args=[app, "SignOut"],
            trigger="cron",
            day_of_week="mon-fri",
            hour="19",
        )
