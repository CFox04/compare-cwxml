from cwxml.fragment import Fragment, ChildrenItem, LODProperty
from comparison import compare_object_attrs, ComparisonResult
from main import compare_and_write


def get_group_name(child: ChildrenItem, lod: LODProperty):
    return lod.groups[child.group_index].name


def compare_frag_children(xml_a: Fragment, xml_b: Fragment):
    lod_a = xml_a.physics.lod1
    lod_b = xml_b.physics.lod1

    differences = []
    similarities = []

    children_a = [(get_group_name(child, lod_a), child)
                  for child in lod_a.children]
    children_a.sort(key=lambda e: e[0])
    children_b = [(get_group_name(child, lod_b), child)
                  for child in lod_b.children]
    children_b.sort(key=lambda e: e[0])

    for (name_a, child_a), (name_b, child_b) in zip(children_a, children_b):
        diff_comparison_attrs, sim_comparison_attrs = compare_object_attrs(
            child_a, child_b, exclude_attrs="group_index")

        if not diff_comparison_attrs.is_blank():
            diff_comparison_attrs.title_a = name_a
            diff_comparison_attrs.title_b = name_b

            differences.append(diff_comparison_attrs)
        if not sim_comparison_attrs.is_blank():
            sim_comparison_attrs.title_a = name_a
            sim_comparison_attrs.title_b = name_b

            similarities.append(sim_comparison_attrs)

    return ComparisonResult(differences, similarities)


if __name__ == '__main__':
    compare_and_write(compare_frag_children)
