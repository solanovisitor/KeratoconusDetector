# Galilei G6 ML algorithm for keratoconus classification.

 You will find a script for preparing data (data_conformer.py) and 
a script for preprocessing and training with the data.

 This experiment is using a CNN plus an LSTM for binary classification, where:

 1 = Exam positive for keratoconus.
 0 = Exam with normal characteristics.

# Data conformer

This is a software to pull data from Galilei G6, an ophthalmologic equipment used for eye biometrics.

1. Clone the repository in your local machine.
2. Open the 'projeto_oft' folder in your terminal
3. Create a python3 virtualenv
4. Open your virtualenv with 'source .env/bin/activate'
5. pip install -r requirements_conform.txt
6. When requirements are installed, run the file as the following:

'python etl_task.py --path --out'

You can see this script takes 2 positional arguments:

1. path is the directory containing all patients.
2. out is the path for your output csv file.

The output should be a single csv per examination, containing 15 columns and 18k rows representing the measures.

# Training

For training, you should install "requirements_train.txt" in your env, using pip.

You can train the model by running:

"python3 train.py --pos_folder --neg_folder --job_dir"

Where:

1. pos_folder is the directory where all the positive class samples are.
2. neg_folder is the directory where all the negative class samples are.
3. job_dir is the directory pointed for saving the model and tensorboard.

# Making predictions

You can make predictions with the model by running:

"python3 predict.py --test_folder --model_path"

Where:

1. test_folder is the directory where your test data is.
2. model_path is the directory containing your h5 keras model.