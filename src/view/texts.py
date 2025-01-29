class Option:
    def __init__(
        self, default_order: int, description: str, display_condition: function = None
    ):
        self.default_order = default_order
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


    def organize_options(self, options:list[Option])->list[Option]:
        remaining_options = []
        for option in options:
            if option.display_condition is not None:
                if option.display_condition() is False:
                    continue
            remaining_options.append(option)
        
        for i, option in enumerate(remaining_options):
            option.default_order = i+1


class MainMenu(Text):
    def __init__(self, display_continue_tournament_condition: function):
        title = """Main menu:"""
        options = [
            Option(
                1,
                "Continuer le tournoi précédent",
                display_continue_tournament_condition,
            ),
            Option(2, "Créer un nouveau tournoi"),
            Option(3, "Ajouter de nouveaux joueurs"),
            Option(4, "Consulter les rapports"),
        ]
        
        super().__init__(title=title, options=options)