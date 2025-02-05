import click

#handle text beautifully

def ask_prompt(text_prompt:str, default_text:str="pwet"):
    answer = click.prompt(text_prompt, default=default_text, show_default=True)
    return answer