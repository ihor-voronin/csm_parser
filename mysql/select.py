import shutil
import time
from typing import Dict

import psutil
import pymysql
from win32service import SERVICE_STOP_PENDING

from os_interaction.folders import is_folder_exist
from settings import Settings

from .service import start_or_restart_service, status_service, stop_service


def get_service_directory() -> str:
    service_infos = psutil.win_service_get("mysql")
    service_infos.as_dict()
    full_path = service_infos.binpath()
    path = (full_path.split("bin")[0])[1:]
    return path


def current_database_path() -> str:
    return get_service_directory() + Settings.current_folder


def temp_database_path() -> str:
    return get_service_directory() + Settings.temp_folder


def copy_database_content() -> None:
    stop_service(Settings.service_name)
    shutil.copytree(current_database_path(), temp_database_path())
    print("Database is already copied to csv_parser folder")
    while status_service(Settings.service_name)[1] == SERVICE_STOP_PENDING:
        time.sleep(0.25)


def delete_copied_database_content() -> None:
    if is_folder_exist(temp_database_path()):
        stop_service(Settings.service_name)
        shutil.rmtree(temp_database_path())


def select_balance() -> Dict[int, float]:
    start_or_restart_service(Settings.service_name)
    result = dict()
    try:
        connection = pymysql.connect(
            host=Settings.database_host,
            database=Settings.database_database,
            user=Settings.database_user,
            password=Settings.database_password,
        )
        sql_select_query = """
        SELECT `RemainMoney` 
        FROM `usertb` 
        WHERE `EIType` = '1' 
        AND `UserType` NOT IN ('4', '13', '14', '15') 
        AND `Status` = '1' 
        ORDER BY `UserId` DESC
        """
        cursor = connection.cursor()
        cursor.execute(sql_select_query)
        # get all records
        records = cursor.fetchall()

        for num, row in enumerate(records, start=1):
            result.update({num: float(row[0])})

    except pymysql.connect.Error as e:
        print("Error reading data from MySQL table", e)
        raise Exception("Cannot continue")
    finally:
        connection.close()
        cursor.close()

    return result
