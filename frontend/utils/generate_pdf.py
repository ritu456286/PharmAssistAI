from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

# Function to generate PDF
def generate_invoice_pdf(invoice_data, invoice_items):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # PDF Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Invoice Details")

    # Invoice Details
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 720, f"Invoice ID: {invoice_data['id']}")
    pdf.drawString(50, 700, f"Date: {invoice_data['invoice_date']}")
    pdf.drawString(50, 680, f"Patient: {invoice_data['patient_name']}")
    pdf.drawString(50, 660, f"Doctor: {invoice_data['doctor_name']}")
    pdf.drawString(50, 640, f"Clinic: {invoice_data['clinic_name']}")

    # Table Headers & Data
    table_data = [["ID", "Name", "Dosage", "Qty", "Unit Price (Rs.)", "Total (Rs.)"]]  # Table Headers
    for med in invoice_items:
        if med["quantity"] > 0:
            table_data.append([
                med["id"], med["name"], med.get("dosage", "N/A"),
                med["quantity"], f"Rs. {med['price']:.2f}", f"Rs. {med['total_price']:.2f}"
            ])

    # Create Table
    table = Table(table_data, colWidths=[50, 100, 100, 50, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header Background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header Text Color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center Align All
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold Headers
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid Lines
    ]))

    table.wrapOn(pdf, 400, 500)
    table.drawOn(pdf, 50, 550)  # Adjust Table Position

    # Total Amount
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 520, f"Total Amount: ₹{invoice_data['total_amount']:.2f}")

    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer