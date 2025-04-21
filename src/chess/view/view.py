"""View object."""

import chess.view.inputs
import chess.view.print


class View:
    """Main View object."""

    def __init__(self):
        """Set all view methods."""
        self.my_input = chess.view.inputs.my_input
        self.my_print = chess.view.print.my_print

        self.create_adress = chess.view.inputs.create_address
        self.get_valid_date = chess.view.inputs.get_valid_date
