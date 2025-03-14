"""Some tools to generate random elements."""

import chess.model as model
import chess.model.storage as storage
import random
import numpy.random as nprand
import string
import datetime
import typing

VOWEL, CONSONNANT = ("aeiouy"), ("bcdfghjklmnpqrstvwxz")


def test_input(  # FIXME should be elsewhere
    generation: typing.Callable, occurences: int = 20, in_between_character: str = ""
):
    """Prints in console *occurences* number of *generation* generated str.

    Args:
        generation (typing.Callable): Function used to generate str. (can be lambda)
        occurences (int, optional): Number of inputs in console. Defaults to 20.
        in_between_character (str, optional): Character between inputs.\
            (can be \\n). Defaults to "".
    """
    for i in range(occurences):
        print(f"{in_between_character}{generation()}")


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


def generate_address(person_name: str = None) -> model.Address:
    """Generates random address.

    Args:
        person_name (str, optional): Name of the person the address is for.\
            Automatically generated if None. Defaults to None.

    Returns:
        model.Address: Random address.
    """
    if person_name is None:
        person_name = str(generate_players(1)[0])
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

def generate_available_id(json_key:str):
    id=None
    while id is None or storage.id_already_exists(id,json_key):
        match json_key:
            case storage.PLAYERS:   
                id = generate_specific_str("aannnnn")
            case storage.TOURNAMENTS :
                id = random.randint(100000,999999)                    
            case storage.ROUNDS:
                id = random.randint(100000,999999)
            case storage.MATCHES:
                id = random.randint(1000000000,9999999999)
            case _:
                raise ValueError("La clé n'existe pas dans le fichier de save. / Elle est mal écrite.")    
    return id

def is_empty_string(string_to_test: str) -> bool:  # FIXME should be elsewhere
    if string_to_test == "" or string_to_test is None:
        return True
    else:
        return False
