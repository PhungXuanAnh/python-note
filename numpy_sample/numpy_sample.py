import numpy as np

a = np.array([1, 2, 3]) # Tạo một numpy array với rank = 1

print(type(a))            # Sẽ in ra "<class 'numpy.ndarray'>"
print(a.shape)            # Sẽ in ra "(3,)"
print(a[0], a[1], a[2])   # Sẽ in ra "1 2 3"
a[0] = 5                  # Thay đổi giá trị của 1 phần tử trong mảng
print(a)                  # Sẽ in ra kết quả là "[5, 2, 3]"

b = np.array([[1,2,3],[4,5,6]])    # Tạo một numpy array với rank =2
print(b.shape)                     # In ra "(2, 3)"
print(b[0, 0], b[0, 1], b[1, 0])   # Sẽ in ra "1 2 4"

a = np.zeros((2,2))   # Tạo một numpy array với tất cả phẩn tử là 0
print(a)              # "[[ 0.  0.]
                      #   [ 0.  0.]]"

b = np.ones((1,2))    # Tạo một numpy array với tất cả phẩn tử là 1
print(b)              # "[[ 1.  1.]]"

c = np.full((2,2), 7)  # Tạo một mảng hằng
print(c)               # "[[ 7.  7.]
                       #   [ 7.  7.]]"

d = np.eye(2)         # Tạo một ma trận đơn vị 2 x 2
print(d)              # "[[ 1.  0.]
                      #   [ 0.  1.]]"

e = np.random.random((2,2))  # Tạo một mảng với các giá trị ngẫu nhiên
print(e)                     # Có thể là "[[ 0.91940167  0.08143941]
                             #             [ 0.68744134  0.87236687]]"
f = np.arange(10) # Tạo 1 numpy array với các phẩn tử từ 0 đến 9
print(f)          # "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"