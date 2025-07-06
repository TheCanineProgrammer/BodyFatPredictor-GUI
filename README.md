# BodyFatPredictor-GUI

A desktop app built with **Tkinter**, **SQLite**, and **scikit-learn** that predicts body fat percentage using a **Decision Tree Regressor** model. Users can register and log in, view their BMI and body fat stats, visualize their health data, and export it to Excel.

---

## 🔧 Features

- 🔐 **User Authentication**: Register/login system with SQLite backend
- 🧍 **Body Fat Prediction** using a trained Decision Tree Regressor
- 📊 **BMI Classification** (e.g., Underweight, Normal, Overweight, Obese)
- 📈 **Chart Visualization** comparing user to dataset
- 📁 **Export to Excel** to save user data locally

---

## 🧪 Technologies Used

- Python `tkinter` (GUI)
- `sqlite3` (Database)
- `scikit-learn` (Machine Learning)
- `matplotlib` (Charting)
- `xlsxwriter` or `pandas` (Excel export)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/TheCanineProgrammer/BodyFatPredictor-GUI.git
cd BodyFatPredictor-GUI
```

### 2. Install Requirements

Run this command to install all necessary Python packages:

```bash
pip install -r requirements.txt
```

### 3. Run the app

Run the following command to start the application:

```bash
python Body-Fat-Prediction.py
```

## 📂 How It Works

- **Register:** New users provide their ID, weight, height, and age.

- **Login:** Existing users log in using their ID.

- **Prediction:** The app calculates BMI and predicts body fat percentage.

- **Visualization:** View your data in comparison to the dataset.

- **Export:** Save your profile info as an Excel file.

## 📁 Database

The app uses a local SQLite database (`server.db`).

The database is only created if it doesn't already exist.

## 🧠 Model Info

- Trained using a Decision Tree Regressor on a dataset of body measurements.
- ⚠️ **Disclaimer:** The model is not highly accurate or fine-tuned. It's intended for demonstration and learning purposes only.

## 📸 Screenshots

- **Welcome screen**  
  ![Welcome screen](https://github.com/TheCanineProgrammer/BodyFatPredictor-GUI/blob/main/Images/Welcome.png)

- **Register**  
  ![Register](https://github.com/TheCanineProgrammer/BodyFatPredictor-GUI/blob/main/Images/Register.png)

- **Login**  
  ![Login](https://github.com/TheCanineProgrammer/BodyFatPredictor-GUI/blob/main/Images/Login.png)

- **Info**  
  ![Info](https://github.com/TheCanineProgrammer/BodyFatPredictor-GUI/blob/main/Images/Info.png)

- **Excel export**  
  ![Excel export](https://github.com/TheCanineProgrammer/BodyFatPredictor-GUI/blob/main/Images/Excel.png)


### 💡 Contributions Welcome!

This project is open for improvement! If you'd like to:
- Improve the model (tuning, cross-validation, feature selection)
- Refactor the GUI or structure
- Add tests or better error handling

Feel free to open a pull request or submit an issue. All contributions are welcome!
