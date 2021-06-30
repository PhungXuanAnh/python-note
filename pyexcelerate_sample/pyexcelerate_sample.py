"""
    pip install pyexcelerate
"""

from pyexcelerate import Workbook
from datetime import datetime


def write_bulk_data_cell_by_cell():
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # data is a 2D array
    wb = Workbook()
    wb.new_sheet("sheet name", data=data)
    wb.save("write_bulk_data_cell_by_cell.xlsx")


def write_bulk_data_to_a_range():
    wb = Workbook()
    ws = wb.new_sheet("test")
    ws.range("B2", "C3").value = [[1, 2], [3, 4]]
    wb.save("write_bulk_data_to_a_range.xlsx")


def write_cell_data_faster():
    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws.set_cell_value(1, 1, 15) # a number
    ws.set_cell_value(1, 2, 20)
    ws.set_cell_value(1, 3, "=SUM(A1,B1)") # a formula
    ws.set_cell_value(1, 4, str(datetime.now())) # a date
    wb.save("write_cell_data_faster.xlsx")


def write_cell_data_fast():
    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws[1][1].value = 15 # a number
    ws[1][2].value = 20
    ws[1][3].value = "=SUM(A1,B1)" # a formula
    ws[1][4].value = str(datetime.now()) # a date
    wb.save("write_cell_data_fast.xlsx")


def select_cell_by_name():
    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws.cell("A1").value = 12
    wb.save("select_cell_by_name.xlsx")


def merge_cell():
    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    
    ws[1][1].value = 15
    ws.range("A1", "B1").merge()

    ws[1][5].value = 15
    ws.range("E1", "G1").merge()

    ws[3][1].value = 15
    ws.range("A3", "A4").merge()

    ws[3][5].value = 15
    ws.range("E3", "E5").merge()

    wb.save("merge_cell.xlsx")


def styling_cell_fastest():
    from pyexcelerate import Workbook, Color, Style, Font, Fill, Format
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws.set_cell_value(1, 1, 123456)
    ws.set_cell_style(1, 1, Style(font=Font(bold=True)))
    ws.set_cell_style(1, 1, Style(font=Font(italic=True)))
    ws.set_cell_style(1, 1, Style(font=Font(underline=True)))
    ws.set_cell_style(1, 1, Style(font=Font(strikethrough=True)))
    ws.set_cell_style(1, 1, Style(fill=Fill(background=Color(255,228,75,52))))

    ws.set_cell_value(1, 2, datetime.now())
    ws.set_cell_style(1, 2, Style(format=Format('mm/dd/yy')))

    wb.save("styling_cell_fastest.xlsx")


def styling_cell_faster():
    from pyexcelerate import Workbook, Color
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws.set_cell_value(1, 1, 123456)
    ws.get_cell_style(1, 1).font.bold = True
    ws.get_cell_style(1, 1).font.italic = True
    ws.get_cell_style(1, 1).font.underline = True
    ws.get_cell_style(1, 1).font.strikethrough = True
    ws.get_cell_style(1, 1).fill.background = Color(0, 255, 0, 0)

    ws.set_cell_value(1, 2, datetime.now())
    ws.get_cell_style(1, 2).format.format = 'mm/dd/yy'
    
    wb.save("styling_cell_faster.xlsx")


def styling_cell_fast():
    from pyexcelerate import Workbook, Color
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws[1][1].value = 123456
    ws[1][1].style.font.bold = True
    ws[1][1].style.font.italic = True
    ws[1][1].style.font.underline = True
    ws[1][1].style.font.strikethrough = True
    ws[1][1].style.fill.background = Color(0, 255, 0, 0)

    ws[1][2].value = datetime.now()
    ws[1][2].style.format.format = 'mm/dd/yy'

    wb.save("styling_cell_fast.xlsx")


def styling_ranges():
    from pyexcelerate import Workbook, Color
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("test")
    ws.range("A1","C3").value = 1
    ws.range("A1","C1").style.font.bold = True
    ws.range("A2","C3").style.font.italic = True
    ws.range("A3","C3").style.fill.background = Color(255, 0, 0, 0)
    ws.range("C1","C3").style.font.strikethrough = True

    wb.save("styling_ranges.xlsx")


def styling_rows_fastest():
    from pyexcelerate import Workbook, Color, Style, Fill
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws[1][1].value = 123456
    ws.set_row_style(1, Style(fill=Fill(background=Color(255,0,0,0))))
    wb.save("styling_rows_fastest.xlsx")


def styling_rows_faster():
    from pyexcelerate import Workbook, Color
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws[1][1].value = 123456
    ws.get_row_style(1).fill.background = Color(255, 0, 0)
    wb.save("styling_rows_faster.xlsx")

def styling_rows_fast():
    from pyexcelerate import Workbook, Color
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws[1][1].value = 123456
    ws[1].style.fill.background = Color(255, 0, 0)
    wb.save("styling_rows_fast.xlsx")


def styling_columns_fastest():
    from pyexcelerate import Workbook, Color, Style, Fill
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws[1][1].value = 123456
    ws.set_col_style(1, Style(fill=Fill(background=Color(255,0,0,0))))
    wb.save("styling_columns_fastest.xlsx")


def row_height_width():
    from pyexcelerate import Workbook, Color, Style, Fill
    from datetime import datetime

    wb = Workbook()

    ws = wb.new_sheet("sheet name 1")
    
    ws[1][1].value = "this is long string 1"
    ws[1][2].value = "this is long string 2"
    ws[1][3].value = "this is long string 3"

    ws.set_col_style(1, Style(size=-1))     # auto-fit     column 1
    ws.set_col_style(2, Style(size=0))      # hidden       column 2
    ws.set_col_style(3, Style(size=100))    # width=100    column 3
    
    # -----------------
    ws = wb.new_sheet("sheet name 2")
    
    ws[1][1].value = "this is long string 1"
    ws[2][1].value = "this is long string 2"
    ws[3][1].value = "this is long string 3"

    ws.set_row_style(1, Style(size=-1))     # auto-fit     column 1
    ws.set_row_style(2, Style(size=0))      # hidden       column 2
    ws.set_row_style(3, Style(size=100))    # width=100    column 3

    wb.save("row_height_width.xlsx")


def styling_available():
    from pyexcelerate import Workbook, Color, Style, Fill, Border
    from datetime import datetime

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws[1][1].value = 123456
    ws[1][1].style.font.bold = True
    ws[1][1].style.font.italic = True
    ws[1][1].style.font.underline = True
    ws[1][1].style.font.strikethrough = True
    ws[1][1].style.font.color = Color(255, 0, 255)
    ws[1][1].style.fill.background = Color(0, 255, 0)
    ws[1][1].style.alignment.vertical = 'top'
    ws[1][1].style.alignment.horizontal = 'right'
    ws[1][1].style.alignment.rotation = 90
    ws[1][1].style.alignment.wrap_text = True
    ws[1][1].style.borders.top.color = Color(255, 0, 0)
    ws[1][1].style.borders.right.style = '-.'   # available: .-, ..-, --, .., =, ., medium -., medium -.., medium --, /-., _

    wb.save("styling_available.xlsx")


def styling_defined_by_objects():
    from pyexcelerate import Workbook, Font, Color, Alignment

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws[1][1].value = datetime.now()

    ws[1][1].style.font = Font(bold=True, italic=True, underline=True, strikethrough=True, family="Calibri", size=10, color=Color(255,0,0))
    ws[1][1].style.format.format = 'mm/dd/yy'
    ws[1][1].style.alignment=Alignment(horizontal="left", vertical="bottom", rotation=0, wrap_text=True)    #("left", "center", "right"), 

    wb.save("styling_defined_by_objects.xlsx")



def styling_defined_ALL_style_by_objects():
    from pyexcelerate import Workbook, Style, Font, Color, Fill, Alignment, Borders, Border, Format

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    
    borders = Borders.Borders(
        left=Border.Border(color=Color(255,0,0), style="thin"), 
        right=Border.Border(color=Color(255,0,0), style="mediumDashDotDot"), 
        top=Border.Border(color=Color(255,0,0), style="double"), 
        bottom=Border.Border(color=Color(255,0,0), style="slantDashDot")
    )

    ws.cell("E11").value = datetime.now()
    ws.cell("E11").style = Style(
        font=Font(bold=True, italic=True, underline=True, strikethrough=True, family="Calibri", size=20, color=Color(251,240,11)),
        fill=Fill(background= Color(33,133,255)), 
        alignment=Alignment(horizontal="left", vertical="bottom", rotation=0, wrap_text=True),    #("left", "center", "right"), 
        borders=borders,
        format=Format('mm/dd/yy'),  # NOTE: if cell string show ###, then decrease font size or increase col size
        # size=-1     # NOTE: don't work, it must use below with row or column statements
    )

    ws.set_col_style(5, Style(size=-1))     # set width of column   # E col
    ws.set_row_style(11, Style(size=-1))    # set height of row

    wb.save("styling_defined_ALL_style_by_objects.xlsx")


def styling_cell_some_sample_format():
    from pyexcelerate import Workbook, Style

    wb = Workbook()
    ws = wb.new_sheet("sheet name")
    ws.set_col_style(5, Style(size=30))     # set width of column   # E col
    
    ws.cell("E1").value = datetime.now()
    ws.cell("E1").style.format.format = 'mm/dd/yy hh:MM:ss'  # datetime

    ws.cell("E2").value = 12345678
    ws.cell("E2").style.format.format = '#,##0'             # number    : 12,345,678

    ws.cell("E3").value = 1234.5678
    ws.cell("E3").style.format.format = '#,##0.00'          # float number : 1,234.57

    ws.cell("E4").value = 0.12345
    ws.cell("E4").style.format.format = '0.00%'             # percentage: 12.35%

    wb.save("styling_cell_some_sample_format.xlsx")


if __name__ == "__main__":
    # write_bulk_data_cell_by_cell()
    # write_bulk_data_to_a_range()
    # write_cell_data_faster()
    # write_cell_data_fast()
    
    # select_cell_by_name()
    # merge_cell()

    # styling_cell_fastest()
    # styling_cell_faster()
    # styling_cell_fast()
    styling_cell_some_sample_format()

    # styling_ranges()

    # styling_rows_fastest()
    # styling_rows_faster()
    # styling_rows_fast()

    # styling_columns_fastest()

    # styling_available()
    # row_height_width()

    # styling_defined_by_objects()
    # styling_defined_ALL_style_by_objects()
