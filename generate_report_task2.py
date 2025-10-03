import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

csv_path = ""
try:
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    csv_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files","*.csv")])
    root.destroy()
except Exception:
    pass

if not csv_path:
    csv_path = input("Enter full path to your CSV file (example: C:\\Users\\suhaina afreen\\Downloads\\sales_task2_friend.csv): ").strip()

if not os.path.exists(csv_path):
    print("ERROR: CSV file not found at this path:")
    print(csv_path)
    print("Make sure the file name is correct and has .csv extension.")
    raise SystemExit(1)

df = pd.read_csv(csv_path)
summary = df.groupby("Product")["Sales"].sum()
avg_sales = df["Sales"].mean()

output_dir = os.path.dirname(csv_path) or os.getcwd()
chart_path = os.path.join(output_dir, "sales_chart_task2_friend.png")
pdf_path = os.path.join(output_dir, "Sales_Report_Task2_Friend.pdf")

plt.figure(figsize=(8,5))
summary.plot(kind="bar", color="green")
plt.title("Total Sales by Product (Friend Task 2)")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(chart_path)
plt.close()

doc = SimpleDocTemplate(pdf_path)
styles = getSampleStyleSheet()
content = []

content.append(Paragraph("<b>Automated Sales Report - Friend Task 2</b>", styles["Title"]))
content.append(Spacer(1,12))
content.append(Paragraph(f"Average Sales: {avg_sales:.2f}", styles["Normal"]))
content.append(Spacer(1,12))
content.append(Paragraph("Sales Summary:", styles["Heading2"]))

for product, value in summary.items():
    content.append(Paragraph(f"{product}: {value}", styles["Normal"]))

content.append(Spacer(1,12))
content.append(Image(chart_path, width=400, height=300))
doc.build(content)

print("✅ Report Generated:", pdf_path)
try:
    os.startfile(pdf_path)
except Exception:
    pass
