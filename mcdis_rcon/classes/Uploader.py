class Uploader:
    def __init__(self) -> None:
        self.is_running = False
        self.overwrite = False
        self.path_to_upload = '.'
