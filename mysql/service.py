import logging

import win32serviceutil
from win32service import SERVICE_RUNNING


def start_service(service: str) -> None:
    logging.info("Start MySQL service")
    return win32serviceutil.StartService(service)


def stop_service(service: str) -> None:
    logging.info("Stop MySQL service")
    return win32serviceutil.StopService(service)


def restart_service(service: str) -> None:
    logging.info("Restart MySQL service")
    return win32serviceutil.RestartService(service)


def status_service(service: str) -> tuple:
    return win32serviceutil.QueryServiceStatus(service)


def start_or_restart_service(service: str) -> None:
    if not status_service(service):
        logging.error("MySQL service is NOT installed")
        raise Exception
    if status_service(service)[1] != SERVICE_RUNNING:
        logging.info("MySQL is off")
        return start_service(service)
    if status_service(service)[1] == SERVICE_RUNNING:
        logging.info("MySQL is running now")
        return restart_service(service)
