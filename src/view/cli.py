# TODO delete this whole file probably or is this just the "View"?
import click
from src.view.inputs import Inputs
from src.view.style import Style


class View:  # parent of all views ?
    def __init__(self):
        self.inputs = Inputs()
        self.style = Style()

    def my_print(self, menu_calling:"Menu", statement: str):
        # TODO include style and stuff to print using click
        click.echo(statement)


if __name__ == "__main__":
    _view = View()
    _view.inputs.ask_prompt
