get_config().InteractiveShellApp.exec_lines = \
    [
        '%load_ext autoreload',
        '%autoreload 2',
        'from pprint import pprint',
        'import toolz.curried as tc',
        'import blackjack as b'
    ]
print("---------->>>>>>>>>> CUSTOM CONFIG LOADED <<<<<<<<<<----------")
