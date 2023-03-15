import os
import tempfile
import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import psycopg2 as pg
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as datef
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfFileMerger
from zenpy import Zenpy
from zenpy.lib.api_objects import Comment
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
)
from PIL import Image


# Configuration
CONFIG = {
    "db_name": "your_dbname",
    "db_host": "your_host",
    "db_port": 5439,
    "db_user": "username",
    "db_password": "password",
    "pdf_merger": PdfFileMerger(),
    "email": "your_email",
    "token": "your_ZenDesk_token",
    "subdomain": "your_customer_name_from_ZenDesk",
    "reference_sheet_path": Path("C:/ComputerName/ReferenceSheet.csv"),
}


def get_database_connection():
    return pg.connect(
        dbname=CONFIG["db_name"],
        host=CONFIG["db_host"],
        port=CONFIG["db_port"],
        user=CONFIG["db_user"],
        password=CONFIG["db_password"],
    )


def query_database(query):
    with get_database_connection() as connection:
        return pd.read_sql_query(query, con=connection)


def search_tickets():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=62)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    today = datetime.datetime.now()
    today = today.replace(hour=23, minute=59, second=0, microsecond=0)

    creds = {
        "email": CONFIG["email"],
        "token": CONFIG["token"],
        "subdomain": CONFIG["subdomain"],
    }
    zenpy_client = Zenpy(**creds)

    return zenpy_client.search(
        created_between=[yesterday, today],
        group="Data Analytics",
        type="ticket",
        status=["new", "open"],
        minus="negated",
    )


def get_chart_data(name, search_type):
    query = f"""Add your SQL Query with f string command to automatically generate {search_type} charts by name;"""
    return query_database(query)


def get_ref_dataframe():
    return pd.read_csv(CONFIG["reference_sheet_path"])


def get_sql_name(ticket):
    custom_field = ticket.custom_fields[5]
    return custom_field[27 : len(custom_field) - 2]


def resize_images(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [
        im.resize(
            (min_width,
if name == ref.iloc[i, 0]:
name = ref.iloc[i, 1]
print(name)
for report in ["Report1", "Report2", "Report3", "Report4"]:
chart_data = q_search(name, report)
if len(chart_data) > 0:
# Create chart with seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.set_palette("colorblind")
sns.lineplot(x="date", y="count", data=chart_data, hue="category", ax=ax)
plt.title(f"{name} {report} Chart")
plt.ylabel("Count")
plt.xlabel("Date")
plt.legend(title="Category", loc="upper left", bbox_to_anchor=(1.05, 1))
plt.tight_layout()

        # Save chart to temp file and convert to PDF
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            plt.savefig(tmp_file, format="png")
            tmp_file.flush()
            with convert_from_path(tmp_file.name) as pdf_pages:
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
                    pdf_file_path = pdf_file.name
                    Image.open(pdf_pages[0]).save(pdf_file, "PDF", resolution=100.0)
                    os.unlink(tmp_file.name)

                    # Create ZenDesk ticket with PDF attachment
                    ticket_body = f"{name} {report} chart for {today.strftime('%m/%d/%Y')}"
                    ticket = zenpy_client.tickets.create(
                        Comment(
                            body=ticket_body,
                            uploads=[pdf_file_path],
                        ),
                        subject=f"{name} {report} chart {today.strftime('%m/%d/%Y')}",
                        group_id=your_group_id,
                        requester={'name': 'your_name', 'email': 'your_email'},
                    )

                    print(f"Created ticket: {ticket.ticket.id}")

                    # Save PDF to list for merging
                    pdf_paths = []
                    pdf_paths.append(pdf_file_path)

print(f"Finished charts and tickets for {name}\n")

#Merge all generated PDFs into one document
with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as merged_file:
merged_file_path = merged_file.name
pdf_append(pdf_paths, merged_file_path)
print(f"Merged PDFs to {merged_file_path}")


# Create ZenDesk ticket with merged PDF attachment
ticket_body = f"Charts for {today.strftime('%m/%d/%Y')}"
ticket = zenpy_client.tickets.create(
    Comment(
        body=ticket_body,
        uploads=[merged_file_path],
    ),
    subject=f"All charts {today.strftime('%m/%d/%Y')}",
    group_id=your_group_id,
    requester={'name': 'your_name', 'email': 'your_email'},
)

print(f"Created ticket: {ticket.ticket.id}")

#Cleanup
os.unlink(merged_file_path)

creds1 = {
    "email": "your_email",
    "token": "your_ZenDesk_token",
    "subdomain": "your_customer_name_from_ZenDesk",
}
zenpy_client = Zenpy(**creds1)

yesterday = datetime.datetime.now() - datetime.timedelta(days=62)
yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0) # Returns a copy
today = datetime.datetime.now()
today = today.replace(hour=23, minute=59, second=0, microsecond=0) # Returns a copy

for ticket in zenpy_client.search(
    created_between=[yesterday, today],
    group="Data Analytics",
    type="ticket",
    status=['new', 'open'],
    minus='negated'
):
    print(ticket)
    print(ticket.custom_fields[5])
    # using custom field 5 to find SQL name for each generated ticket location
    for_name = str(ticket.custom_fields[5])
    name = for_name[27 : len(for_name) - 2]
    for i in range(len(ref)):
        if name == ref.iloc[i, 0]:
            name = ref.iloc[i, 1]
            break

    # Checking if there are existing ticket replies that include charts
    # Making a list of any chart attachments already in the ticket
    current_attachments = []
    for comment in ticket.comments:
        attachments = comment.attachments
        for attachment in attachments:
            current_attachments.append(attachment.file_name)

    # Only generating charts if no charts exist in the ticket replies
    if "D" not in ticket


