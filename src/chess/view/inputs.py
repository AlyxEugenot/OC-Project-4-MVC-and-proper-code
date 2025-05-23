"""View inputs."""

from typing import Callable
import datetime
import click
from chess.view import print as _print


def my_input(
    prompt_text: str,
    menu_arborescence: list[str],
    regular_inputs_method: Callable,
    can_be_empty: bool = True,
) -> str:
    """Handle input.

    Args:
        prompt_text (str): Text to preface the input.
        menu_arborescence (list[str]): Menu str list for prefix.
        regular_inputs_method (Callable): regular_inputs method loaded with
            callbacks.
        can_be_empty (bool, optional): If False, force user to not input "".
            Defaults to True.


    Returns:
        str: Returned input.
    """
    this_prefix = _print.str_prefix(menu_arborescence)
    lines = prompt_text.split("\n")
    if len(lines) > 1:
        before_last_line = ("\n").join(lines[:-1])
        _print.my_print(before_last_line, menu_arborescence)

        user_input = input(f"{this_prefix}{lines[-1]}").strip()
    else:
        user_input = input(f"{this_prefix}{prompt_text}").strip()

    regular_inputs_method(user_input)

    if user_input == "" and not can_be_empty:
        _print.my_print("\nNe peut pas être vide.\n", menu_arborescence)
        my_input(
            prompt_text, menu_arborescence, regular_inputs_method, can_be_empty
        )

    return user_input


# def ask_prompt(text_prompt: str, default_text: str = None):
#     if default_text is None:
#         answer = click.prompt(text_prompt, show_default=False)
#     else:
#         answer = click.prompt(text_prompt, default=default_text,
#               show_default=True)
#     return answer


def create_address(
    address_context: str,
    menu_arborescence: list[str],
    regular_inputs_method: Callable,
) -> tuple[str, str, str, str, str, str, str] | None:
    """Create address from user input.

    Args:
        address_context (str): Text to preface the address inputs.
        menu_arborescence (list[str]): Menu str list for prefix.
        regular_inputs_method (Callable): regular_inputs method loaded with
            callbacks.

    Returns:
        tuple[str, str, str, str, str, str, str] | None: Return all address
            fields.
    """
    print(_print.str_prefix(menu_arborescence))  # print("")
    print(
        f"{_print.str_prefix(menu_arborescence).removesuffix("│ ")}├┬─ "
        f"{address_context}"
    )
    menu_arborescence[-1] = menu_arborescence[-1].removeprefix("action")

    suffix = "\n\t\t-> "
    addressee_id = my_input(
        (
            "1. Identification du destinataire : civilité, titre ou qualité "
            "+ prénom + nom.\n\tEx : M. Valéry DUPONT\n\t"
            f"[Generate complete address if empty]{suffix}"
        ),
        menu_arborescence,
        regular_inputs_method,
    )

    if addressee_id == "":
        return None

    delivery_point = my_input(
        (
            "2. Complément d’identification du destinataire ou point de "
            "remise à l’intérieur du bâtiment :\n   N° appartement, boite aux "
            "lettres, étage, couloir.\n\tEx : Appartement 12 Escalier "
            f"C{suffix}"
        ),
        menu_arborescence,
        regular_inputs_method,
        can_be_empty=False,
    )
    additional_geo_info = my_input(
        (
            "3. Facultatif. Complément d’identification du point "
            "géographique – extérieur du bâtiment : \n   entrée, tour, "
            "bâtiment, immeuble, résidence."
            f"\n\tEx : Résidence Les Tilleuls{suffix}"
        ),
        menu_arborescence,
        regular_inputs_method,
    )
    house_nb_street_name = my_input(
        (
            "4. Numéro et libellé de la voie.\n\tEx : 1 impasse de "
            f"l'Eglise{suffix}"
        ),
        menu_arborescence,
        regular_inputs_method,
        can_be_empty=False,
    )
    additional_delivery_info = my_input(
        (
            f"5. Facultatif. Lieu dit ou service particulier de distribution –"
            f" Poste restante, boite postale, etc.\n\tEx : AMAREINS{suffix}"
        ),
        menu_arborescence,
        regular_inputs_method,
    )
    postcode = my_input(
        (
            "6. Code postal et localité de destination.\n\tEx : 01090 "
            f"FRANCHELEINS{suffix}"
        ),
        menu_arborescence,
        regular_inputs_method,
        can_be_empty=False,
    )
    country_name = my_input(
        (f"7. Pays.\n\tEx : FRANCE{suffix}"),
        menu_arborescence,
        regular_inputs_method,
        can_be_empty=False,
    )
    menu_arborescence[-1] = f"action{menu_arborescence[-1]}"

    return (
        addressee_id,
        delivery_point,
        additional_geo_info,  # =""
        house_nb_street_name,
        additional_delivery_info,  # =""
        postcode,
        country_name,  # ="France"
    )


def get_valid_date(
    menu_arborescence: list[str],
    regular_inputs_method: Callable,
) -> datetime.date:
    """Create date from user input.

    Args:
        menu_arborescence (list[str]): Menu str list for prefix.
        regular_inputs_method (Callable): regular_inputs method loaded with
            callbacks.

    Returns:
        datetime.date: Return date input.
    """
    try:
        date = my_input(
            "Birth date (format DD/MM/YYYY) : ",
            menu_arborescence,
            regular_inputs_method,
        )
        day, month, year = [int(x.strip()) for x in date.split("/")]
        date = datetime.date(year, month, day)
    except ValueError:
        _print.my_print("Wrong date format.", menu_arborescence)
        date = get_valid_date(menu_arborescence, regular_inputs_method)
    return date


def regular_inputs(
    _input: str,
    _my_input: Callable,
    quit_callback: Callable,
    cancel_callback: Callable,
    main_menu_callback: Callable,
):
    """Regular inputs. To trigger on any input.

    `q` for quit program. (Confirmation needed with `o`)

    `r` for cancel to execute last menu.

    `m` for execute main menu.

    Args:
        _input (str): Input to check.
        _my_input (Callable): view.my_input for quit confirmation.
        quit_callback (Callable): Quit program callback.
        cancel_callback (Callable): Cancel to execute last menu callback.
        main_menu_callback (Callable): Execute main menu callback.
    """
    match _input.lower():
        case "q":  # for quitter
            prompt = (
                "\nVoulez-vous vraiment quitter ?\n"
                "Retour au dernier menu si non. (o/n) : "
            )
            _input = _my_input(prompt).lower()
            while _input not in ("o", "n"):
                _input = _my_input(f"Input non reconnu.\n{prompt}").lower()

            if _input == "o":
                quit_callback()
            cancel_callback()
        case "r":  # for retour
            cancel_callback()
        case "m":  # for menu principal
            click.clear()
            main_menu_callback()
        case _:
            pass
