class GUI:
    instance = None
    def __init__(self, *args, **kwargs) -> None:
        if GUI.instance == None:
            