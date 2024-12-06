from fpdf import FPDF
import os

class PDFGeneratorAgent:
    def __init__(self, name="PDF Generator Agent"):
        self.name = name

    def generate_pdf(self, blog_content, blog_number):

        clean_content = blog_content.encode('latin1', 'replace').decode('latin1')
        # Create PDF instance
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set title font
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, txt=f"Generated Blog {blog_number}", ln=True, align='C')

        # Add a line break
        pdf.ln(10)

        # Set content font
        pdf.set_font('Arial', '', 12)

        # Add the blog content
        pdf.multi_cell(0, 10, clean_content)

        # Save the PDF to a file
        pdf_output_dir = 'generated_pdfs'
        if not os.path.exists(pdf_output_dir):
            os.makedirs(pdf_output_dir)

        pdf_output_path = os.path.join(pdf_output_dir, f"generated_blog{blog_number}.pdf")
        pdf.output(pdf_output_path)

        return pdf_output_path
