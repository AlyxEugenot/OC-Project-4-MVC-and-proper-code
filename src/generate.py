"""Some tools to generate random elements."""

import models.model as model
import random
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
            last_name=generate_str(max_len=8),
            birth_date=datetime.date(
                random.randrange(1970, 2022),
                random.randrange(1, 12),
                random.randrange(1, 31),
            ),
            elo=random.randint(150, 2000),
        )
        new_players.append(player)

    return new_players


def generate_str(min_len: int = 3, max_len: int = 12) -> str:
    """Generates any string.

    Args:
        min_len (int, optional): String's minimum length. Defaults to 3.
        max_len (int, optional): String's maximum length. Defaults to 12.

    Returns:
        str: String generated.
    """
    return "".join(
        i for i in random.sample(string.ascii_letters, random.randint(min_len, max_len))
    )


def generate_specific_str(model: str) -> str:
    """Generates specific str from model in argument.
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
            chars.append(str(c))
        elif char.isupper():
            chars.append(c.upper())
        else:
            chars.append(c)

    return "".join(chars)
