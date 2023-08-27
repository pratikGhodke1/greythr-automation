"""Auto Sign Schedular."""

from datetime import datetime
from random import shuffle
from time import sleep
from flask_apscheduler import APScheduler
from api.model.employee import Employee
from api.service.greythr_automation import execute_sign_operation
from api.service.helper import get_sign_action_schedule


def auto_sign_employees(app, action: str):
    """Auto Sign All Employees"""
    print(f"Schedular Triggered at {datetime.now()} for action {action.upper()}")
    with app.app_context():
        employees = Employee.query.all()
        shuffle(employees)
        sleep_times = get_sign_action_schedule(len(employees))

        for employee, sleep_time in zip(employees, sleep_times):
            sleep(sleep_time * 60)
            print(f"Signing {employee.name} at {datetime.now()}")
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
            hour=9,
        )
        scheduler.add_job(
            id="auto_sign_out_employees",
            func=auto_sign_employees,
            args=[app, "SignOut"],
            trigger="cron",
            day_of_week="mon-fri",
            hour=19,
            minute=30,
        )
