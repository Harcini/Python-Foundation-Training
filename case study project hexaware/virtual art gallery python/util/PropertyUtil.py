import os

def load_db_properties():
    # This line finds the correct path to the properties file
    filename = os.path.join(os.path.dirname(__file__), "db.properties")
    props = {}

    with open(filename, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                props[key.strip()] = value.strip()

    return props
