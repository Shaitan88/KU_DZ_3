import toml
import re


def parse_toml_with_const_refs(toml_file_path):
    """
    Парсит TOML-файл, извлекает значения констант, переменных,
    разрешает ссылки на константы, выводит словари и строки.
    """
    try:
        # Читаем TOML-файл и преобразуем в структуру данных Python
        with open(toml_file_path, 'r', encoding='utf-8') as file:
            toml_string = file.read()
            data = toml.loads(toml_string)
    except FileNotFoundError:
        print(f"Ошибка: файл {toml_file_path} не найден.")
        return
    except toml.TomlDecodeError as e:
        print(f"Ошибка при парсинге TOML: {e}")
        return

    # Получаем константы из TOML
    constants = data.get("constants", {})

    print("\nОбъявление константы на этапе трансляции:")
    for const_key, const_value in constants.items():
        print(f"{const_key}: {const_value}")

    print("\nВычисление константы на этапе трансляции:")
    for table_name, table_content in data.items():
        # двойная проверка является ли таблица словарем и является ли переменная константой (ниже)
        if isinstance(table_content, dict) and table_name != "constants":
            for key, value in table_content.items():
                if isinstance(value, str) and value.startswith("^"):
                    print(f"  ^{value[1:]}")

    print("\nСловари:")
    for table_name, table_content in data.items():
        if isinstance(table_content, dict):
            if table_name != "constants":
                print(f"{table_name} {{")
                for key, value in table_content.items():
                    if isinstance(value, str) and value.startswith("^"): # двойная проверка является ли строкой и начинается с "^"
                        ref_name = value[1:]
                        print(
                            f'  {key} = {constants.get(ref_name, "Ошибка: константа не найдена")} (^' + f"{ref_name});")
                    else:
                        print(f'  {key} = {value};')
                print("}")
    if constants:
        print("constants {")
        for key, value in constants.items():
            print(f'  {key} : {value};')
        print("}")

    print("\nСтроки:")
    strings = re.findall(r'("[^"]*")', toml_string)
    for s in strings:
        if not (s.startswith('"^') and s.endswith('"')):
            print(f"[[{s[1:-1]}]]")


# Пример использования
file_path = "example.toml"
parse_toml_with_const_refs(file_path) #вызов функции парсера