"""Context to be shared between all menus."""

from typing import Optional


class Context:
    """Object shared between all menus.

    Keep track of tournament, round and match IDs.
    """

    def __init__(self):
        self.current_tournament_id: Optional[int]
        self.current_round_id: Optional[int]
        self.current_match_id: Optional[int]

    def __repr__(self):
        return (
            "IDs: "
            f"T:{self.current_tournament_id}|"
            f"R:{self.current_round_id}|"
            f"M:{self.current_match_id}"
        )
