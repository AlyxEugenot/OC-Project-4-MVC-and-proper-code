import chess.view
import chess.view.menus._abstract as _abstract
import chess.model as model
import chess.model.generate as generate

class WhichRound(_abstract.Menu): #NON
    def __init__(self, round:model.Round):
        title=f"Round {str(round)}"
        menu_option_name=str(round)
        super().__init__(title,menu_option_name)
class RoundHandling(_abstract.Menu):
    def __init__(self, round:model.Round):
        title=f"Round {str(round)}"
        menu_option_name=str(round)
        self.round = round
        super().__init__(title,menu_option_name)
        self.loop_above=True
    def execute(self):
        while True:
            if type(self.parent) is WhichRound:
                self.parent = self.parent.parent

            self.children.clear()

            if self.round.end_time is not None:
                pass  # TODO ?
            elif self.round.start_time is None:
                pass
        
        super().execute()