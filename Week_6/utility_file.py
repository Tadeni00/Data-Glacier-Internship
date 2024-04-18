
import yaml
import logging
import os

def read_yaml_file(file):
    with open(file, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as error:
            logging.error(error)

            
def validate(data, config_data):
    if 'columns' not in config_data:
        print('Error: Missing Columns Dictionary!!!')
        return 0
    
    config_cols = sorted(config_data['columns'])
    df_cols = sorted(data.columns)
    
    data.columns = [x.strip().lower().replace(' ', '_') for x in data.columns]
    
    if len(config_cols) != len(df_cols) or list(config_cols) != list(df_cols):
        print('Error: Invalid number of columns or column names not matching as per config file.')
        return 0
    
    print('Validation Successful')
    return 1
