import yaml
from datetime import datetime

def read_config() -> dict:
    with open('config.yaml', 'r') as stream:
        try: 
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            raise e
        
def convert_string_date_to_epoch(date: str) -> int:
    date_object = datetime.strptime(date, "%Y-%m-%d")
    epoch_time = (date_object - datetime(1970, 1, 1)).total_seconds()
    return epoch_time 
