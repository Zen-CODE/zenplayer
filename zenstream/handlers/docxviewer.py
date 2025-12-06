import streamlit as st
from styler import Styler
from docx import Document
import re


class DocXViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("DocX Viewer")
        document = Document(file_name)

        Styler.show_dict(
            "Metadata",
            {
                "Author": document.core_properties.author,
                "Category": document.core_properties.category,
                "Comments": document.core_properties.comments,
                "Status": document.core_properties.content_status,
                "Created": document.core_properties.created,
                "Identifier": document.core_properties.identifier,
                "Keywords": document.core_properties.keywords,
                "Language": document.core_properties.language,
                "Last modified by": document.core_properties.last_modified_by,
                "Revision": document.core_properties.revision,
                "Subject": document.core_properties.subject,
                "Title": document.core_properties.title,
                "Version": document.core_properties.version,
            },
        )

        paragraph_data = {
            f"Paragraph {index + 1}": DocXViewer._format_text(paragraph.text)
            for index, paragraph in enumerate(document.paragraphs)
        }

        Styler.show_dict("Paragraphs", paragraph_data)

        tables_data = {
            f"Table {index + 1}": str(DocXViewer._get_table_rows(table))
            for index, table in enumerate(document.tables)
        }

        Styler.show_dict("Tables", tables_data)

    @staticmethod
    def _format_text(text: str) -> str:
        """Remove non-readable characters"""
        control_char_pattern = r"[\x00-\x1F\x7F]"
        return re.sub(control_char_pattern, "", text)

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
