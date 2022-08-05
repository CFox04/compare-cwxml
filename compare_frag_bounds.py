from cwxml.fragment import Fragment, LODProperty, ChildrenItem
from comparison import compare_object_attrs, ComparisonResult
from main import compare_and_write


def get_col_name(child_index: int, lod: LODProperty):
    child: ChildrenItem = lod.children[child_index]

    return lod.groups[child.group_index].name + "_col"


def compare_frag_bounds(xml_a: Fragment, xml_b: Fragment):
    lod_a = xml_a.physics.lod1
    lod_b = xml_b.physics.lod1

    differences = []
    similarities = []

    bounds_a = [(get_col_name(index, lod_a), bound)
                for (index, bound) in enumerate(lod_a.archetype.bounds.children)]
    bounds_a.sort(key=lambda e: e[0])
    bounds_b = [(get_col_name(index, lod_b), bound)
                for (index, bound) in enumerate(lod_b.archetype.bounds.children)]
    bounds_b.sort(key=lambda e: e[0])

    for (name_a, bound_a), (name_b, bound_b) in zip(bounds_a, bounds_b):
        diff_comparison_attrs, sim_comparison_attrs = compare_object_attrs(
            bound_a, bound_b, exclude_attrs=["materials, vertices, vertex_colors, polygons, vertices_2, octants"])

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
    compare_and_write(compare_frag_bounds)
