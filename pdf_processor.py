import PyPDF2


def extract_pdf_text(uploaded_file):
    """
    Extract text from an uploaded PDF file.
    Returns extracted text as a string.
    """

    try:

        uploaded_file.seek(0)

        reader = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:

        return f"Error reading PDF: {str(e)}"


def get_pdf_information(uploaded_file):
    """
    Returns basic PDF information.
    """

    try:

        uploaded_file.seek(0)

        reader = PyPDF2.PdfReader(uploaded_file)

        info = {

            "Pages": len(reader.pages),

            "Encrypted": reader.is_encrypted

        }

        return info

    except Exception:

        return None