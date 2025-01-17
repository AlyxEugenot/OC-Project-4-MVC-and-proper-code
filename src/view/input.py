import click

def ask_prompt(text_prompt:str):
    answer = click.prompt(text_prompt)
    return answer