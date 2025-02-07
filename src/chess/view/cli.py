# TODO delete this whole file probably or is this just the "View"?
import click
from chess.view.inputs import *
# from view.style import Style
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.menus import Menu


class View:  # parent of all views ?
    def __init__(self):
        # self.inputs = Inputs()
        # self.style = Style()
        pass

    def my_print(self, menu_calling:"Menu", statement: str):
        # TODO include style and stuff to print using click
        click.echo(statement)
        
    def inputs(self, prompt:str,default_answer:str=None)  ->str  :
        return ask_prompt(prompt, default_answer)


if __name__ == "__main__":
    _view = View()
    print(_view.inputs("bonjour", "oui"))

