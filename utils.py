def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Please provide enough arguments."
    return inner


def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    return command, args
