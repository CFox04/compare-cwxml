from dataclasses import dataclass, field
from string_template import md_template
from config import Config


def compare_object_attrs(object_a, object_b, exclude_attrs: list[str] = None):
    """Compare the attributes of object_a and object_b and return a difference
    comparison and similarity comparison."""
    difference_comparison = Comparison()
    similarity_comparison = Comparison()

    for key in object_a.__dict__.keys():
        if key in exclude_attrs:
            continue

        value_a = getattr(object_a, key)
        value_b = getattr(object_b, key)

        if Config.float_precision is not None and isinstance(value_a, float) and isinstance(value_b, float):
            value_a = round(value_a, Config.float_precision)
            value_b = round(value_b, Config.float_precision)

        comparison_string_a = f"{key}: {value_a}"
        comparison_string_b = f"{key}: {value_b}"

        if value_a != value_b:
            difference_comparison.append_desc_a(comparison_string_a)
            difference_comparison.append_desc_b(comparison_string_b)
        else:
            similarity_comparison.append_desc_a(comparison_string_a)
            similarity_comparison.append_desc_b(comparison_string_b)

    return difference_comparison, similarity_comparison


def add_str_spaces(string: str):
    SPACES = " " * 4
    new_string = []
    for line in string.split("\n"):
        new_string.append(SPACES + line)
    return "\n".join(new_string)


def append_string(str_a: str, str_b: str):
    return f"{str_a}\n{str_b}"


@dataclass
class Comparison:
    """Stores data that describes a comparison."""
    desc_a: str = ""
    desc_b: str = ""
    title_a: str = ""
    title_b: str = ""

    def text(self) -> str:
        """Get string representation of this comparison."""
        self.add_desc_spaces()
        return md_template(self.title_a, self.desc_a, self.title_b, self.desc_b)

    def combine_descriptions(self, other):
        self.desc_a = append_string(self.desc_a, other.desc_a)
        self.desc_b = append_string(self.desc_b, other.desc_b)

    def append_desc_a(self, desc: str):
        self.desc_a = append_string(self.desc_a, desc)

    def append_desc_b(self, desc: str):
        self.desc_b = append_string(self.desc_b, desc)

    def add_desc_spaces(self):
        self.desc_a = add_str_spaces(self.desc_a)
        self.desc_b = add_str_spaces(self.desc_b)

    def is_blank(self):
        return self.desc_a.strip() == "" and self.desc_b.strip() == ""


@dataclass
class ComparisonResult:
    """Differences and similarities of two XML files."""
    differences: list[Comparison] = field(default_factory=list)
    similarities: list[Comparison] = field(default_factory=list)
