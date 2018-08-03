"""
Merge sort sử dụng chiến lược chia để trị
Merge sort là thuật toán sắp xếp đệ quy, liên tục chia đôi danh sách.
    - nếu danh sách rỗng hoặc có 1 phần tử, nó đã được sắp xếp
    - nếu danh sách có nhiều hơn 1 phần tử, chúng ta chia đôi danh sách và gọi đệ quy
        merge sort trên 2 nửa
    - Khi 2 nửa đã được sắp xếp thì thực hiện merge 2 nửa đó thành 1 danh sách đã
        được sắp xếp, tiến trình merge lấy 2 danh sách con đã được sắp xếp và kết hợp
        đồng thời sắp xếp chúng thành 1 danh sách đơn 

"""


def merge_sort(unsorted_list):
    """
    Bước 1: Nếu chỉ có 1 phần tử trong list thì list coi như đã được sắp xếp
            Trả về list hoặc giá trị nào đó
    """
    if len(unsorted_list) == 1:
        return unsorted_list

    """
    Bước 2: Chia list một cách đệ qui thành 2 nữa cho đến khi không chia được nữa
    """
    middle = len(unsorted_list) // 2
    list1 = unsorted_list[:middle]
    list2 = unsorted_list[middle:]

    list1 = merge_sort(list1)
    list2 = merge_sort(list2)

    """
    Bước 3: Kết hợp các list nhỏ (đã được sắp xếp) thành list mới (cũng đã được sắp xếp)
            và trả về list này
    """
    return merge(list1, list2)


def merge(list1, list2):
    """
    Lưu y: list1 và list2 là những list đã được sắp xếp
    """
    result = []

    while len(list1) != 0 and len(list2) != 0:
        if list1[0] < list2[0]:
            result.append(list1[0])
            list1.remove(list1[0])
        else:
            result.append(list2[0])
            list2.remove(list2[0])

    if len(list1) != 0:
        result = result + list1

    if len(list2) != 0:
        result = result + list2

    return result


unsorted_list = [3, 4, 2, 1, 8, 6, 9, 0, 5, 7]

print(merge_sort(unsorted_list))
