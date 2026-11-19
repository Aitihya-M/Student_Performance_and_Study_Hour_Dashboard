Student Study-Hours and Performance Dashboard

A beginner-friendly Python data analysis project that manages student records and studies the relationship between students' study hours and examination marks.

Features

- CSV and JSON files containing simulated student records
- "StudentRecord" class using object-oriented programming (OOP)
- Input validation for student IDs, course names, study hours and assessment scores
- Add, insert, delete, modify and display student records
- NumPy statistics: total students, average score, median score, average study hours, standard deviation, highest score and lowest score
- Pandas course-wise performance analysis
- Matplotlib graphs: study-hours-versus-score scatter plot and score-distribution histogram
- IQR and MAD methods for score-outlier detection
- Correlation analysis before and after IQR outlier filtering
- Menu-driven interface
- Data saved in both CSV and JSON formats
- Error handling for missing files, missing columns, invalid values and duplicate student IDs

Project structure

Student_Performance_and_Study_Hours_Dashboard/
├── student_performance_dashboard.py   # complete menu-driven application
├── requirements.txt                   # required Python libraries
├── student_data.csv                   # sample synthetic student dataset
├── student_data.json                  # same sample data in JSON format
├── Student_Performance_and_Study_Hours_Dashboard_Report.pdf
├── Student_Performance_and_Study_Hours_Dashboard_Report.docx
├── SUBMISSION_CHECKLIST.md             # final submission checklist
├── .gitignore
└── README.md

How to run (VS Code / Python)

1. Open the "Student_Performance_and_Study_Hours_Dashboard" folder in VS Code.

2. Open a terminal in VS Code.

3. (Recommended) Create and activate a virtual environment:
   
   python -m venv .venv
   
   Windows:
   
   .venv\Scripts\activate
   
   macOS/Linux:
   
   source .venv/bin/activate

4. Install the required libraries:
   
   python -m pip install -r requirements.txt

5. Run the application:
   
   python student_performance_dashboard.py

6. Choose an option from the menu. Choose option 12 to generate the sample dataset if the database is empty. Choose options 7–10 to view statistical analysis, course-wise analysis, graphs, and outlier/correlation analysis. Choose option 13 to save and exit.

Data files

The application loads "student_data.csv" when it exists. If the CSV file is not present, it attempts to load "student_data.json". Saving data writes both formats. The included sample records are synthetic demonstration data, not real student observations.

Note

Correlation describes an association between study hours and assessment scores. It does not prove that studying for more hours directly causes higher marks. The sample dataset is simulated and should not be treated as evidence about real students.

