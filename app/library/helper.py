import os.path
import markdown
from fastapi.templating import Jinja2Templates
import os

def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data


class CustomJinja2Templates(Jinja2Templates):
    """
    To make the username appear in the topnav.html for all pages without 
    having to retrieve it in each specific view function, you can use a global template context processor.
    In FastAPI with Jinja2, you don't have a built-in global context processor like in Django,
    but you can mimic this functionality by modifying the Jinja2Templates class to automatically inject
    the username into every template.

    Args:
        Jinja2Templates (_type_): _description_
    """
    def TemplateResponse(self, name: str, context: dict = None, **kwargs):
        if context is None:
            context = {}
        # Ensure the user is added to the context for every template
        context['user'] = os.getlogin()  # or any other method to fetch the user
        return super().TemplateResponse(name, context, **kwargs)