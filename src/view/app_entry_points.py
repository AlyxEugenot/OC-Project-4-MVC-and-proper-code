import click
import controller.mainMenu


@click.command()
def start_app():
    controller.mainMenu.main_menu()
