"""Auto Sign Schedular."""

from json import dumps
from datetime import datetime, timedelta
from random import shuffle
from time import sleep
from flask_apscheduler import APScheduler
from api.model.employee import Employee
from api.modules.logger import init_logger
from api.service.greythr_automation import execute_sign_operation
from api.service.helper import get_sign_action_schedule

logger = init_logger(__name__, "AUTO_SIGN_SCHEDULER")


def auto_sign_employees(app, action: str):
    """Auto Sign All Employees"""
    logger.info(f"Schedular Triggered at {datetime.now()} for action {action.upper()}")

    with app.app_context():
        employees = Employee.query.all()
        shuffle(employees)
        sleep_times = get_sign_action_schedule(len(employees))
        logger.info(
            dumps(
                [
                    f"{emp.name}: {datetime.now()+timedelta(minutes=sleep_time)}"
                    for emp, sleep_time in zip(employees, sleep_times)
                ],
                indent=4,
            )
        )
        for employee, sleep_time in zip(employees, sleep_times):
            retry = 3
            sleep(sleep_time * 60)
            logger.info(f"Signing {employee.name} at {datetime.now()}")

            while retry:
                try:
                    execute_sign_operation(employee=employee, action=action)
                    break
                except Exception:
                    retry -= 1
                    logger.exception(
                        f"Error while signing {employee}, Retries Remaining: {retry}"
                    )


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
        logger.debug("Schedulers are added")
