import easygui


class FrpManNodeClientExceptionBase(Exception):
    def __init__(self, title, description, solution=None, e=None):
        self.title = title
        self.description = description
        self.solution = solution
        self.e = e
        easygui.msgbox(
            msg=f'Unknown Error\n\n{self.e}',
            title='Error',
            ok_button='Exit',
        )

    def __str__(self):
        return self.description
