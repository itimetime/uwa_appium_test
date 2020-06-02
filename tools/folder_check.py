import os
from config.config import project_path

class Floder_check():
    def __init__(self):
        children_folder = ["screenshots", "screenshots-error", "logs"]

        for folder in children_folder:
            if not os.path.exists(os.path.join(project_path, folder)):
                os.makedirs(folder)