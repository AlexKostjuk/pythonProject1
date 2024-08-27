import hashlib
import time

import psycopg2
import wmi
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from datetime import timedelta
import tkinter as tk


DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'Admin1'
DB_PASSWORD = 'Power1983'


datetime_madege = datetime.datetime.now()
datetime_db = datetime.datetime.now()

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # hashed_password = hash_password(password)

        cursor.execute("SELECT * FROM auth_user WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None




def call_function():
    arg1 = entry1.get()
    arg2 = entry2.get()
    work(arg1, arg2)

def create_gui():
    global entry1, entry2
    root = tk.Tk()
    root.title("Пример GUI")

    call_button = tk.Button(root, text="Вызвать sensor_psname", command=work)

    call_button.pack(pady=20)
    tk.Label(root, text="Аргумент 1:").pack(pady=5)
    entry1 = tk.Entry(root)
    entry1.pack(pady=5)

    tk.Label(root, text="Аргумент 2:").pack(pady=5)
    entry2 = tk.Entry(root)
    entry2.pack(pady=5)

    call_button = tk.Button(root, text="Вызвать функцию", command=call_function)
    call_button.pack(pady=20)

    root.mainloop()



def get_all_sensors():
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        sensor_info = w.Sensor()
        sensors = {}
        for sensor in sensor_info:
            sensors[sensor.Name] = {
                "Type": sensor.SensorType,
                "Value": sensor.Value,
                "Min": sensor.Min,
                "Max": sensor.Max
            }
        return sensors
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return {}

def get_computer_name():
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Ошибка при получении имени компьютера: {e}")
        return "Unknown"



def compare_and_update_nested_dicts(main_dict1, main_dict2):
    updated_dict = main_dict1.copy()

    for key in updated_dict.keys():
        if key in main_dict2:
            nested_dict1 = updated_dict[key]
            nested_dict2 = main_dict2[key]

            for nested_key in nested_dict1.keys():
                if nested_key in nested_dict2 and nested_dict2[nested_key] > nested_dict1[nested_key]:
                    nested_dict1[nested_key] = nested_dict2[nested_key]

    return updated_dict

all_sensors = get_all_sensors()
computer_name = get_computer_name()
main_dict1 = get_all_sensors()

main_dict2 = {}



data = {
    "ComputerName": computer_name,
    "Sensors": all_sensors
}

print(all_sensors)

def work(username, password):
    user = authenticate(username, password)

    if user:
        while True:
            main_dict2= get_all_sensors()
            main_dict1 = compare_and_update_nested_dicts(main_dict1, main_dict2)
            print(main_dict1)
            alarm = (main_dict1['CPU Core #4']['Value'])
            print(alarm)
            print(datetime_madege)
            datetime_naw = datetime.datetime.now()
            if alarm > 50 and datetime_madege + timedelta(minutes=5) < datetime_naw :
                datetime_madege = datetime.datetime.now()
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                username = "alkost198333@gmail.com"
                password = "jkzv lbdn qlrw emsa"

                # Налаштування електронного листа
                from_email = "alkost198333@gmail.com"
                to_email = "alkost1983333@outlook.com"
                subject = "alarm Temp"
                body = f"temp CP = {alarm}."


                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = to_email
                msg['Subject'] = subject


                msg.attach(MIMEText(body, 'plain'))


                try:

                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(username, password)


                    server.send_message(msg)
                    print("Лист успішно відправлений!")

                except Exception as e:
                    print(f"Помилка: {e}")

                finally:
                    server.quit()


            # if datetime_db + timedelta(minutes=5) > datetime_naw:
            #     datetime_db =datetime.datetime.now()
            #     current_date = datetime_naw.date()
            #     current_time = datetime_naw.time()



            time.sleep(2)

create_gui()