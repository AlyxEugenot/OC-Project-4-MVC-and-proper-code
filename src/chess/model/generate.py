"""Some tools to generate random elements."""

__all__ = [
    "generate_available_id",
    "generate_players",
    "generate_address",
    "generate_specific_str",
    "generate_str",
]
import random
import string
import datetime
import numpy.random as nprand
from chess import model
from chess.model import storage

VOWEL, CONSONNANT = ("aeiouy"), ("bcdfghjklmnpqrstvwxz")


def generate_players(amount: int = 4) -> list["model.Player"]:
    """Generates *amount* number of random players.

    Args:
        amount (int, optional): Number of players to generate. Defaults to 4.

    Returns:
        list[model.Player]: List of players generated.
    """

    new_players = []
    for player in range(amount):
        player = model.Player(
            _id=generate_available_id(storage.PLAYERS),
            first_name=generate_specific_str("Cvacv"),
            last_name=generate_str().title(),
            birth_date=datetime.date(
                random.randint(1970, 2022),
                random.randint(1, 12),
                random.randint(1, 28),
            ),
            elo=random.randint(0, 2000),
        )
        new_players.append(player)

    return new_players


def generate_address(person_name: str = None) -> "model.Address":
    """Generates random address.

    Args:
        person_name (str, optional): Name of the person the address is for.\
            Automatically generated if None. Defaults to None.

    Returns:
        model.Address: Random address.
    """

    if person_name is None:
        person_name = str(generate_players(1)[0])
    addressee_id = f"{random.choice(["Mr", "Mme", "Mx"])}. {person_name}"
    delivery_point = nprand.choice(
        a=[
            "",
            f"Appartement {random.randint(1, 50)}",
            f"Escalier {random.choice("ABCDE")}",
            f"Chambre {random.randint(1, 50)}",
        ],
        p=[0.3, 0.3, 0.3, 0.1],
    )
    # region house_nb_street_name
    _house_nb = random.randint(1, 250)
    _street_title = nprand.choice(
        a=["Rue", "Avenue", "Place", "Parvis"], p=[0.45, 0.35, 0.15, 0.05]
    )
    _street_bis_ter = nprand.choice(["", "Bis", "Ter"], p=[0.7, 0.2, 0.1])
    _street_name = " ".join(
        [generate_str(2, 6) for i in range(random.randint(1, 4))]
    ).title()
    # endregion
    house_nb_street_name = (
        f"{_house_nb} {_street_title}{_street_bis_ter} {_street_name}"
    )

    postcode = f"{generate_specific_str("nnnnn")} {generate_str().upper()}"

    result = model.Address(
        addressee_id, delivery_point, house_nb_street_name, postcode
    )
    return result


def generate_str(min_len: int = 3, max_len: int = 8) -> str:
    """Generates any string.

    Args:
        min_len (int, optional): String's minimum length. Defaults to 3.
        max_len (int, optional): String's maximum length. Defaults to 8.

    Returns:
        str: String generated.
    """
    return "".join(
        i
        for i in random.sample(
            string.ascii_letters, random.randint(min_len, max_len)
        )
    )


def generate_specific_str(str_model: str) -> str:
    """Generates specific str from model in argument. Same length and\
        c=consonnant, v=vowel, n=number, any=letter.\
            Upper and lower stay as is.

    Args:
        str_model (str): Model to generate string from random letters.\
        c=consonnant, v=vowel, n=number, any=letter

    Returns:
        str: String generated.
    """
    chars = []
    for char in str_model:
        if char.lower() == "v":
            c = random.choice(VOWEL)
        elif char.lower() == "c":
            c = random.choice(CONSONNANT)
        elif char.lower() == "n":
            c = random.randint(0, 9)
        else:
            c = random.choice(string.ascii_lowercase)

        if isinstance(c, int):
            c = str(c)
        elif char.isupper():
            c = c.upper()

        chars.append(c)

    return "".join(chars)


def generate_available_id(json_key: str) -> str | int:
    """Generate available random ID of json_key type.

    Args:
        json_key (str): json_key from data.json\
            Can be players, rounds, tournaments or matches.

    Raises:
        ValueError: ValueError raised if json_key is wrong.

    Returns:
        str | int: str or int ID depending on what ID is for.
    """
    _id = None
    while _id is None or storage.id_already_exists(_id, json_key):
        match json_key:
            case storage.PLAYERS:
                _id = generate_specific_str("aannnnn")
            case storage.TOURNAMENTS:
                _id = random.randint(100000, 999999)
            case storage.ROUNDS:
                _id = random.randint(100000, 999999)
            case storage.MATCHES:
                _id = random.randint(1000000000, 9999999999)
            case _:
                raise ValueError(
                    "json_key does not exist in data.json. It is wrong."
                )
    return _id
