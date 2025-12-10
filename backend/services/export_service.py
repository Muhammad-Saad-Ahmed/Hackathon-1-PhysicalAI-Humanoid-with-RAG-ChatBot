from typing import Dict, Any, List, Tuple
from weasyprint import HTML
import markdown2
from ebooklib import epub
import uuid

class ExportService:
    """
    Service for exporting textbook content to various formats.
    """

    def __init__(self):
        pass

    def export_to_pdf(self, content_markdown: str, filename: str = "textbook.pdf", format_preferences: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Converts markdown content to a PDF file, applying format preferences if provided.

        Args:
            content_markdown: The textbook content in Markdown format.
            filename: The desired output filename for the PDF.
            format_preferences: Optional dictionary of format preferences (e.g., font_size, layout).

        Returns:
            The PDF file content as bytes.
        """
        # Convert Markdown to HTML
        html_content = markdown2.markdown(content_markdown, extras=["tables", "fenced-code-blocks"])

        # Dynamic CSS based on format_preferences
        font_size = format_preferences.get("font_size", "medium") if format_preferences else "medium"
        layout = format_preferences.get("layout", "standard") if format_preferences else "standard"

        body_style = "font-family: sans-serif;"
        if font_size == "small":
            body_style += " font-size: 0.8em;"
        elif font_size == "large":
            body_style += " font-size: 1.2em;"

        margin_style = "2cm;"
        if layout == "compact":
            margin_style = "1cm;"
        elif layout == "spacious":
            margin_style = "3cm;"
        body_style += f" margin: {margin_style};"


        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Textbook</title>
            <meta charset="utf-8">
            <style>
                body {{ {body_style} }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; }}
                pre {{ background-color: #eee; padding: 10px; border-radius: 5px; }}
                code {{ font-family: monospace; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Generate PDF from HTML
        pdf_bytes = HTML(string=html_template).write_pdf()
        return pdf_bytes

    def export_to_epub(self, title: str, author: str, chapter_markdown: List[Tuple[str, str]], format_preferences: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Converts textbook content (list of chapter markdown) to an EPUB file, applying format preferences if provided.

        Args:
            title: The title of the textbook.
            author: The author of the textbook.
            chapter_markdown: A list of tuples, where each tuple contains (chapter_title, chapter_markdown_content).
            format_preferences: Optional dictionary of format preferences (e.g., font_size, layout).

        Returns:
            The EPUB file content as bytes.
        """
        book = epub.EpubBook()

        # Set metadata
        book.set_identifier(str(uuid.uuid4()))
        book.set_title(title)
        book.set_language('en')
        book.add_author(author)

        # Dynamic CSS based on format_preferences
        font_size_css = ""
        if format_preferences:
            if format_preferences.get("font_size") == "small":
                font_size_css = "font-size: 0.8em;"
            elif format_preferences.get("font_size") == "large":
                font_size_css = "font-size: 1.2em;"
            # Layout preferences are more about rendering, less direct CSS in EPUB chapters

        style = 'body { font-family: sans-serif; }'
        if font_size_css:
            style += f' body {{ {font_size_css} }}'

        default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
        book.add_item(default_css)


        chapters = []
        for i, (chapter_title, markdown_content) in enumerate(chapter_markdown):
            # Convert markdown to HTML for EPUB
            html_content = markdown2.markdown(markdown_content, extras=["tables", "fenced-code-blocks"])

            # Create chapter
            c = epub.EpubHtml(title=chapter_title, file_name=f'chap_{i+1}.xhtml', lang='en')
            c.content = f'<h1>{chapter_title}</h1>\n{html_content}'
            c.add_item(default_css) # Link the CSS to each chapter
            book.add_item(c)
            chapters.append(c)

        # Define table of contents
        book.toc = tuple(chapters)

        # Add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define spine (order of chapters)
        book.spine = ['nav'] + chapters

        # Write the EPUB file to memory
        epub_bytes = epub.write_epub(None, book, {})
        return epub_bytes
