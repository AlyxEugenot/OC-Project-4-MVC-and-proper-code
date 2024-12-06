"""Some tools to generate random elements."""

import models.model as model
import random
import numpy.random as nprand
import string
import datetime

VOWEL, CONSONNANT = ("aeiouy"), ("bcdfghjklmnpqrstvwxz")


def generate_players(amount: int = 4) -> list[model.Player]:
    """Generates *amount* number of random players.

    Args:
        amount (int, optional): Number of players to generate. Defaults to 4.

    Returns:
        list[model.Player]: List of players generated.
    """
    new_players = []
    for player in range(amount):
        player = model.Player(
            id=generate_specific_str("AANNNNN"),
            first_name=generate_specific_str("Cvacv"),
            last_name=generate_str().title(),
            birth_date=datetime.date(
                random.randint(1970, 2022),
                random.randint(1, 12),
                random.randint(1, 28),
            ),
            elo=random.randint(150, 2000),
        )
        new_players.append(player)

    return new_players


def generate_address(person_name: str) -> model.Address:
    """Generates random address.

    Returns:
        model.Address: Random address.
    """
    addressee_id = f"{random.choice(["Mr","Mme","Mx"])}. {person_name}"
    delivery_point = f"{nprand.choice(
        a=["", 
            f"Appartement {random.randint(1,50)}", 
            f"Escalier {random.choice("ABCDE")}",
            f"Chambre {random.randint(1,50)}"
            ],
        p=[.3,.3,.3,.1]
        )}"
    house_nb_street_name = f"{random.randint(1,250)} {nprand.choice(
            a=["Rue", "Avenue","Place","Parvis"],
            p=[.45,.35,.15,.05]
        )} {nprand.choice(["","Bis","Ter"],p=[.7,.2,.1])} {" ".join(
            [generate_str(2,6) for i in range(random.randint(1,4))]
            ).title()}"
    postcode = f"{generate_specific_str("nnnnn")} {generate_str().upper()}"

    result = model.Address(addressee_id, delivery_point, house_nb_street_name, postcode)
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
        i for i in random.sample(string.ascii_letters, random.randint(min_len, max_len))
    )


def generate_specific_str(model: str) -> str:
    """Generates specific str from model in argument. Same length and 
    c=consonnant, v=vowel, n=number, any=letter. 
    Upper and lower stay as is.

    Args:
        model (str): Model to generate string from random letters.\
        c=consonnant, v=vowel, n=number, any=letter

    Returns:
        str: String generated.
    """
    chars = []
    for char in model:
        if char.lower() == "v":
            c = random.choice(VOWEL)
        elif char.lower() == "c":
            c = random.choice(CONSONNANT)
        elif char.lower() == "n":
            c = random.randint(0, 9)
        else:
            c = random.choice(string.ascii_lowercase)

        if type(c) is int:
            c = str(c)
        elif char.isupper():
            c = c.upper()

        chars.append(c)

    return "".join(chars)
