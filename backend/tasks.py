# pyright: reportMissingImports=false, reportMissingModuleSource=false
# .\venv\Scripts\activate
# celery -A main:cel_app worker -l INFO -P gevent


# sudo service redis-server start
# redis-cli
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
import ssl
from worker import celery_app
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import csv

templates_path = os.path.join(os.path.dirname(__file__), "templates")

env = Environment(
    loader=FileSystemLoader(templates_path),
    autoescape=select_autoescape()
)


email_body1 = """ Hey {},

We hope you've been enjoying our latest movie offerings at MovieCops! We value your patronage and want to ensure you never miss out on the best movie experiences.
We've noticed that it's been a while since your last booking with us. Don't miss the chance to catch the latest blockbusters on the big screen. As a valued customer, we have an exclusive offer waiting for you:

🎉 Book your tickets today and get 50% off your next movie experience! 🎉

Whether it's a thrilling action movie, a heartwarming romantic comedy, or a captivating adventure, we have something for everyone. Our comfortable seats, state-of-the-art sound system, and high-quality visuals await you.

Here's how to claim your discount:

1. Visit our website at http://localhost:8080/
2. Browse our selection of upcoming shows and movies.
3. Select your preferred showtime and seats.
4. Use the promo code: Promo Code is Auto Applied!.

This offer is valid for a limited time, so don't wait too long to make your booking. Treat yourself to a memorable movie experience and create lasting memories with friends and family.

Book now: http://localhost:8080/shows
Thank you for choosing MovieCops. We look forward to seeing you at the movies soon!

Best regards,
The MovieCops Team
"""

email_body2 = """ Hey {},

We're excited to have you as a loyal customer at MovieCops! You've recently enjoyed a fantastic movie experience with us, and we're here to let you know that the excitement continues.

🎬 Don't miss out on the amazing movies currently airing at our theater! 🎬

Whether you're in the mood for action, comedy, romance, or adventure, we have a variety of films that cater to all tastes. Our state-of-the-art facilities and comfortable seating are ready to provide you with another unforgettable cinematic journey.

Visit our website today to explore the latest showtimes and book your tickets. Grab your popcorn and get ready for a movie night you won't forget!

Explore showtimes: http://localhost:8080/shows
Thank you for choosing MovieCops. We can't wait to see you again!

Best regards,
The MovieCops Team
"""


def send_email(receiver_email, subject, message, html=None):
    try:
        email_sender = "moviecopsreminders@gmail.com"
        email_password = "gmgxrvchhvrgjfnq"

        em = EmailMessage()
        em['From'] = receiver_email
        em['To'] = email_sender
        em['Subject'] = subject

        if html:
            em.set_content("Please enable HTML to view this email.")
            em.add_alternative(html, subtype='html')
        else:
            em.set_content(message)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email_sender, email_password)
            server.sendmail(email_sender, receiver_email, em.as_string())
    except Exception as e:
        return str(e)

    return "Successfully sent email"


@celery_app.task
def email_task(user, last_booking):
    if last_booking:
        now = datetime.now()
        time_since_last_booking = now - last_booking
        if time_since_last_booking <= timedelta(minutes=1):
            return "Active User"
        else:
            email_subject = f"🍿 Lights, Camera, Action! Explore the Latest Movies at MovieCops 🎬 - {user['name']}"
            res = send_email(user["email"], email_subject,
                             email_body2.format(user["name"]))
            return res
    else:
        email_subject = f"🎉 Exclusive Offer: Book Your Tickets Now! - {user['name']}"
        res = send_email(user["email"], email_subject,
                         email_body1.format(user["name"]))
        return res


@celery_app.task
def monthly_report(user, bookings, month, year):
    if bookings:
        email_subject = f"🎉 Monthly Report - {user['name']}"
        template = env.get_template("report_template.html")
        html = template.render(month=month, year=year, bookings=bookings)
        res = send_email(user["email"], email_subject, None, html)
        return res
    return "No bookings found"


@celery_app.task
def export_csv(name, venue_data):
    if venue_data:
        filepath = "./exports/"+name+".csv"
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = venue_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data in venue_data:
                writer.writerow(data)
        return "CSV Exported"
    return "No bookings found"
