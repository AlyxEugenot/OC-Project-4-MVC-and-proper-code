import typing

if typing.TYPE_CHECKING:
    from chess.controller.app import Context


class MenuAbstractItem:
    def __init__(self, menu_option_name: str) -> None:
        self.menu_option_name = menu_option_name
        self.parent: Menu = None

    def execute(self) -> None:
        pass

    def __str__(self) -> str:
        return self.menu_option_name


class Menu(MenuAbstractItem):
    def __init__(self, title: str, menu_option_name: str = None) -> None:
        self.title = title
        self.menu_option_name = (
            menu_option_name if menu_option_name is not None else title
        )
        super().__init__(self.menu_option_name)
        self.children: list[MenuAbstractItem] = []
        self.loop_above = False
        self.context: "Context" = None

    def add_child(self, item: MenuAbstractItem) -> None:
        if item.parent != None:
            raise ValueError("Contient déjà un parent")
        item.parent = self
        self.children.append(item)

        if issubclass(type(item), Menu):
            item.context = self.context

    def execute(self) -> None:
        while True:
            print()
            if self.parent != None:
                print("0", f"Revenir à {self.parent.title}")

            for i, item in enumerate(self.children):
                print(i + 1, item.menu_option_name)

            choice = input("Sélectionne un choix : ")
            # regular_inputs(choice) # TODO

            try:
                choice = int(choice)
            except ValueError:
                pass

            print()

            if choice == 0 and self.parent != None:
                self.on_exit()
                self.parent.execute()

            elif choice > 0 and choice <= len(self.children):
                self.children[choice - 1].execute()

            else:
                print("Input non reconnu.")

            if self.loop_above:
                break

    def on_exit(self):
        pass

    def organize_children(self):
        """Sort children menu first, action second."""
        children, new_children = self.children, []
        for child in children:
            if type(child) is Menu:
                new_children.append(child)
        for child in children:
            if type(child) is Action:
                new_children.append(child)
        self.children = new_children

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{str(self.parent)} > {self.title} > {"|".join(str(x) for x in self.children)}"


def not_implemented():
    print("not implemented")


class Action(MenuAbstractItem):
    def __init__(
        self, menu_option_name: str, callback: typing.Callable = not_implemented
    ) -> None:
        super().__init__(menu_option_name)
        self.callback = callback

    def execute(self) -> None:
        self.callback()

    def connect(self, ext_callback) -> None:
        self.callback = ext_callback

    def __repr__(self):
        return f"Action: {self.menu_option_name}"


def find_menu(menutype: typing.Type[Menu], menu_to_search: Menu) -> Menu | None:
    for child in menu_to_search.children:
        if issubclass(type(child), Menu):
            if type(child) is menutype:
                return child
            found_deeper = find_menu(menutype, child)
            if found_deeper is not None:
                return found_deeper
