from config import Config
from string import Template

_MD_TEMPLATE = Template("""
**$file_name_a**:

*$title_a*

$a

**$file_name_b**:

*$title_b*

$b

""")


def md_template(title_a: str, a: str, title_b: str, b: str):
    """String template for a markdown entry."""
    file_name_a, file_name_b = Config.get_file_names()
    return _MD_TEMPLATE.substitute(file_name_a=file_name_a, file_name_b=file_name_b, title_a=title_a, a=a, title_b=title_b, b=b)
