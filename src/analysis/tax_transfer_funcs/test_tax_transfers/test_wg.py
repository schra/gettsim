import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from src.analysis.tax_transfer_funcs.test_tax_transfers.auxiliary_test_tax import (
    load_input,
)
from src.analysis.tax_transfer_funcs.test_tax_transfers.auxiliary_test_tax import (
    load_output,
)
from src.analysis.tax_transfer_funcs.test_tax_transfers.auxiliary_test_tax import (
    load_tb,
)
from src.analysis.tax_transfer_funcs.benefits import wg


input_cols = [
    "pid",
    "hid",
    "tu_id",
    "head_tu",
    "hh_korr",
    "hhsize",
    "child",
    "miete",
    "heizkost",
    "alleinerz",
    "child11_num_tu",
    "cnstyr",
    "m_wage",
    "m_pensions",
    "ertragsanteil",
    "m_alg1",
    "m_transfers",
    "uhv",
    "gross_e1",
    "gross_e4",
    "gross_e5",
    "gross_e6",
    "incometax",
    "rvbeit",
    "gkvbeit",
    "handcap_degree",
    "divdy",
    "year",
    "hhsize_tu",
]
years = [2006, 2009, 2013, 2016]


@pytest.mark.parametrize("year", years)
def test_wg(year):
    file_name = "test_dfs_wg.xlsx"
    columns = ["wohngeld_basis_hh"]
    df = load_input(year, file_name, input_cols)
    tb = load_tb(year)
    tb["yr"] = year
    calculated = pd.DataFrame(columns=columns)
    for hid in df["hid"].unique():
        calculated = calculated.append(wg(df[df["hid"] == hid], tb)[columns])
    expected = load_output(year, file_name, columns)
    print("calculated: \n", calculated, "\n\n")
    print("expected: \n", expected)
    assert_frame_equal(calculated, expected)