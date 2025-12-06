import streamlit as st
from styler import Styler
from docx import Document


class DocXViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("DocX Viewer")
        document = Document(file_name)
        paragraph_data = {
            f"Paragraph {index + 1}": paragraph.text
            for index, paragraph in enumerate(document.paragraphs)
        }

        Styler.show_dict("Paragrahs", paragraph_data)

        tables_data = {
            f"Table {index + 1}": str(DocXViewer._get_table_rows(table))
            for index, table in enumerate(document.tables)
        }

        Styler.show_dict("Tables", tables_data)

    @staticmethod
    def _get_table_rows(table) -> list:
        """Return a list of lists / tuples"""
        # [
        # ("",  "a", "b"),
        # ("c", "d", ""),
        # ("",  "e", ""),
        # ]

        def iter_row_cell_texts(row):  # -> Iterator[str]:
            for _ in range(row.grid_cols_before):
                yield ""
            for c in row.cells:
                yield c.text
            for _ in range(row.grid_cols_after):
                yield ""

        rows = [tuple(iter_row_cell_texts(r)) for r in table.rows]
        return rows
