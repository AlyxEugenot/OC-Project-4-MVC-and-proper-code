"""Utilitary scripts to controllers""" # TODO adapt this ?

import view
import model
import generate

class _util:
    

    def ask_address(self, intro: str) -> model.Address:
        view.intro(intro)

        addressee_id = view.ask_prompt("Addressee ID:(generate all if 'gen' is typed) ")
        if addressee_id == "gen":
            return generate.generate_address()
        delivery_point = view.ask_prompt("delivery_point: ")
        additional_geo_info = view.ask_prompt("additional_geo_info:(can be empty) ")
        house_nb_street_name = view.ask_prompt("house_nb_street_name: ")
        additional_delivery_info = view.ask_prompt(
            "additional_delivery_info:(can be empty) "
        )
        postcode = view.ask_prompt("postcode: ")
        country_name = view.ask_prompt("country_name:(can be empty) ")

        address = model.Address(
            addressee_id=addressee_id,
            delivery_point=delivery_point,
            house_nb_street_name=house_nb_street_name,
            postcode=postcode,
        )
        if additional_geo_info != "":
            address.additional_geo_info = additional_geo_info
        if additional_delivery_info != "":
            address.additional_delivery_info = additional_delivery_info
        if country_name != "":
            address.country_name = country_name

        return address
