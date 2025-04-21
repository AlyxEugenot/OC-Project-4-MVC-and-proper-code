"""Address object."""


class Address:
    """Address class to French address standard: AFNOR NF 10-011.

    All fields should be 38 characters max str.
    """

    def __init__(
        self,
        addressee_id: str,
        delivery_point: str,
        house_nb_street_name: str,
        postcode: str,
        additional_geo_info: str = "",
        additional_delivery_info: str = "",
        country_name: str = "France",
    ):
        """French address standard. All fields should be 38 characters max.

        Args:
            addressee_id (str): 1. Addressee ID: civility, title or quality +\
                firstname + surname. ex: M. Valéry DUPONT
            delivery_point (str): 2. Identification complement: appt nb,\
                letter box, stair, corridor. ex: Appartment 12 Stairs C
            house_nb_street_name (str): 4. Number and street name.\
                ex: 1 avenue des champs élysées
            postcode (str): 6. Postal code and destination locality.\
                ex: 75001 PARIS
            additional_geo_info (str, optional): 3. outside ID complement:\
                entry, tower, building, residence. ex: Résidence Les Tilleuls.\
                    Defaults to "".
            additional_delivery_info (str, optional):
                5. Hamlet (lieu-dit) or particular distribution service:\
                post box, poste restante. ex: La Chaise Dieu. Defaults to "".
            country_name (str, optional): 7. Country name.\
                Defaults to "FRANCE".
        """
        self.addressee_id = addressee_id
        self.delivery_point = delivery_point
        self.additional_geo_info = additional_geo_info
        self.house_nb_street_name = house_nb_street_name
        self.additional_delivery_info = additional_delivery_info
        self.postcode = postcode
        self.country_name = country_name.upper()

    def to_json(self) -> dict:
        """Return json implementation from Address object.

        Args:
            address (Address): Adress object to save

        Returns:
            dict: json dict to use for saving
        """
        this_json = {
            "addressee_id": self.addressee_id,
            "delivery_point": self.delivery_point,
            "additional_geo_info": self.additional_geo_info,
            "house_nb_street_name": self.house_nb_street_name,
            "additional_delivery_info": self.additional_delivery_info,
            "postcode": self.postcode,
            "country_name": self.country_name,
        }
        return this_json

    # pylint: disable=no-self-argument
    def from_json(address: dict) -> "Address":
        # pylint: disable=unsubscriptable-object
        """Return Address object from json.

        Args:
            address (dict): Address dict

        Returns:
            Address: Address object
        """
        returned_address = Address(
            addressee_id=address["addressee_id"],
            delivery_point=address["delivery_point"],
            additional_geo_info=address["additional_geo_info"],
            house_nb_street_name=address["house_nb_street_name"],
            additional_delivery_info=address["additional_delivery_info"],
            postcode=address["postcode"],
            country_name=address["country_name"],
        )
        return returned_address

    def __str__(self):
        """str method. Address formatted.

        Returns:
            str: Address formatted.
        """
        complete_address = [
            self.addressee_id,
            self.delivery_point,
            self.additional_geo_info,
            self.house_nb_street_name,
            self.additional_delivery_info,
            self.postcode,
            self.country_name,
        ]
        filled_address = []
        for element in complete_address:
            if element == "" or element is None:
                continue
            filled_address.append(element)
        return "\n".join(filled_address)

    def __repr__(self):
        return f"{self.addressee_id}, {self.postcode}"
