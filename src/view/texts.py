# class Option:
#     def __init__(
#         self, command_handle:str, description: str, display_condition: callable = None
#     ):
#         self.command_handle = command_handle
#         self.description = description
#         self.display_condition = display_condition


# FIXME
# FIXME text was a way to write and stock all texts here and get them later elsewhere
# FIXME BUT it will be the class that handles text writing (text written elsewhere) and not just a text container
# FIXME SO will be called from the View and not Controller
# FIXME
class Text:
    def __init__(
        self,
        *,
        title: str = "/!\\ Title missing.",
        paragraph: str = "/!\\ Paragraph missing.",
        # options: list[Option] = "/!\\ Options missing."
    ):
        self.title = title
        self.paragraph = paragraph
        # self.options = self.organize_options(options)

    def func_for_all_texts(self, paragraph: str):
        pass
