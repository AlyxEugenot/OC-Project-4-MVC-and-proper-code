# import click

# handle text beautifully

import chess.view


def my_input(prompt_text: str):
    return input(f"input {prompt_text}")  # TODO str prefix


# def ask_prompt(text_prompt: str, default_text: str = None):
#     if default_text is None:
#         answer = click.prompt(text_prompt, show_default=False)
#     else:
#         answer = click.prompt(text_prompt, default=default_text,
#               show_default=True)
#     return answer


def create_address(
    address_context: str,
) -> tuple[str, str, str, str, str, str, str] | None:
    chess.view.my_print(address_context)

    suffix = "\n\t\t-> "
    addressee_id = my_input(
        (
            "1. Identification du destinataire : civilité, titre ou qualité "
            "+ prénom + nom.\n\tEx : M. Valéry DUPONT\n\t"
            f"[Generate complete address if empty]{suffix}"
        ),
    )

    if addressee_id == "":
        return None

    delivery_point = my_input(
        (
            "2. Complément d’identification du destinataire ou point de "
            "remise à l’intérieur du bâtiment : N° appartement, boite aux "
            "lettres, étage, couloir.\n\tEx : Appartement 12 Escalier "
            f"C{suffix}"
        )
    )
    additional_geo_info = my_input(
        (
            "3. Facultatif. Complément d’identification du point "
            "géographique – extérieur du bâtiment : entrée, tour, bâtiment, "
            f"immeuble, résidence.\n\tEx : Résidence Les Tilleuls{suffix}"
        )
    )
    house_nb_street_name = my_input(
        (
            "4. Numéro et libellé de la voie.\n\tEx : 1 impasse de "
            f"l'Eglise{suffix}"
        )
    )
    additional_delivery_info = my_input(
        (
            f"5. Facultatif. Lieu dit ou service particulier de distribution –"
            f" Poste restante, boite postale, etc.\n\tEx : AMAREINS{suffix}"
        )
    )
    postcode = my_input(
        (
            "6. Code postal et localité de destination.\n\tEx : 01090 "
            f"FRANCHELEINS{suffix}"
        )
    )
    country_name = my_input((f"7. Pays.\n\tEx : FRANCE{suffix}"))
    return (
        addressee_id,
        delivery_point,
        additional_geo_info,  # =""
        house_nb_street_name,
        additional_delivery_info,  # =""
        postcode,
        country_name,  # ="France"
    )
