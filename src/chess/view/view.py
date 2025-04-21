"""View object."""

import chess.view.inputs
import chess.view.print


class View:
    """Main View object."""

    def __init__(self):
        """Set all view methods."""
        self.current_menu_arborescence: list[str] = ["Menu principal"]
        self.my_input = lambda prompt: chess.view.inputs.my_input(
            prompt, self.current_menu_arborescence, self.regular_inputs
        )
        self.my_print = lambda prompt: chess.view.print.my_print(
            prompt, self.current_menu_arborescence
        )

        self.create_adress = (
            lambda address_context: chess.view.inputs.create_address(
                address_context,
                self.current_menu_arborescence,
                self.regular_inputs,
            )
        )
        self.get_valid_date = lambda: chess.view.inputs.get_valid_date(
            self.current_menu_arborescence, self.regular_inputs
        )
        self.my_print_header = lambda: chess.view.print.title_headers(
            self.current_menu_arborescence
        )
        self.regular_inputs = lambda input: chess.view.inputs.regular_inputs(
            _input=input,
            _my_input=self.my_input,
            quit_callback=self.callback_input_quit,
            cancel_callback=self.callback_input_cancel,
            main_menu_callback=self.callback_input_main_menu,
        )
        self.callback_input_cancel = not_implemented
        self.callback_input_main_menu = not_implemented
        self.callback_input_quit = not_implemented


def not_implemented(*args):
    """Default implementation to be overridden."""
    print(
        "not implemented."
        f"{" args entered are"if len(args) > 0 else ""} "
        f"{", ".join([str(arg) for arg in args])}."
    )
