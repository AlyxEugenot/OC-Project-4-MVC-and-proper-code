import typing


class MenuAbstractItem:
    def __init__(self, menu_option_name: str) -> None:
        self.menu_option_name = menu_option_name
        self.parent: "Menu" = None

    def execute(self) -> None:
        pass

    def __str__(self) -> str:
        return self.menu_option_name


class Menu(MenuAbstractItem):
    def __init__(self, menu_option_name: str, title: str = None) -> None:
        super().__init__(menu_option_name)
        self.title = title if title is not None else menu_option_name
        self.children: list[MenuAbstractItem] = []
        self.loop_above=False

    def add_child(self, item: MenuAbstractItem) -> None:
        if item.parent != None:
            raise ValueError("Contient déjà un parent")
        item.parent = self
        self.children.append(item)

    def execute(self) -> None:
        while True:
            print()
            if self.parent != None:
                print("0", f"Revenir à {self.parent.title}")

            for i, item in enumerate(self.children):
                print(i + 1, item.menu_option_name)

            choice = input("Sélectionne un choix :")
            # regular_inputs(choice) # TODO

            choice = int(choice)
            print()

            if choice == 0 and self.parent != None:
                self.parent.execute()

            elif choice > 0 and choice <= len(self.children):
                self.children[choice - 1].execute()

            else:
                print("Input non reconnu.")
                
            if self.loop_above:
                break

    def organize_children(self):
        """Sort children menu first, action second.
        """
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
        return f"{str(self.parent)} > {self.title} > {"/".join(str(x) for x in self.children)}"


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
