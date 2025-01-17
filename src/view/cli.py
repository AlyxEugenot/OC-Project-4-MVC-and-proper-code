import click


class View:  # parent of all views ?
    quitapp = False

    def main(self):
        while not self.quitapp:
            self.cli()

    @click.group()
    def cli():
        pass

    def quit(self):
        self.quitapp = True

    @click.command(name="b")
    def back(self):
        pass


@click.command()
@click.argument("name")
@click.option("--greeting", "-g", default="Bonjour")
def hello_world(name, greeting):
    click.secho("{}, {}".format(greeting, name), fg="blue", bg="white")


@click.command()
@click.argument("end_arg")
@click.option(
    "--same_wording",
    "-g",
    "-other_option_for_same_wording_param",
)
def func(end_arg, same_wording):
    click.echo(f"{same_wording}, {end_arg}")


if __name__ == "__main__":
    _view = View
    _view.main()
    
