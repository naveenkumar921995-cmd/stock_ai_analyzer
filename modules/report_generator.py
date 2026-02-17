from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st

def generate_pdf(stock):

    doc = SimpleDocTemplate("stock_report.pdf")
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Stock Report - {stock}", styles['Title']))
    elements.append(Spacer(1,12))

    doc.build(elements)

    st.success("PDF Generated Successfully")

