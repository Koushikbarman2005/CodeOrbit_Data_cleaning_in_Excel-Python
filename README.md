# CodeOrbit_Data_cleaning_in_Excel-Python
Data cleaning projects using Microsoft Excel/ Python for my CodeOrbit Tech Data Analyst Internship.  
titanic_raw_messy.csv — original dataset with data issues. 
titanic_cleaned.csv — cleaned dataset. 
cleaning_log.txt — record of cleaning steps.
 Titanic_Data_Cleaning.xlsx — Excel workbook with raw data, cleaned data, summary, and log.
 
## Project 1: Data Cleaning in Excel/Python
A messy, realistic sample passenger dataset (modeled on the classic Titanic dataset) is cleaned, documented, and delivered in both Python/CSV and Excel formats.

**Result:** 79 raw rows → 64 clean rows, 0 missing values remaining.

**Files:**
- `make_messy_data.py` — generates the raw sample dataset
- `clean_data.py` — main cleaning script (documented, step-by-step)
- `build_cleaning_excel.py` — builds the formatted Excel deliverable
- `titanic_raw_messy.csv` — raw, uncleaned sample dataset
- `titanic_cleaned.csv` — final cleaned dataset
- `cleaning_log.txt` — auto-generated log of every cleaning step
- `Titanic_Data_Cleaning.xlsx` — Excel workbook: raw data, cleaned data, summary, log
- `Data_Cleaning_Report.docx` — written report documenting the process

**Run it:**
```bash
python make_messy_data.py     # (optional) regenerate raw sample data
python clean_data.py          # clean the data
python build_cleaning_excel.py  # (optional) rebuild the Excel workbook
```
