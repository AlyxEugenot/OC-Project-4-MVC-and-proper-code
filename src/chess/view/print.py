"""View prints."""


def my_print(text_to_print: str, menu_arborescence: list[str]):
    """Handle app prints.

    Args:
        text_to_print (str): Text to print.
        menu_arborescence (list[str]): Menu str list for prefix.
    """
    this_prefix = str_prefix(menu_arborescence)

    for line in text_to_print.split("\n"):
        print(f"{this_prefix}{line}")


def str_prefix(menu_arborescence: list[str]) -> str:
    """Prefix to preface all print statements to align with headers.

    Example :
        `┌ Menu 1                  <-- header`
        `├┬ Menu 2                 <-- header`
        `│├─ Action                <-- header`
        `││                        <-- prefixed`
        `││ Other printed things   <-- prefixed`

    Args:
        menu_arborescence (list[str]): Arborescence needed to adapt the prefix.

    Returns:
        str: "│" per menu in arborescence followed by " ".
    """
    arborescence_len = len(menu_arborescence)
    if menu_arborescence[-1].startswith("action"):
        arborescence_len -= 1
    return f"{"│" * arborescence_len} "


def title_headers(menu_arborescence: list[str]):
    """Print headers.

    Example :
        `[empty space]`
        `┌ Menu 1`
        `├┬ Menu 2`
        `│├─ Action`
        `││`
        `││ Other printed things`

    Args:
        menu_arborescence (list[str]): Menu str list for prefix.
    """
    print()
    new_arborescence_list = list(menu_arborescence)
    for index, menu in enumerate(new_arborescence_list):
        if menu.startswith("action"):
            prefix = ["─"]
            menu = menu.removeprefix("action")
        else:
            prefix = ["┬"]

        if index > 0:
            prefix.insert(0, "├")
            if index > 1:
                prefix.insert(0, "│" * (index - 1))
        new_arborescence_list[index] = f"{"".join(prefix)} {menu}"

    if len(new_arborescence_list) < 1:
        new_arborescence_list = [""]
    new_arborescence_list[0] = "┌ Menu principal"

    print("\n".join(new_arborescence_list))

    my_print("", menu_arborescence)
