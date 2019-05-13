# DYNAMOD - Dynamic Modelling of the German Tax Transfer System #

## Technical Remarks
- In order to clone including submodules, please clone via `git clone --recurse-submodules https://git.econ.tools/dynamod/dynamod.git` .
- The data for the test cases are prepared in Excel as we make use of formulas. When opening these files in Libreoffice Calc, boolean values (e.g. for `child` oder `east`) might be displayed as `0/1` instead of `TRUE/FALSE`. 
Changing the tests with calc might hence lead to failure, as the function requires the `pandas` boolean type. **Remedy:** Change the format in Calc to *booelan* by selecting the respective cells and hitting `Ctrl+1`.
- The data preparation is outsourced into separate repositories. In order to work smoothly, place these repos into the same root folder as this repo. 
Alternatively, you may change the respective path (`SOEP_PATH`, `SIAB_PATH`, etc.) in `wscript`. 

## Assumptions in SOEP data preparation
- A household member is defined as a child if (under 18) or (under 25 and in education). Unless it's the household head or his/her partner
- Earnings:
  - Monthly earnings are summed up from earnings from all jobs. This is a simplification as the 2nd job might be tax-free if it's paid below 450€. 
  - To this, other wage components (13th salary, bonus payments) are added. Since this information stems from the previous year, it is divided by the number of months in work.
  - If "stellung im Beruf" is self-employed, these earnings count as self-employed income `m_self`. Otherwise, it's labor income `m_wage`.
- Non-workers are assigned a potential hourly wage via Heckman Imputation. (function `heckman()` in `2_prepare_data.py`)
- `m_transfers` encompasses all private transfers (alimony mainly) and public transfers which we do not simulate (e.g. Parental Benefit, BaföG)
- Renting costs `hgrent` and heating costs `hgheat` exhibit many missings. Missing values are imputed in order to have some idea on benefit claim. It's better to be somewhat off than to assume no renting costs.

## Implicit Assumptions in Tax-Benefit calculations ##

- Calculation of taxable income (`zve()`): 
  - In lack of more detailed information, we always deduct the lumpsum amount `werbung` (currently € 1000) which is the lower bound
  - The same holds for Sonderausgaben (`sonder` = € 36)
- Income Tax Calculation:
  - married couples are assumed to file jointly. This is not a brave assumption; they are always better off that way.
- Housing Benefit (Wohngeld):
  - There is an upper threshold `tg["wgmax?p_m"], (? = [1,2,4,5,plus5])` up to which rents are considered in the wohngeld formula. These values differ by *Mietstufe* (I: Eifel village , V: Bonn, VI: Köln).
We don't know the municipality and hence the Mietstufe. We assume instead Mietstufe III for *everyone*, which is supposed to capture a medium level. This leads to undercoverage of housing benefit in large, expensive cities.
- Unemployment Benefit (ALG 2):
  - Housing costs are paid if *appropriate*.
    - We cap rents to €10 per square meter. In 2017, actual acknowledged cost of ALG2 recipients were in average between €8 and €9.
    - There is a *Faustregel* on the maximum size of the flat:
	  - For Renters: 45 sqm plus 15 sqm for each additional person
	  - For Owners: 80 sqm plus 20 sqm for each additional person after third
    - *Kosten der Unterkunft* (`alg2_kdu`) are hence calculated by maximum 10€ per sqm, multiplied by minimum of actual flat size and Faustregel.
- For the Asset Test, we impute assets via capital income and some average interest rate (tb['r_assets']). This should be replaced by either imputed wealth from EVS, or wealth observed in SOEP wave 2017.
