import yaml

def read_config() -> dict:
    with open('./src/config.yaml', 'r') as stream:
        try: 
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            raise e