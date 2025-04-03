class Context:
    def __init__(self):
        self.current_tournament_id: int | None = None
        self.current_round_id: int | None = None
        self.current_match_id: int | None = None

    def __repr__(self):
        return (
            "IDs: "
            f"T:{self.current_tournament_id}|"
            f"R:{self.current_round_id}|"
            f"M:{self.current_match_id}"
        )
