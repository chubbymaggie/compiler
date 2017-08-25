from pprint import pprint

class Environment:
    @staticmethod
    def get_current_env(data):
        env_count = len(data['environments'])
        if env_count == 0:
            return data
        return data['environments'][env_count - 1]

    @staticmethod
    def get_env(data, env_number):
        env_count = len(data['environments'])
        if env_count < env_number:
            return None
        if env_count == env_number:
            return data
        return data['environments'][env_count - env_number - 1]

    @staticmethod
    def store_variable(data, name, value):
        data = Environment.get_current_env(data)
        data['static_variables'][name] = value

    @staticmethod
    def search_variable(data, variable):
        env_counter = 0
        env = Environment.get_env(data, env_counter)
        while env:
            if variable in env['static_variables']:
                return env['static_variables'][variable]
            env_counter += 1
            env = Environment.get_env(data, env_counter)
        return None

    @staticmethod
    def create(data):
        data['environments'].append({
            'static_variables': {}
        })

    @staticmethod
    def clear(data):
        data['environments'].pop()