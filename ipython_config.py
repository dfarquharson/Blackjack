get_config().InteractiveShellApp.exec_lines = \
    [
        '%load_ext autoreload',
        '%autoreload 2',
        'import toolz.curried as T',
        'import game',
        'import model'
    ]
print("---------->>>>>>>>>> CUSTOM CONFIG LOADED <<<<<<<<<<----------")
