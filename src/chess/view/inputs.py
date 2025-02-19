import click
import chess.model
import chess.generate

# handle text beautifully


def ask_prompt(text_prompt: str, default_text: str = None):
    if default_text is None:
        answer = click.prompt(text_prompt, show_default=False)
    else:
        answer = click.prompt(text_prompt, default=default_text, show_default=True)
    return answer


def create_address(address_context: str) -> chess.model.Address:  # TODO str_prefix
    click.echo(address_context)

    suffix = "\n\t\t-> "
    addressee_id = click.prompt(
        (
            "1. Identification du destinataire : civilité, titre ou qualité "
            "+ prénom + nom.\n\tEx : M. Valéry DUPONT\n\t"
            f"[Generate complete address if empty]{suffix}"
        )
    )

    if addressee_id == "":
        return chess.generate.generate_address(chess.generate.generate_players(1)[0])

    delivery_point = click.prompt(
        (
            "2. Complément d’identification du destinataire ou point de "
            "remise à l’intérieur du bâtiment : N° appartement, boite aux "
            f"lettres, étage, couloir.\n\tEx : Appartement 12 Escalier C{suffix}"
        )
    )
    additional_geo_info = click.prompt(
        (
            "3. Facultatif. Complément d’identification du point "
            "géographique – extérieur du bâtiment : entrée, tour, bâtiment, "
            f"immeuble, résidence.\n\tEx : Résidence Les Tilleuls{suffix}"
        )
    )
    house_nb_street_name = click.prompt(
        ("4. Numéro et libellé de la voie.\n\tEx : 1 impasse de " f"l'Eglise{suffix}")
    )
    additional_delivery_info = click.prompt(
        (
            f"5. Facultatif. Lieu dit ou service particulier de distribution – "
            f"Poste restante, boite postale, etc.\n\tEx : AMAREINS{suffix}"
        )
    )
    postcode = click.prompt(
        (
            "6. Code postal et localité de destination.\n\tEx : 01090 "
            f"FRANCHELEINS{suffix}"
        )
    )
    country_name = click.prompt((f"7. Pays.\n\tEx : FRANCE{suffix}"))
    return chess.model.Address(
        addressee_id=addressee_id,
        delivery_point=delivery_point,
        additional_geo_info=additional_geo_info,  # =""
        house_nb_street_name=house_nb_street_name,
        additional_delivery_info=additional_delivery_info,  # =""
        postcode=postcode,
        country_name=country_name,  # ="France"
    )
