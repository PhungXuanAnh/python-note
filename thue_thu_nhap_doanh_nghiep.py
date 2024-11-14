# -*- coding: utf-8 -*-
# mypy: ignore-errors
# cSpell:disable

from functools import partial

from babel.numbers import format_decimal

fm = partial(format_decimal, locale="vi_VN")

ke_toan = 2000000

doanh_thu = eval("".join("150.000.000".split(".")))

thue_bhxh_1_ld = eval("".join("3.633.040".split(".")))
chi_phi_nhan_cong = eval("".join("31.066.400".split(".")))
so_luong_lao_dong = 4
thue_bhxh_nld = thue_bhxh_1_ld * so_luong_lao_dong
tong_chi_phi_nhan_cong = chi_phi_nhan_cong * so_luong_lao_dong

thu_nhap_chiu_thue = doanh_thu - chi_phi_nhan_cong * so_luong_lao_dong
thue_tndn = round(thu_nhap_chiu_thue * 0.2)
tong_thue_bhxh_ketoan = thue_bhxh_nld + thue_tndn + ke_toan
loi_nhuan_sau_thue = doanh_thu - tong_thue_bhxh_ketoan

width = [30, 12]

print(
    "---------------------------------------------",
    f"{'Doanh thu:':<{width[0]}}{fm(doanh_thu):>{width[1]}}",
    f"{'Tổng lương:':<{width[0]}}{fm(tong_chi_phi_nhan_cong):>{width[1]}}",
    f"{'Thu nhap chiu thue:':<{width[0]}}{fm(thu_nhap_chiu_thue):>{width[1]}}",
    f"{'Thue tndn:':<{width[0]}}{fm(thue_tndn):>{width[1]}}",
    f"{'Thue + bhxh nld:':<{width[0]}}{fm(thue_bhxh_nld):>{width[1]}}",
    "---------------------------------------------",
    f"{'tong_thue_bhxh_ketoan:':<{width[0]}}{fm(tong_thue_bhxh_ketoan):>{width[1]}}",
    f"{'loi_nhuan_sau_thue:':<{width[0]}}{fm(loi_nhuan_sau_thue):>{width[1]}}",
    sep="\n",
)
