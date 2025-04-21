"""Base menu elements."""

import typing
from chess.view import View

if typing.TYPE_CHECKING:
    from chess.controller.context import Context


class MenuAbstractItem:
    """Most basic menu element."""

    def __init__(self, menu_option_name: str) -> None:
        self.menu_option_name = menu_option_name
        self.parent: Menu | None = None

    def execute(self) -> None:
        """Function holding the behaviour of the menu object."""

    def __str__(self) -> str:
        return self.menu_option_name


class Menu(MenuAbstractItem):
    """Menu item containing other items.

    Inherit from MenuAbstractItem.
    """

    def __init__(
        self, title: str, menu_option_name: str | None = None
    ) -> None:
        """Menu init.

        Args:
            title (str): Title of the menu. Used on tree view.
            menu_option_name (str | None, optional): Note for menu choices.\
                Defaults to title's content.
        """
        self.title = title
        self.menu_option_name = (
            menu_option_name if menu_option_name is not None else title
        )
        super().__init__(self.menu_option_name)
        self.children: list[MenuAbstractItem] = []
        self.loop_above = False
        self.context: typing.Optional["Context"]
        self.view: typing.Optional[View]
        self.invisible_child: typing.Optional[Menu]

    def add_child(self, item: MenuAbstractItem) -> None:
        """Add child to menu choices.

        Also sets child parent relationship.

        Args:
            item (MenuAbstractItem): Menu item to add.

        Raises:
            ValueError: If already has parent.
        """
        if item.parent is not None:
            raise ValueError("Contient déjà un parent")
        item.parent = self
        self.children.append(item)

        # for late menu creation, late_init takes care of initial arborescence
        if issubclass(type(item), Menu):
            item.context = self.context
            item.view = self.view

    def add_remanent_menu_not_child(self, item: "Menu") -> "Menu":
        """Sets parent relationship to this for item.

        Args:
            item (Menu): Menu item to set.

        Raises:
            ValueError: If already has parent.

        Returns:
            Menu: Menu item set.
        """
        if item.parent is not None:
            raise ValueError("Contient déjà un parent")
        item.parent = self

        return item

    def late_init(self, am_root: bool = False):
        """Init aiming at setting context and view objects to entire tree.

        Called after general init.

        Args:
            am_root (bool, optional): If root object, needs to be True.\
                Defaults to False.
        """
        if not am_root:
            self.context = self.parent.context
            self.view = self.parent.view

        children: list[Menu] = [
            child for child in self.children if issubclass(type(child), Menu)
        ]
        if self.invisible_child is not None:
            children.append(self.invisible_child)

        for child in children:
            child.late_init()

    def execute(self) -> None:
        """For Menu objects, sets up the menu choice.

        If loop_above is True, also execute the inherited function body every\
            time it is called.
        """
        while True:
            self.view.my_print("")
            if self.parent is not None:
                self.view.my_print(f"0, Revenir à {self.parent.title}")

            for i, item in enumerate(self.children):
                self.view.my_print(f"{i + 1}, {item.menu_option_name}")

            choice = self.view.my_input("Sélectionne un choix : ")
            # regular_inputs(choice) # TODO

            try:
                choice = int(choice)
            except ValueError:
                pass

            self.view.my_print("")

            if choice == 0 and self.parent is not None:
                self.on_exit()
                self.parent.execute()

            elif choice > 0 and choice <= len(self.children):
                self.children[choice - 1].execute()

            else:
                self.view.my_print("Input non reconnu.")

            if self.loop_above:
                break

    def on_exit(self):
        """To call behaviour on exiting a menu."""

    def organize_children(self):
        """Sort children menu first, action second."""
        children, new_children = self.children, []
        for child in children:
            if isinstance(child, Menu):
                new_children.append(child)
        for child in children:
            if isinstance(child, Action):
                new_children.append(child)
        self.children = new_children

    def __str__(self):
        return self.title

    def __repr__(self):
        return (
            f"{str(self.parent)} > {self.title} > "
            f"{" | ".join(str(x) for x in self.children)}"
        )


def not_implemented(*args):
    """Default implementation to be overridden."""
    print(
        "not implemented."
        f"{" args entered are"if len(args) > 0 else ""} "
        f"{", ".join([str(arg) for arg in args])}."
    )


class Action(MenuAbstractItem):
    """Menu item NOT containing other items. Only behaviour.

    Inherit from MenuAbstractItem.
    """

    def __init__(
        self,
        menu_option_name: str,
        callback: typing.Callable = not_implemented,
    ) -> None:
        super().__init__(menu_option_name)
        self.callback = callback

    def execute(self) -> None:
        self.callback()

    def __repr__(self):
        return f"Action: {self.menu_option_name}"


def find_menu(
    menutype: typing.Type[Menu], menu_to_search_from: Menu
) -> Menu | None:
    """Find a menu in children.

    Args:
        menutype (Type[Menu]): Menu to search.
        menu_to_search_from (Menu): Menu to search FROM.

    Returns:
        Menu | None: Return menu found or None if not found.
    """
    for child in menu_to_search_from.children:
        if issubclass(type(child), Menu):
            if isinstance(child, menutype):
                return child
            found_deeper = find_menu(menutype, child)
            if found_deeper is not None:
                return found_deeper
    return None
