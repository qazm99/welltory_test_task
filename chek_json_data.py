from jsonschema import ValidationError, Draft7Validator
import json
import os


def get_schemas(schemas_directory: str):
    schemas = dict()
    for schema_file in os.listdir(SCHEMA_DIR):
        schema = json.load(open(f'{schemas_directory}\\{schema_file}'))
        schema_name = schema_file.replace('.schema', '')
        schemas.update({schema_name: schema})
    return schemas


def error_clear(error):
    if error.validator == 'required':
        error_string = error.message.replace('is a required property', '').strip()
        error_string = f'Не хватает параметра {error_string}'
    elif error.validator == 'type':
        error_string = f'В параметре \'{error.path.pop()}\' данные \'{error.instance}\' не могут быть преобразованы в тип \'{error.validator_value}\' '
    else:
        error_string = error.message
    return error_string


def chek_data(schemas):
    for data_file in os.listdir(DATA_DIR):
        data = json.load(open(f'{DATA_DIR}\\{data_file}'))
        errors = []
        if data:
            event_data = data.get('event').replace(' ', '')
            if event_data:
                current_schema = schemas.get(event_data)
                if current_schema:
                    try:
                        validator = Draft7Validator(current_schema)
                        clear_data = data.get('data')
                        if clear_data:
                            all_errors = validator.iter_errors(clear_data)
                        else:
                            errors.append('Не хватает в файле блока данных \'data\'')
                        for error_validate in all_errors:
                            current_err = error_clear(error_validate)
                            errors.append(current_err)
                    except ValidationError as e:
                        print(e.message)
                else:
                    errors.append(f"нет схемы для события {event_data}")
            else:
                errors.append(f"нет типа события в файле данных {event_data}")
        else:
            errors.append(f"нет данных в файле {data_file}")

        if len(errors):
            print(f"\n Ошибки в файле {data_file}")
            str_to_file(f"\nОшибки в файле {data_file}")
            for error_in_list in errors:
                print(error_in_list)
                str_to_file(f"-{error_in_list}")
        else:
            print(f"ОК {data_file}")


def str_to_file(string: str, filename='README.md'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.writelines(f"{string}\n")


if __name__ == '__main__':
    SCHEMA_DIR = 'schema'
    DATA_DIR = 'event'
    schemas = get_schemas(SCHEMA_DIR)
    chek_data(schemas)
