import csv
import random
import string

def generate_name():
    return "Student" + str(random.randint(1, 300))

def generate_gender():
    return random.choice(['Male', 'Female'])

def generate_score():
    return random.randint(60, 100)

with open('students_data_300.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Name', 'Gender', 'Score'])

    for i in range(1, 301):
        writer.writerow([i, generate_name(), generate_gender(), generate_score()])

print("CSV file generated successfully.")