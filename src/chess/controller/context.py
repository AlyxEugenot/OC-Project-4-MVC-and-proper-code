"""Context to be shared between all menus."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chess.controller.menus._abstract import Menu


class Context:
    """Object shared between all menus.

    Keep track of current menu and IDs of tournament, round and match.
    """

    def __init__(self):
        self.current_tournament_id: int | None = None
        self.current_round_id: int | None = None
        self.current_match_id: int | None = None
        self.current_menu: "Menu" | None = None

    def __repr__(self):
        return (
            "ID: "
            f"T:{self.current_tournament_id}|"
            f"R:{self.current_round_id}|"
            f"M:{self.current_match_id}"
            f" - {self.current_menu.title}"
        )
