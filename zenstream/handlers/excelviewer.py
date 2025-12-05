import streamlit as st
from os.path import sep
from openpyxl import load_workbook
from styler import Styler


class ExcelViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("Excel Viewer")
        st.text(file_name.split(sep)[-1])

        workbook = load_workbook(file_name)
        active = workbook.active.title
        Styler.show_dict(
            "Excel metadata",
            {
                "Sheets": str(len(workbook.sheetnames)),
                "Sheet names": str(workbook.sheetnames),
                "Active sheet": active,
            },
        )

        row_dict = {}
        sheet_data = workbook.active.values

        # Convert to a list of lists for easy processing
        data_list = list(sheet_data)
        for index, row in enumerate(data_list):
            row_dict[f"Row {index}"] = row[0] if row[0] else "-"
            if index > 9:
                break

        Styler.show_dict(f"**Rows for {active}**", row_dict)
