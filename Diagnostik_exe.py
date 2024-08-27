import psycopg2
import hashlib
import wmi
import subprocess
import socket



# Настройка подключения к базе данных PostgreSQL
DB_HOST = 'localhost'  # Или IP адрес контейнера Docker
DB_PORT = '5432'  # Порт PostgreSQL
DB_NAME = 'your_db_name'
DB_USER = 'your_db_user'
DB_PASSWORD = 'your_db_password'


def hardware_monitor():

    # Путь к вашему .exe файлу
    path_to_exe = "C:\\Users\\Alex\\PycharmProjects\\Diagnostick\\djangoProjectDiagnostick\\OpenHardwareMonitor\\OpenHardwareMonitor.exe"
    # Запуск .exe файла с правами администратора
    subprocess.run(["powershell", "-Command", f"Start-Process '{path_to_exe}' -Verb RunAs"])


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

# Функция для хэширования пароля (опционально)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Функция для аутентификации пользователя
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

        # Хэширование пароля перед сравнением (если используется хэширование)
        hashed_password = hash_password(password)

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


# Пример функции, которая выполняется после успешного логина
def perform_task():
    # Пример выполнения какой-либо задачи


    all_sensors = get_all_sensors()
    computer_name = get_computer_name()

    data = {
        "ComputerName": computer_name,
        "Sensors": all_sensors
    }

    return data



# Функция для отправки результатов в базу данных
def send_result_to_db(user_id, result):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute("INSERT INTO results (user_id, result) VALUES (%s, %s)", (user_id, result))
        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error connecting to the database: {e}")


def main():
    # Пример запроса логина и пароля у пользователя
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = authenticate(username, password)

    if user:
        print(f"Login successful! Welcome, {username}.")


        # Выполнение задачи
        result = perform_task()
        print(result)

        # Отправка результата в базу данных
        send_result_to_db(user_id=user[0], result=result)
        print("Result has been sent to the database.")
    else:
        print("Login failed! Invalid username or password.")


if __name__ == "__main__":
    main()