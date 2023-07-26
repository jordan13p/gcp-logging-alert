import os, json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from ..services.counts_data import CountsAlertMessage


# set env variables
env_path = str(Path(__file__).parents[2] / '.env')
load_dotenv(dotenv_path = env_path)


class CountsAlertMessageCheck:
    def __init__(self, alert_message_data):
        self.alert_message_data = alert_message_data
        self.dir_path = ""
        self.time_list = []
        self.timestamp = self.alert_message_data['timestamp']
        self.time_file_path = ""

    def create_folder(self):
        # if folder not exists, will be created
        cluster_name = self.alert_message_data.get('cluster_name')
        namespace_name = self.alert_message_data.get('namespace_name')
        container_name = self.alert_message_data.get('container_name')
        self.dir_path = f'./logging_alert/docs/{cluster_name}/{namespace_name}/{container_name}'
        os.makedirs(self.dir_path, exist_ok=True)

    def get_check_time_list(self):
        time_range = self.alert_message_data.get('time_range')

        if not self.time_list or self.time_list is None:
             self.time_list.append(self.timestamp)
             return self.time_list

        else:
            time_delta = (self.timestamp - self.time_list[0])

        if time_delta < time_range:
            self.time_list.append(self.timestamp)
            self.time_list.sort()
            return self.time_list

        else:
            self.time_list.remove(self.time_list[0])
            return self.get_check_time_list()

    def check_time_list(self):
        error_code = self.alert_message_data.get('error_code')
        file_path = f'{self.dir_path}/{error_code}.txt'

        # if file not exists, create it and write time list
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                self.time_list.append(self.timestamp)
                json.dump(self.time_list, file)
            
            return self.time_list

        # if file is exists, read / write time list and check time list
        else:
            with open(file_path,'rb') as file:
                self.time_list = json.load(file)

            self.time_list = self.get_check_time_list()

            with open(file_path, "w") as file:
                json.dump(self.time_list, file)
            
            return self.time_list
    
    def check_send_message_period(self):
        SEND_MESSAGE_PERIOD = os.getenv('SEND_MESSAGE_PERIOD')
        self.time_file_path = f'{self.dir_path}/record_send_time.txt'

        if not os.path.exists(self.time_file_path):
            with open(self.time_file_path, "w") as file:
                file.write(str(datetime.now().timestamp()))

            return False

        with open(self.time_file_path, 'r') as file:
            last_sent_time_str = file.read().strip()

        last_sent_time = datetime.fromtimestamp(float(last_sent_time_str))
        now_time = datetime.now()
        delta = now_time - last_sent_time

        if delta.total_seconds() > int(SEND_MESSAGE_PERIOD):
            send_message_flag = True

        else:
            send_message_flag = False

        return send_message_flag
    
    def write_send_message_time(self):
        send_message_time = datetime.now().timestamp()
        with open(self.time_file_path, "w") as file:
            file.write(str(send_message_time))
