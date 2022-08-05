from cwxml.fragment import Fragment, GroupItem, LODProperty
from comparison import compare_object_attrs, ComparisonResult, Comparison
from main import compare_and_write


def get_group_parent_name(parent_index: int, lod: LODProperty) -> str:
    if parent_index == 255:
        return lod.tag_name

    parent = lod.groups[parent_index]

    if isinstance(parent, GroupItem):
        return parent.name

    return "Unknown parent"


def compare_group_parents(parent_a_name: str, parent_b_name: str):
    diff_comparison = Comparison()
    sim_comparison = Comparison()

    comparison_string_a = f"Has parent '{parent_a_name}'"
    comparison_string_b = f"Has parent '{parent_b_name}'"

    if parent_a_name != parent_b_name:
        diff_comparison.desc_a = comparison_string_a
        diff_comparison.desc_b = comparison_string_b
    else:
        sim_comparison.desc_a = comparison_string_a
        sim_comparison.desc_b = comparison_string_b

    return diff_comparison, sim_comparison


def compare_frag_groups(xml_a: Fragment, xml_b: Fragment):
    differences = []
    similarities = []

    lod_a = xml_a.physics.lod1
    lod_b = xml_b.physics.lod1

    groups_a: list[GroupItem] = [group for group in lod_a.groups]
    groups_a.sort(key=lambda e: e.name)
    groups_b: list[GroupItem] = [group for group in lod_b.groups]
    groups_b.sort(key=lambda e: e.name)

    for group_a, group_b in zip(groups_a, groups_b):
        parent_a_name = get_group_parent_name(group_a.parent_index, lod_a)
        parent_b_name = get_group_parent_name(group_b.parent_index, lod_b)

        diff_comparison, sim_comparison = compare_group_parents(
            parent_a_name, parent_b_name)
        diff_comparison_attrs, sim_comparison_attrs = compare_object_attrs(
            group_a, group_b, exclude_attrs="parent_index")

        diff_comparison.combine_descriptions(diff_comparison_attrs)
        sim_comparison.combine_descriptions(sim_comparison_attrs)

        diff_comparison.title_a = group_a.name
        diff_comparison.title_b = group_b.name
        sim_comparison.title_a = group_a.name
        sim_comparison.title_b = group_b.name

        if not diff_comparison.is_blank():
            differences.append(diff_comparison)
        if not sim_comparison.is_blank():
            similarities.append(sim_comparison)

    return ComparisonResult(differences, similarities)


if __name__ == '__main__':
    compare_and_write(compare_frag_groups)
