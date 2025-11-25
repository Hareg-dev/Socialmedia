import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_and_train_model():
    # Load dataset
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
               "DiabetesPedigreeFunction", "Age", "Outcome"]
    data = pd.read_csv(url, names=columns)

    # Split data
    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest
    rf_clf = RandomForestClassifier(random_state=42, n_estimators=100)
    rf_clf.fit(X_train, y_train)

    # Evaluate
    y_pred = rf_clf.predict(X_test)
    print(f"Random Forest Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred))

    return rf_clf

def complex_rule_check(patient):
    # More detailed heuristics based on medical domain knowledge:
    
    # Rule 1: Very high glucose level
    if patient["Glucose"] > 180:
        return 1  # High chance of diabetes
    
    # Rule 2: Combination of BMI and Age
    if patient["BMI"] > 30 and patient["Age"] > 45:
        return 1
    
    # Rule 3: Low insulin but high glucose
    if patient["Insulin"] < 50 and patient["Glucose"] > 140:
        return 1
    
    # Rule 4: Multiple pregnancies + high BMI
    if patient["Pregnancies"] > 3 and patient["BMI"] > 35:
        return 1
    
    # Rule 5: Normal case
    if patient["Glucose"] < 100 and patient["BMI"] < 25 and patient["Age"] < 30:
        return 0  # Likely no diabetes
    
    return None  # No conclusion from rules

def combined_predict(patient, model):
    rule_result = complex_rule_check(patient)
    if rule_result is not None:
        print("[Rule-based] Diagnosis triggered.")
        return rule_result
    else:
        ml_result = model.predict([patient.values])[0]
        print("[ML Model] Diagnosis predicted.")
        return ml_result

def get_input(prompt, value_type=float):
    while True:
        try:
            val = value_type(input(prompt))
            return val
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def medical_chatbot(model):
    print("Welcome to MedBot! I'll ask some questions to help diagnose diabetes risk.")
    print("Please enter numerical values where applicable.\n")

    while True:
        patient = {}

        patient["Pregnancies"] = get_input("Number of pregnancies: ", int)
        patient["Glucose"] = get_input("Glucose level (mg/dL): ")
        patient["BloodPressure"] = get_input("Blood pressure (mm Hg): ")
        patient["SkinThickness"] = get_input("Skin thickness (mm): ")
        patient["Insulin"] = get_input("Insulin level (mu U/ml): ")
        patient["BMI"] = get_input("BMI (body mass index): ")
        patient["DiabetesPedigreeFunction"] = get_input("Diabetes pedigree function (0.0 - 2.5): ")
        patient["Age"] = get_input("Age: ", int)

        patient_series = pd.Series(patient)

        diagnosis = combined_predict(patient_series, model)

        if diagnosis == 1:
            print("\nMedBot Diagnosis: Based on the inputs, you are at risk of diabetes. Please consult a healthcare professional.\n")
        else:
            print("\nMedBot Diagnosis: Based on the inputs, you are unlikely to have diabetes.\n")

        cont = input("Would you like to diagnose another patient? (yes/no): ").lower()
        if cont != "yes":
            print("Thank you for using MedBot! Stay healthy!")
            break

if __name__ == "__main__":
    model = load_and_train_model()
    medical_chatbot(model)
