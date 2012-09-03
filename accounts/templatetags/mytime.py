from django import template
import datetime
import re

register = template.Library()

@register.tag(name="current_time")
def do_current_time(parser,token):
    try:
        tag_name,arg = token.contents.split(None,1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    format_string, var_name = m.groups()
    if not (format_string[0] == format_string[-1] and format_string[0] in('"',",")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    
    return CurrentTimeNode(format_string[1:-1],var_name)

class CurrentTimeNode(template.Node):
    def __init__(self, format_string,var_name):
        self.format_string = format_string
        self.var_name = var_name
    def render(self, context):
        context[self.var_name]=int(datetime.datetime.now().strftime(self.format_string))
        return ''
