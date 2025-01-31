class Option:
    def __init__(
        self, command_handle:str, description: str, display_condition: function = None
    ):
        self.command_handle = command_handle
        self.description = description
        self.display_condition = display_condition


class Text:
    def __init__(
        self,
        *,
        title: str = "/!\\ Title missing.",
        paragraph: str = "/!\\ Paragraph missing.",
        options: list[Option] = "/!\\ Options missing."
    ):
        self.title = title
        self.paragraph = paragraph
        self.options = self.organize_options(options)



class MainMenu(Text):
    def __init__(self, display_continue_tournament_condition: function):
        title = """Main menu:"""
        options = [######################################
            Option(
                1,
                "Continuer le tournoi précédent",
                display_continue_tournament_condition,
            ),
            Option(2, "Créer un nouveau tournoi"),
            Option(3, "Ajouter de nouveaux joueurs"),
            Option(4, "Consulter les rapports"),
        ] ##################################################
        
        super().__init__(title=title, options=options)