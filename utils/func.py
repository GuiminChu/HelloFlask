class Func():

    @staticmethod
    def camel_to_snake(camel_str):
        snake_str = ''.join(['_' + c.lower() if c.isupper() else c for c in camel_str])
        return snake_str.lstrip('_')

    @staticmethod
    def snake_to_camel(snake_str):
        parts = iter(snake_str.split("_"))
        return next(parts) + "".join(i.title() for i in parts)

    @staticmethod
    def _convert_keys(data, convert_func):
        if isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                new_key = convert_func(key)
                new_data[new_key] = Func._convert_keys(value, convert_func)
            return new_data
        elif isinstance(data, list):
            return [Func._convert_keys(item, convert_func) for item in data]
        else:
            return data

    # 将 JSON 数据中的驼峰键转换为下划线键
    @staticmethod
    def convert_camel_to_snake(json_data):
        return Func._convert_keys(json_data, Func.camel_to_snake)

    # 将 JSON 数据中的下划线键转换为驼峰键
    @staticmethod
    def convert_snake_to_camel(json_data):
        return Func._convert_keys(json_data, Func.snake_to_camel)
