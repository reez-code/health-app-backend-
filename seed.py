from faker import Faker
from datetime import datetime
from random import choice as rc
from app import app
from models import db, Doctor, Appointment, Admin

fake = Faker()

doctor_specialisations = [
    "Cardiology", "Orthopedic Surgery", "Neurology", "Oncology", "Pediatrics",
    "Dermatology", "Gynecology", "Urology", "Ophthalmology", "Ear, Nose, and Throat (ENT)",
    "Radiology", "Emergency Medicine", "Anesthesiology", "Psychiatry", "Physical Therapy",
    "Internal Medicine", "General Surgery", "Pathology", "Gastroenterology", "Endocrinology",
    "Hematology", "Pulmonology", "Rheumatology", "Infectious Disease", "Nephrology",
    "Geriatrics", "Cardiothoracic Surgery", "Plastic Surgery", "Neurosurgery", "Oncologic Surgery",
    "Hand Surgery", "Vascular Surgery", "Bariatric Surgery", "Oncologic Pathology",
    "Forensic Pathology", "Pediatric Surgery", "Hepatology", "Reproductive Endocrinology",
    "Allergy and Immunology", "Clinical Genetics", "Pain Medicine", "Sleep Medicine",
    "Sports Medicine", "Vascular Medicine", "Infectious Disease Medicine", "Neurophysiology",
    "Interventional Radiology", "Radiation Oncology", "Palliative Medicine", "Occupational Medicine"
]

appointment_reasons = [
    "Routine Checkup", "Follow-up Consultation", "Vaccination", "Prescription Refill",
    "Blood Test", "X-ray or Imaging", "Physical Therapy Session", "Dental Checkup",
    "Mental Health Counseling", "Surgical Consultation", "Chronic Disease Management",
    "Pregnancy Monitoring", "Allergy Testing", "Orthopedic Evaluation", "Hearing Test",
    "Eye Examination", "Dermatological Evaluation", "Cancer Screening", "Emergency Room Visit",
    "Second Opinion Consultation"
]


doctor_image=[
    "https://i.ibb.co/m6hfBgj/doctor1f.jpg",
    "https://i.ibb.co/kcqM90m/doc1m.jpg",
    "https://i.ibb.co/KyskyQL/doc2f.jpg",
    "https://i.ibb.co/Jz6GPXg/doc2m-jpeg.jpg",
    "https://i.ibb.co/fnB9vGr/doc3m.jpg",
    "https://i.ibb.co/SRydDxq/doc3f.jpg",
    "https://i.ibb.co/TB4pjGs/doc5m.jpg",
    "https://i.ibb.co/WPS8bzG/doc4f.webp",
    "https://i.ibb.co/tJ1P85s/doc5f.jpg",
    "https://i.ibb.co/1LRrWwh/doc6f.jpg",
    "https://i.ibb.co/vQVdjmQ/doc7f.jpg",
    "https://i.ibb.co/LghN8j8/doc8f.jpg",
    "https://i.ibb.co/JQDfkbx/doc9f.jpg",
    "https://i.ibb.co/nLYW72Y/doc10f.jpg",
    "https://i.ibb.co/hXxTnLt/doc6m.jpg",
    "https://i.ibb.co/MnmJ3pJ/doc7m.jpg",
    "https://i.ibb.co/mSR3LM7/doc8m.jpg",
    "https://i.ibb.co/0Mb7j7q/docm10.jpg"
]

admin_roles = [
    "Routine Checkup", "Follow-up Consultation", "Vaccination", "Prescription Refill",
    "Blood Test", "X-ray or Imaging", "Physical Therapy Session", "Dental Checkup",
    "Mental Health Counseling", "Surgical Consultation", "Chronic Disease Management",
    "Pregnancy Monitoring", "Allergy Testing", "Orthopedic Evaluation", "Hearing Test",
    "Eye Examination", "Dermatological Evaluation", "Cancer Screening", "Emergency Room Visit",
    "Second Opinion Consultation"
]

with app.app_context():
    # This will delete any existing rows
    print("Deleting data...")
    db.session.query(Doctor).delete()
    db.session.query(Appointment).delete()
    db.session.query(Admin).delete()
    db.session.commit()

    # creating doctors
    print("creating doctors...")
    doctors = []
    for i in range(15):
        doctor = Doctor(
            name=fake.name(),
            email=fake.email(),
            specialization=rc(doctor_specialisations),
            phone=fake.phone_number(),
            password=fake.password(length=10),
            image=rc(doctor_image)
        )
        doctors.append(doctor)
    db.session.add_all(doctors)
    db.session.commit()

    #creating appointments
    print("creating appointments...")
    appointments = []
    for i in range(20):
        appointment = Appointment(
            reason=rc(appointment_reasons),
            timestamp=fake.date_time_this_year(before_now=True, after_now=False)
        )
        appointments.append(appointment)
    db.session.add_all(appointments)
    db.session.commit()

    #creating admins
    print("creating admins...")
    admins = []
    for i in range(5):
        admin = Admin(
            name=fake.name(),
            email=fake.email(),
            role=rc(admin_roles),
            password=fake.password(length=10),  # Use a strong password generator for production
            phone=fake.phone_number()
        )
        admins.append(admin)
    db.session.add_all(admins)
    db.session.commit()

print("Database seeded successfully.")
