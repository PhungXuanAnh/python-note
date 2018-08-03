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

    if len(unsorted_list) <= 1:
        return unsorted_list
    # Find the middle point and devide it
    middle = len(unsorted_list) // 2
    left_list = unsorted_list[:middle]
    right_list = unsorted_list[middle:]

    left_list = merge_sort(left_list)
    right_list = merge_sort(right_list)
    return list(merge(left_list, right_list))

# Merge the sorted halves


def merge(left_half, right_half):

    res = []
    while len(left_half) != 0 and len(right_half) != 0:
        if left_half[0] < right_half[0]:
            res.append(left_half[0])
            left_half.remove(left_half[0])
        else:
            res.append(right_half[0])
            right_half.remove(right_half[0])
    if len(left_half) == 0:
        res = res + right_half
    else:
        res = res + left_half
    return res


unsorted_list = [3, 4, 2, 1, 8, 6, 9, 0, 5, 7]

print(merge_sort(unsorted_list))
