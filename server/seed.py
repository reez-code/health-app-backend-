#!/usr/bin/env python3

from app import app
import random
from models import db,Patient, Department
from faker import Faker

faker = Faker()

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Department.query.delete()
    Patient.query.delete()
    
    department_names = [
    "Cardiology",
    "Orthopedics",
    "Neurology",
    "Oncology",
    "Pediatrics",
    "Dermatology",
    "Gynecology",
    "Urology",
    "Ophthalmology",
    "ENT (Ear, Nose, Throat)",
    "Radiology",
    "Emergency Medicine",
    "Anesthesiology",
    "Psychiatry",
    "Physical Therapy",
    "Internal Medicine",
    "Surgery",
    "Pathology",
    "Gastroenterology",
    "Endocrinology"
]
    
    
    print("Creating departments...")
    
    departments=[]
    for i in range(20):
        department=Department(
            name=random.choice(department_names)
        )
        departments.append(department)
    
    disease_list = [
    "Common Cold",
    "Influenza (Flu)",
    "Pneumonia",
    "Bronchitis",
    "Asthma",
    "Chronic Obstructive Pulmonary Disease (COPD)",
    "Hypertension (High Blood Pressure)",
    "Coronary Artery Disease",
    "Heart Failure",
    "Stroke",
    "Diabetes Mellitus",
    "Hypothyroidism",
    "Hyperthyroidism",
    "Obesity",
    "Arthritis",
    "Osteoporosis",
    "Rheumatoid Arthritis",
    "Gastroesophageal Reflux Disease (GERD)",
    "Peptic Ulcer Disease",
    "Irritable Bowel Syndrome (IBS)",
    "Inflammatory Bowel Disease (IBD)",
    "Gallstones",
    "Kidney Stones",
    "Urinary Tract Infection (UTI)",
    "Benign Prostatic Hyperplasia (BPH)",
    "Erectile Dysfunction (ED)",
    "Anxiety Disorders",
    "Depressive Disorders",
    "Bipolar Disorder",
    "Schizophrenia",
    "Attention Deficit Hyperactivity Disorder (ADHD)",
    "Alzheimer's Disease",
    "Parkinson's Disease",
    "Multiple Sclerosis (MS)",
    "Migraine",
    "Epilepsy",
    "Cancer (Various Types)",
    "Human Immunodeficiency Virus (HIV) Infection",
    "Acquired Immunodeficiency Syndrome (AIDS)",
    "Chlamydia",
    "Gonorrhea",
    "Syphilis",
    "Hepatitis (Various Types)",
    "Tuberculosis (TB)",
    "Malaria",
    "Dengue Fever",
    "Chikungunya Fever",
    "Zika Virus Infection",
    "Ebola Virus Disease",
    "COVID-19 (Coronavirus Disease)"
]
    
    
    # Creating patients
    print("Creating patients...")
    patients = []
    for _ in range(30):
        patient = Patient(
            name=faker.name(),
            age=faker.random_int(min=18, max=90),
            gender=random.choice(["Male", "Female"]),
            phone_number=faker.phone_number(),
            diagnosis=random.choice(disease_list),
            email=faker.email());
        
        patients.append(patient)
            
    db.session.add_all(departments)
    db.session.add_all(patients)
    db.session.commit()
    
    
    print("Seeding done!")