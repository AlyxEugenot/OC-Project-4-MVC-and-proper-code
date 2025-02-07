import click

#handle text beautifully

def ask_prompt(text_prompt:str, default_text:str=None):
    if default_text is None:
        answer = click.prompt(text_prompt, default="1", show_default=False)
    else:
        answer = click.prompt(text_prompt, default=default_text, show_default=True)
    return answer