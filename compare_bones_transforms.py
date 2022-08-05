from cwxml.fragment import Fragment
from cwxml.drawable import BoneItem
from comparison import ComparisonResult, Comparison
from main import compare_and_write


def are_mats_equal(m1, m2, do_abs=True, precision: int | None = 4) -> bool:
    """Check if two matrices are equal"""
    is_equal = True

    for row1, row2 in zip(m1, m2):
        for val1, val2 in zip(row1, row2):
            if do_abs:
                val1 = abs(val1)
                val2 = abs(val2)
            if precision is not None:
                val1 = round(val1, precision)
                val2 = round(val2, precision)
            if val1 != val2:
                is_equal = False
                break

    return is_equal


def compare_bone_transforms(xml_a: Fragment, xml_b: Fragment):
    differences = []
    similarities = []

    for (index_a, transform_a), (index_b, transform_b) in zip(enumerate(xml_a.bones_transforms), enumerate(xml_b.bones_transforms)):
        bone_a: BoneItem = xml_a.drawable.skeleton.bones[index_a]
        bone_b: BoneItem = xml_b.drawable.skeleton.bones[index_b]

        mat_a, mat_b = transform_a.value, transform_b.value

        comparison = Comparison(
            title_a=bone_a.name, desc_a=str(mat_a), title_b=bone_b.name, desc_b=str(mat_b))

        if not are_mats_equal(mat_a, mat_b):
            differences.append(comparison)
        else:
            similarities.append(comparison)

    return ComparisonResult(differences, similarities)


if __name__ == '__main__':
    compare_and_write(compare_bone_transforms)
