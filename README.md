# header 1
## header 2
### header 3
#### header 4
##### header 5
###### header 6
****
- Đoạn văn số 1
- Đoạn văn số 2
- Đoạn văn số 3
****
+ Đoạn văn sô 4
+ Đoạn văn số 5
+ Đoạn văn số 6
********
* Đọan văn số 7
* Đoạn văn số 8
  * Đoạn nhỏ số 1
  * Đoạn nhỏ số 2
  * Đoạn nhỏ số 3
****
1. Phần 1
2. Phần 2
3. Phần 3
****
1. Item 1
1. Item 2
1. Item 3
   1. Item 3a
   1. Item 3b
***
**Chữ in đậm** và *chữ in nghiêng*

***Chữ in nghiêng và in đậm***

~~chữ bị gach ngang~~
****
> dẫn chứng 1

> dẫn chứng 2

> dẫn chứng 3
****
code inline:
`import os`

code block:
```python
import os
print("xin chào markdown")
```
****
# bảng
Vẽ bảng trong Markdown sẽ hơi khó nếu bạn chưa quen. Các cột được tách nhau bằng dấu ngăn thẳng đứng | và header được tách với content bằng dấu gạch ngang -.

| Tables        | Are(căn lề giữa)| Cool(căn lề trái)  |
| ------------- |:---------------:| ------------------:|
| col 3 is      | right-aligned   | $1600              |
| col 2 is      | centered        |   $12              |
| zebra stripes | are neat        |    $1              |

****
# link tài liệu tham khảo:
Markdown được thiết kế để dễ nhìn ngay ở định dạng tự nhiên.
Vì vậy bạn có thể đánh dấu mỗi link thành từng số và viết tất cả link thực tương ứng với các số ở cuối cùng (Chú ý: bắt buộc phải đặt dưới cùng).

Let's check out [Wikipedia][1] and [Google][2].

****
# chú thích
Chú thích hay footnote sẽ dùng ký tự ^ bên trong ngoặc vuông [] để đánh dấu và viết lại giải thích ở cuối, cách viết tương tự như link tài liệu tham khảo bên trên.

John Gruber[^1].
[^1]: writer, blog publisher, UI designer, the inventor of the Markdown publishing format.

****
# Escape
Sẽ có những lúc bạn cần dùng đến đúng những ký tự mà Markdown đang sử dụng, ví dụ đơn giản như khi muốn viết *bold* mà không bị in đậm. Khi đó hãy sử dụng ký tự escape \

\*bold\*

****
# Emoji :smile:
Emoji là các biểu tượng thể hiện cảm xúc bắt nguồn từ bộ gõ của Mac/Iphone/Ipad. Kipalog cho phép bạn viết đủ bộ emoji theo cheatsheet của Github :smile:

:smile:

****
# chèn link hình ảnh

![Mô tả hình ảnh](https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png)

****
# chèn link liên kết
[Mô tả liên kết: google](https://www.google.com/)

***
# tạo đường kẻ ngang
***
---
___
# tạo điểm nhấn (highlight)
cách 1: ==highlight==

cách 2: <mark>Marked text</mark>

---
**Markdown** quá *tuyệt* phải không nào. Cảm ơn [John_Gruber](https://en.wikipedia.org/wiki/John_Gruber).

[1]: https://en.wikipedia.org "Wikipedia"
[2]: https://www.google.com "Google"