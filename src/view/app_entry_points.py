import click
import src.controller.menus.mainMenu


@click.command()
def start_app():
    src.controller.menus.mainMenu.main_menu()
