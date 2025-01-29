import click

#handle text beautifully

def ask_prompt(text_prompt:str, default_text:str=""):
    answer = click.prompt(text_prompt, default="pwet", show_default=True)
    return answer