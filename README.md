# Data conformer for Galilei G6

This is a software to pull data from Galilei G6, used for eye biometrics.

1. Clone the repository in your local machine.
2. Open the 'projeto_oft' folder in your terminal
3. Create a python3 virtualenv
4. Open your virtualenv with 'source .env/bin/activate'
5. pip install -r requirements.txt
6. When requirements are installed, run the file as the following:

'python data_conform.py --patient --path --out'

You can see this script takes 3 positional arguments:

1. Patient: The ID number of the patient.
2. Path: The path for your directory containing all patients.
3. Out: The path for your output csv file.

The output should be a single csv with 15 columns and 18k rows representing the measures.
