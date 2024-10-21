# -*- coding: utf-8 -*-
# mypy: ignore-errors
# cSpell:disable


"""
Tham khảo: https://www.meinvoice.vn/tin-tuc/18211/cach-tinh-thue-thu-nhap-ca-nhan/#3_Cach_tu_tinh_thue_thu_nhap_ca_nhan
Code Python dùng để tính thuế thu nhập cá nhân, nhập vào lương chưa khấu trừ + số người phụ thuộc
"""
import re
from babel.numbers import format_decimal
from functools import partial

fm = partial(format_decimal, locale="vi_VN")


def bảo_hiểm_xã_hội(lương_gross: int):
    lương_đóng_bhxh_cao_nhất = 46800000
    if lương_gross > lương_đóng_bhxh_cao_nhất:
        return lương_đóng_bhxh_cao_nhất * 8 / 100
    return lương_gross * 8 / 100


def bảo_hiểm_y_tế(lương_gross: int):
    lương_đóng_bhyt_cao_nhất = 46800000
    if lương_gross > lương_đóng_bhyt_cao_nhất:
        return lương_đóng_bhyt_cao_nhất * 1.5 / 100
    return lương_gross * 1.5 / 100


def bảo_hiểm_thất_nghiệp(lương_gross: int):
    # https://thuvienphapluat.vn/cong-dong-dan-luat/chi-tiet-muc-dong-va-huong-bao-hiem-that-nghiep-cao-nhat-theo-tien-luong-moi-215326.aspx
    # https://thuvienphapluat.vn/hoi-dap-phap-luat/83A281A-hd-muc-dong-bao-hiem-that-nghiep-moi-nhat-nam-2024-la-bao-nhieu.html#:~:text=M%E1%BB%A9c%20l%C6%B0%C6%A1ng%20c%C6%A1%20s%E1%BB%9F%20t%E1%BB%AB,t%E1%BB%91i%20%C4%91a%20l%C3%A0%20468.000%20%C4%91%E1%BB%93ng.
    lương_đóng_bhtn_cao_nhất = 99200000
    if lương_gross > lương_đóng_bhtn_cao_nhất:
        return lương_đóng_bhtn_cao_nhất * 1 / 100
    return lương_gross * 1 / 100


def tinh_thue_theo_thang(thu_nhập_tính_thuế: int):
    if 0 <= thu_nhập_tính_thuế <= 5000000:  # Bậc thuế 5%
        thuế_bậc_5 = (5000000 - thu_nhập_tính_thuế) * 5 / 100
        thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = 0, 0, 0, 0, 0, 0

    if 5000000 < thu_nhập_tính_thuế <= 10000000:  # Bậc thuế 10%
        thuế_bậc_5 = (5000000 - 0) * 5 / 100
        thuế_bậc_10 = (thu_nhập_tính_thuế - 5000000) * 10 / 100
        thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = 0, 0, 0, 0, 0

    if thu_nhập_tính_thuế in range(10000000, 18000000 + 1):  # Bậc thuế 15%
        thuế_bậc_5 = (5000000 - 0) * 5 / 100
        thuế_bậc_10 = (10000000 - 5000000) * 10 / 100
        thuế_bậc_15 = (thu_nhập_tính_thuế - 10000000) * 15 / 100
        thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = 0, 0, 0, 0

    if thu_nhập_tính_thuế in range(18000000, 32000000 + 1):  # Bậc thuế 20%
        thuế_bậc_5 = (5000000 - 0) * 5 / 100
        thuế_bậc_10 = (10000000 - 5000000) * 10 / 100
        thuế_bậc_15 = (18000000 - 10000000) * 15 / 100
        thuế_bậc_20 = (thu_nhập_tính_thuế - 18000000) * 20 / 100
        thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = 0, 0, 0

    if thu_nhập_tính_thuế in range(32000000, 52000000):  # Bậc thuế 25%
        thuế_bậc_5 = (5000000 - 0) * 5 / 100
        thuế_bậc_10 = (10000000 - 5000000) * 10 / 100
        thuế_bậc_15 = (18000000 - 10000000) * 15 / 100
        thuế_bậc_20 = (32000000 - 18000000) * 20 / 100
        thuế_bậc_25 = (thu_nhập_tính_thuế - 32000000) * 25 / 100
        thuế_bậc_30, thuế_bậc_35 = 0, 0

    if thu_nhập_tính_thuế in range(52000000, 80000000 + 1):  # Bậc thuế 30%
        thuế_bậc_5 = (5000000 - 0) * 5 / 100
        thuế_bậc_10 = (10000000 - 5000000) * 10 / 100
        thuế_bậc_15 = (18000000 - 10000000) * 15 / 100
        thuế_bậc_20 = (32000000 - 18000000) * 20 / 100
        thuế_bậc_25 = (52000000 - 32000000) * 25 / 100
        thuế_bậc_30 = (thu_nhập_tính_thuế - 52000000) * 30 / 100
        thuế_bậc_35 = 0

    if thu_nhập_tính_thuế > 80000000:  # Bậc thuế 35%
        thuế_bậc_5 = (5000000 - 0) * 5 / 100
        thuế_bậc_10 = (10000000 - 5000000) * 10 / 100
        thuế_bậc_15 = (18000000 - 10000000) * 15 / 100
        thuế_bậc_20 = (32000000 - 18000000) * 20 / 100
        thuế_bậc_25 = (52000000 - 32000000) * 25 / 100
        thuế_bậc_30 = (80000000 - 52000000) * 30 / 100
        thuế_bậc_35 = (thu_nhập_tính_thuế - 80000000) * 35 / 100

    return (round(thuế_bậc_5), round(thuế_bậc_10), round(thuế_bậc_15), round(thuế_bậc_20), round(thuế_bậc_25), round(thuế_bậc_30), round(thuế_bậc_35))


def thue_tncn_theo_thang(lương_gross: int, số_người_phụ_thuộc: int):
    """
    Hàm tính thuế thu nhập cá nhân bằng Python
    """
    thuế = 0
    lương_gross = eval("".join(lương_gross.split(".")))
    #    số_người_phụ_thuộc = eval(số_người_phụ_thuộc)
    bhxh = round(bảo_hiểm_xã_hội(lương_gross))
    bhyt = round(bảo_hiểm_y_tế(lương_gross))
    bhtn = round(bảo_hiểm_thất_nghiệp(lương_gross))
    bh_tổng = bhxh + bhyt + bhtn

    GIAM_TRU_BAN_THAN = 11000000
    GIAM_TRU_NGUOI_PHU_THUOC = 4400000
    giảm_trừ_gia_cảnh = GIAM_TRU_BAN_THAN + GIAM_TRU_NGUOI_PHU_THUOC * số_người_phụ_thuộc

    thu_nhập_tính_thuế = lương_gross - bh_tổng - giảm_trừ_gia_cảnh
    thu_nhập_tính_thuế = thu_nhập_tính_thuế if thu_nhập_tính_thuế > 0 else 0

    if thu_nhập_tính_thuế == 0:
        thuế_bậc_5, thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = 0, 0, 0, 0, 0, 0, 0
        thuế = 0
    else:
        thuế_bậc_5, thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = tinh_thue_theo_thang(thu_nhập_tính_thuế)
        thuế = thuế_bậc_5 + thuế_bậc_10 + thuế_bậc_15 + thuế_bậc_20 + thuế_bậc_25 + thuế_bậc_30 + thuế_bậc_35

    lương_net = lương_gross - bh_tổng - thuế

    width = [25, 11]

    print(
        f"{'Lương Gross:':<{width[0]}}{fm(lương_gross):>{width[1]}}",
        "---------------------------------------------",
        f"{'Bảo hiểm xã hội:':<{width[0]}}{fm(bhxh):>{width[1]}}",
        f"{'Bảo hiểm y tế:':<{width[0]}}{fm(bhyt):>{width[1]}}",
        f"{'Bảo hiểm thất nghiệp:':<{width[0]}}{fm(bhtn):>{width[1]}}",
        f"{'Bảo hiểm tổng:':<{width[0]}}{fm(bh_tổng):>{width[1]}}",
        "---------------------------------------------",
        f"{'Thu nhập tính thuế:':<{width[0]}}{fm(thu_nhập_tính_thuế):>{width[1]}}",
        f"{'Thuế bậc  5%:':<{width[0]}}{fm(thuế_bậc_5):>{width[1]}}",
        f"{'Thuế bậc 10%:':<{width[0]}}{fm(thuế_bậc_10):>{width[1]}}",
        f"{'Thuế bậc 15%:':<{width[0]}}{fm(thuế_bậc_15):>{width[1]}}",
        f"{'Thuế bậc 20%:':<{width[0]}}{fm(thuế_bậc_20):>{width[1]}}",
        f"{'Thuế bậc 25%:':<{width[0]}}{fm(thuế_bậc_25):>{width[1]}}",
        f"{'Thuế bậc 30%:':<{width[0]}}{fm(thuế_bậc_30):>{width[1]}}",
        f"{'Thuế bậc 35%:':<{width[0]}}{fm(thuế_bậc_35):>{width[1]}}",
        f"{'Thuế tổng:':<{width[0]}}{fm(thuế):>{width[1]}}",
        "---------------------------------------------",
        f"{'Lương net:':<{width[0]}}{fm(lương_net):>{width[1]}}",
        sep="\n",
    )


def input_lương():
    """
    Hàm nhập lương, chỉ nhận giá trị số
    """
    lương = input("Nhập lương Gross:")
    if not re.search(r"((\d{1,3})(?:,[0-9]{3}){1,3}|(\d{1,11}))", lương):
        print("Chỉ nhận input số, không phải ký tự")
        lương = input_lương()
    return lương


def input_số_người_phụ_thuộc():
    """
    Hàm nhập số người phụ thuộc, chỉ nhận giá trị số
    """
    số_người_phụ_thuộc = input("Nhập số người phụ thuộc :")
    if not re.search("^[0-9]+$", số_người_phụ_thuộc):
        print("Chỉ nhận input số, không phải ký tự")
        số_người_phụ_thuộc = input_số_người_phụ_thuộc()
    return số_người_phụ_thuộc


if __name__ == "__main__":
    print("Bạn có thể nhập số tiền bằng phân cách bằng dấu ',' , ví dụ : 10,000,000")
    print("~ ---------- ~")
    #    lương = input_lương()
    #    số_người_phụ_thuộc = input_số_người_phụ_thuộc()

    lương = "79.662.000"
    # lương = "170.000.000"
    số_người_phụ_thuộc = 4
    thue_tncn_theo_thang(lương, số_người_phụ_thuộc)
