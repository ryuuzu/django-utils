from django.template import Library, Node, TemplateSyntaxError, Variable

register = Library()


class RangeNode(Node):
    def __init__(self, num, context_name):
        self.num, self.context_name = Variable(num), context_name

    def render(self, context):
        actual_num = self.num.resolve(context)
        context[self.context_name] = range(int(actual_num))
        return ""


@register.tag
def num_range(parser, token):
    """
    Takes a number and iterates and returns a range (list) that can be
    iterated through in templates

    Syntax:
    {% num_range 5 as some_range %}

    {% for i in some_range %}
      {{ i }}: Something I want to repeat\n
    {% endfor %}

    Produces:
    0: Something I want to repeat
    1: Something I want to repeat
    2: Something I want to repeat
    3: Something I want to repeat
    4: Something I want to repeat
    """
    try:
        fnctn, num, trash, context_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            "%s takes the syntax %s number_to_iterate as context_variable"
            % (fnctn, fnctn)
        )
    if not trash == "as":
        raise TemplateSyntaxError(
            "%s takes the syntax %s number_to_iterate as context_variable"
            % (fnctn, fnctn)
        )
    return RangeNode(num, context_name)


@register.simple_tag
def material_tailwind_cdn():
    return (
        f"<!-- stylesheet -->"
        f"<link"
        f'rel="stylesheet"'
        f'href="https://unpkg.com/@material-tailwind/html@latest/styles/material-tailwind.css"'
        f"/>"
        f"<!-- script -->"
        f'<script src="https://unpkg.com/@material-tailwind/html@latest/scripts/script-name.js"></script>'
    )
