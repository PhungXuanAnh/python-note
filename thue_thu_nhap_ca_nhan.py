# -*- coding: utf-8 -*-
# mypy: ignore-errors
# cSpell:disable


"""
Tham khảo: https://www.meinvoice.vn/tin-tuc/18211/cach-tinh-thue-thu-nhap-ca-nhan/#3_Cach_tu_tinh_thue_thu_nhap_ca_nhan
Code Python dùng để tính thuế thu nhập cá nhân, nhập vào lương chưa khấu trừ + số người phụ thuộc
Ket qua tra ve giong voi ket qua tu trang nay: https://www.topcv.vn/tinh-luong-gross-net
"""
import re
from functools import partial

from babel.numbers import format_decimal

fm = partial(format_decimal, locale="vi_VN")


def bh_tnld_benh_nn(luong_gross: int):
    lương_đóng_bhxh_cao_nhất = 46800000
    if luong_gross > lương_đóng_bhxh_cao_nhất:
        luong_dong = lương_đóng_bhxh_cao_nhất
    else:
        luong_dong = luong_gross
    return luong_dong * 0.5 / 100

def bảo_hiểm_xã_hội(luong_gross: int):
    lương_đóng_bhxh_cao_nhất = 46800000
    if luong_gross > lương_đóng_bhxh_cao_nhất:
        luong_dong_bhxh = lương_đóng_bhxh_cao_nhất
    else:
        luong_dong_bhxh = luong_gross
    nguoi_ld_tra = luong_dong_bhxh * 8 / 100
    nguoi_sd_ld_tra = luong_dong_bhxh * 17 / 100
    return nguoi_ld_tra, nguoi_sd_ld_tra


def bảo_hiểm_y_tế(luong_gross: int):
    lương_đóng_bhyt_cao_nhất = 46800000
    if luong_gross > lương_đóng_bhyt_cao_nhất:
        luong_dong_bhyt = lương_đóng_bhyt_cao_nhất
    else:
        luong_dong_bhyt = luong_gross
    nguoi_ld_tra = luong_dong_bhyt * 1.5 / 100
    nguoi_sd_ld_tra = luong_dong_bhyt * 3 / 100
    return nguoi_ld_tra, nguoi_sd_ld_tra


def bảo_hiểm_thất_nghiệp(luong_gross: int):
    # https://thuvienphapluat.vn/cong-dong-dan-luat/chi-tiet-muc-dong-va-huong-bao-hiem-that-nghiep-cao-nhat-theo-tien-luong-moi-215326.aspx
    # https://thuvienphapluat.vn/hoi-dap-phap-luat/83A281A-hd-muc-dong-bao-hiem-that-nghiep-moi-nhat-nam-2024-la-bao-nhieu.html#:~:text=M%E1%BB%A9c%20l%C6%B0%C6%A1ng%20c%C6%A1%20s%E1%BB%9F%20t%E1%BB%AB,t%E1%BB%91i%20%C4%91a%20l%C3%A0%20468.000%20%C4%91%E1%BB%93ng.
    lương_đóng_bhtn_cao_nhất = 99200000
    if luong_gross > lương_đóng_bhtn_cao_nhất:
        luong_dong_bhtn = lương_đóng_bhtn_cao_nhất
    else:
        luong_dong_bhtn = luong_gross
    nguoi_ld_tra = luong_dong_bhtn * 1 / 100
    nguoi_sd_ld_tra = luong_dong_bhtn * 1 / 100
    return nguoi_ld_tra, nguoi_sd_ld_tra


def tinh_thue_theo_thang(thu_nhập_tính_thuế: int):
    if 0 <= thu_nhập_tính_thuế <= 5000000:  # Bậc thuế 5%
        thuế_bậc_5 = (5000000 - thu_nhập_tính_thuế) * 5 / 100
        thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = (
            0,
            0,
            0,
            0,
            0,
            0,
        )

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

    if thu_nhập_tính_thuế in range(32000000, 52000000 + 1):  # Bậc thuế 25%
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

    return (
        round(thuế_bậc_5),
        round(thuế_bậc_10),
        round(thuế_bậc_15),
        round(thuế_bậc_20),
        round(thuế_bậc_25),
        round(thuế_bậc_30),
        round(thuế_bậc_35),
    )


def tinh_thue_theo_nam(_thu_nhập_tính_thuế: int):
    thu_nhập_tính_thuế = _thu_nhập_tính_thuế / 1000000
    if 0 <= thu_nhập_tính_thuế <= 60:  # Bậc thuế 5%
        thuế_bậc_5 = (60 - thu_nhập_tính_thuế) * 5 / 100
        thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = (
            0,
            0,
            0,
            0,
            0,
            0,
        )

    if 60 < thu_nhập_tính_thuế <= 120:  # Bậc thuế 10%
        thuế_bậc_5 = (60 - 0) * 5 / 100
        thuế_bậc_10 = (thu_nhập_tính_thuế - 60) * 10 / 100
        thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = 0, 0, 0, 0, 0

    if 120 < thu_nhập_tính_thuế <= 216:  # Bậc thuế 15%
        thuế_bậc_5 = (60 - 0) * 5 / 100
        thuế_bậc_10 = (120 - 60) * 10 / 100
        thuế_bậc_15 = (thu_nhập_tính_thuế - 120) * 15 / 100
        thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = 0, 0, 0, 0

    if 216 < thu_nhập_tính_thuế <= 384:  # Bậc thuế 20%
        thuế_bậc_5 = (60 - 0) * 5 / 100
        thuế_bậc_10 = (120 - 60) * 10 / 100
        thuế_bậc_15 = (216 - 120) * 15 / 100
        thuế_bậc_20 = (thu_nhập_tính_thuế - 216) * 20 / 100
        thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = 0, 0, 0

    if 384 < thu_nhập_tính_thuế <= 624:  # Bậc thuế 25%
        thuế_bậc_5 = (60 - 0) * 5 / 100
        thuế_bậc_10 = (120 - 60) * 10 / 100
        thuế_bậc_15 = (216 - 120) * 15 / 100
        thuế_bậc_20 = (384 - 216) * 20 / 100
        thuế_bậc_25 = (thu_nhập_tính_thuế - 384) * 25 / 100
        thuế_bậc_30, thuế_bậc_35 = 0, 0

    if 624 < thu_nhập_tính_thuế <= 960:  # Bậc thuế 30%
        thuế_bậc_5 = (60 - 0) * 5 / 100
        thuế_bậc_10 = (120 - 60) * 10 / 100
        thuế_bậc_15 = (216 - 120) * 15 / 100
        thuế_bậc_20 = (384 - 216) * 20 / 100
        thuế_bậc_25 = (624 - 384) * 25 / 100
        thuế_bậc_30 = (thu_nhập_tính_thuế - 624) * 30 / 100
        thuế_bậc_35 = 0

    if thu_nhập_tính_thuế > 960:  # Bậc thuế 35%
        thuế_bậc_5 = (60 - 0) * 5 / 100
        thuế_bậc_10 = (120 - 60) * 10 / 100
        thuế_bậc_15 = (216 - 120) * 15 / 100
        thuế_bậc_20 = (384 - 216) * 20 / 100
        thuế_bậc_25 = (624 - 384) * 25 / 100
        thuế_bậc_30 = (960 - 624) * 30 / 100
        thuế_bậc_35 = (thu_nhập_tính_thuế - 960) * 35 / 100

    return (
        round(thuế_bậc_5 * 1000000),
        round(thuế_bậc_10 * 1000000),
        round(thuế_bậc_15 * 1000000),
        round(thuế_bậc_20 * 1000000),
        round(thuế_bậc_25 * 1000000),
        round(thuế_bậc_30 * 1000000),
        round(thuế_bậc_35 * 1000000),
    )


def bảng_lương_năm(
    tong_tnct: int,
    so_nguoi_phu_thuoc: int = 0,
    tong_so_thang_phu_thuoc: int = 0,
    bao_hiem_duoc_tru: int = 0,
    so_thue_tncn_da_khau_tru: int = 0,
    so_thue_tncn_da_tam_nop: int = 0,
):
    """
    Hàm tính thuế thu nhập cá nhân bằng Python
    """
    tong_tnct = eval("".join(tong_tnct.split(".")))
    if isinstance(bao_hiem_duoc_tru, str):
        bao_hiem_duoc_tru = eval("".join(bao_hiem_duoc_tru.split(".")))
    if isinstance(so_thue_tncn_da_khau_tru, str):
        so_thue_tncn_da_khau_tru = eval("".join(so_thue_tncn_da_khau_tru.split(".")))
    if isinstance(so_thue_tncn_da_tam_nop, str):
        so_thue_tncn_da_tam_nop = eval("".join(so_thue_tncn_da_tam_nop.split(".")))

    GIAM_TRU_BAN_THAN = 11000000
    GIAM_TRU_NGUOI_PHU_THUOC = 4400000
    giảm_trừ_gia_cảnh = (
        GIAM_TRU_BAN_THAN * 12
        + GIAM_TRU_NGUOI_PHU_THUOC * so_nguoi_phu_thuoc * tong_so_thang_phu_thuoc
    )

    thu_nhập_tính_thuế = (
        tong_tnct
        - bao_hiem_duoc_tru
        - giảm_trừ_gia_cảnh
    )
    thu_nhập_tính_thuế = thu_nhập_tính_thuế if thu_nhập_tính_thuế > 0 else 0
    thue_da_nop = so_thue_tncn_da_khau_tru + so_thue_tncn_da_tam_nop

    if thu_nhập_tính_thuế == 0:
        thuế_bậc_5, thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = (
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        thuế = 0
        thue_con_phai_nop = 0
    else:
        thuế_bậc_5, thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = (
            tinh_thue_theo_nam(thu_nhập_tính_thuế)
        )
        thuế = (
            thuế_bậc_5
            + thuế_bậc_10
            + thuế_bậc_15
            + thuế_bậc_20
            + thuế_bậc_25
            + thuế_bậc_30
            + thuế_bậc_35
        )
        thue_con_phai_nop = thuế - thue_da_nop

    width = [30, 12]

    print(
        "---------------------------------------------",
        f"{'Thu nhập tính thuế:':<{width[0]}}{fm(thu_nhập_tính_thuế):>{width[1]}}",
        f"{'Giảm trừ gia cảnh:':<{width[0]}}{fm(giảm_trừ_gia_cảnh):>{width[1]}}",
        f"{'Thuế bậc  5% (0 - 60):':<{width[0]}}{fm(thuế_bậc_5):>{width[1]}}",
        f"{'Thuế bậc 10% (60 - 120):':<{width[0]}}{fm(thuế_bậc_10):>{width[1]}}",
        f"{'Thuế bậc 15% (120 - 216):':<{width[0]}}{fm(thuế_bậc_15):>{width[1]}}",
        f"{'Thuế bậc 20% (216 - 384):':<{width[0]}}{fm(thuế_bậc_20):>{width[1]}}",
        f"{'Thuế bậc 25% (384 - 624):':<{width[0]}}{fm(thuế_bậc_25):>{width[1]}}",
        f"{'Thuế bậc 30% (624 - 960):':<{width[0]}}{fm(thuế_bậc_30):>{width[1]}}",
        f"{'Thuế bậc 35% ( > 960):':<{width[0]}}{fm(thuế_bậc_35):>{width[1]}}",
        "---------------------------------------------",
        f"{'Thuế tổng:':<{width[0]}}{fm(thuế):>{width[1]}}",
        f"{'Thuế đã nộp:':<{width[0]}}{fm(thue_da_nop):>{width[1]}}",
        f"{'Thuế còn phải nộp:':<{width[0]}}{fm(thue_con_phai_nop):>{width[1]}}",
        sep="\n",
    )


def bảng_lương_thang(luong_gross: int, luong_dong_bhxh: int = None, số_người_phụ_thuộc: int = 0):
    """
    Hàm tính thuế thu nhập cá nhân bằng Python
    """
    luong_gross = eval("".join(luong_gross.split(".")))
    if luong_dong_bhxh:
        _luong_dong_bhxh = eval("".join(luong_dong_bhxh.split(".")))
    else:
        _luong_dong_bhxh = luong_gross
    bhxh, bhxh1 = (round(v) for v in bảo_hiểm_xã_hội(_luong_dong_bhxh))
    bhyt, bhyt1 = (round(v) for v in bảo_hiểm_y_tế(_luong_dong_bhxh))
    bhtn, bhtn1 = (round(v) for v in bảo_hiểm_thất_nghiệp(_luong_dong_bhxh))

    bh_tổng = bhxh + bhyt + bhtn

    GIAM_TRU_BAN_THAN = 11000000
    GIAM_TRU_NGUOI_PHU_THUOC = 4400000
    giảm_trừ_gia_cảnh = GIAM_TRU_BAN_THAN + GIAM_TRU_NGUOI_PHU_THUOC * số_người_phụ_thuộc

    thu_nhập_tính_thuế = luong_gross - bh_tổng - giảm_trừ_gia_cảnh
    thu_nhập_tính_thuế = thu_nhập_tính_thuế if thu_nhập_tính_thuế > 0 else 0

    if thu_nhập_tính_thuế == 0:
        thuế_bậc_5, thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = (
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        thuế = 0
    else:
        thuế_bậc_5, thuế_bậc_10, thuế_bậc_15, thuế_bậc_20, thuế_bậc_25, thuế_bậc_30, thuế_bậc_35 = (
            tinh_thue_theo_thang(thu_nhập_tính_thuế)
        )
        thuế = (
            thuế_bậc_5
            + thuế_bậc_10
            + thuế_bậc_15
            + thuế_bậc_20
            + thuế_bậc_25
            + thuế_bậc_30
            + thuế_bậc_35
        )

    lương_net = luong_gross - bh_tổng - thuế

    # Người sử dụng lao động trả
    bh_tai_nan_ld = round(bh_tnld_benh_nn(_luong_dong_bhxh))
    tong_bhxh1 = bhxh1 + bh_tai_nan_ld + bhyt1 + bhtn1
    tong1 = bhxh1 + bh_tai_nan_ld + bhyt1 + bhtn1 + luong_gross

    width = [26, 11]

    print(
        f"{'Lương Gross:':<{width[0]}}{fm(luong_gross):>{width[1]}}",
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
        "=============================================",
        "Nguời sử dụng lao động trả:",
        f"{'Bảo hiểm xã hội:':<{width[0]}}{fm(bhxh1):>{width[1]}}",
        f"{'Bảo hiểm tai nạn lao động:':<{width[0]}}{fm(bh_tai_nan_ld):>{width[1]}}",
        f"{'Bảo hiểm y tế:':<{width[0]}}{fm(bhyt1):>{width[1]}}",
        f"{'Bảo hiểm thất nghiệp:':<{width[0]}}{fm(bhtn1):>{width[1]}}",
        "---------------------------------------------",
        f"{'Tổng bhxh:':<{width[0]}}{fm(tong_bhxh1):>{width[1]}}",
        "---------------------------------------------",
        f"{'Tổng:':<{width[0]}}{fm(tong1):>{width[1]}}",
        "=============================================",
        f"{'Tổng BHXH:':<{width[0]}}{fm(tong_bhxh1 + bh_tổng):>{width[1]}}",
        f"{'Tổng BHXH + thue:':<{width[0]}}{fm(tong_bhxh1 + bh_tổng + thuế):>{width[1]}}",
        sep="\n",
    )
    return tong_bhxh1 + bh_tổng + thuế


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

    # bảng_lương_thang(luong_gross="79.662.000", số_người_phụ_thuộc=4)
    # bảng_lương_thang(luong_gross="30.000.000", luong_dong_bhxh="4.960.000")
    bảng_lương_thang(luong_gross="80.000.000")

    # bảng_lương_năm(
    #     tong_tnct="1.500.000.000",
    #     so_nguoi_phu_thuoc=4,
    #     tong_so_thang_phu_thuoc=12,
    #     bao_hiem_duoc_tru="30.000.000",
    #     so_thue_tncn_da_khau_tru="50.000.000",
    #     so_thue_tncn_da_tam_nop="20.000.000",
    # )
