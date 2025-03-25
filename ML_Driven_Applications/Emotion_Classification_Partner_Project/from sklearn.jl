from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Define hyperparameter grid
C_values = [0.01, 0.1, 1, 10, 100]  # Regularization strengths

solvers = ['liblinear', 'saga']     # Solvers for Logistic Regression

# Initialize variables to store the best model and performance
best_model = None
best_accuracy = 0
best_params = None

# Iterate over all combinations of hyperparameters
for C in C_values:
    for solver in solvers:
        try:
            # Train Logistic Regression model with current hyperparameters
            logreg = LogisticRegression(C=C, solver=solver, max_iter=1000, random_state=42)
            logreg.fit(X_train_tfidf, y_train)
            
            # Evaluate on the validation set
            y_val_pred = logreg.predict(X_val_tfidf)
            val_accuracy = accuracy_score(y_val, y_val_pred)
            
            # Print current hyperparameter results
            print(f"C: {C}, Solver: {solver}, Validation Accuracy: {val_accuracy:.4f}")
            
            # Update best model if current one performs better
            if val_accuracy > best_accuracy:
                best_accuracy = val_accuracy
                best_model = logreg
                best_params = {'C': C, 'solver': solver}
        except Exception as e:
            # Handle potential exceptions (e.g., incompatible solver with data)
            print(f"Error with C: {C}, Solver: {solver} - {e}")

# Output the best hyperparameters and validation accuracy
print(f"\nBest Parameters: {best_params}")
print(f"Best Validation Accuracy: {best_accuracy:.4f}")

# Use the best model to make predictions on the validation set
y_val_pred_best = best_model.predict(X_val_tfidf)

# Calculate validation accuracy
val_accuracy = accuracy_score(y_val, y_val_pred_best)

# Print validation accuracy
print(f"Validation Accuracy with Best Model: {val_accuracy:.4f}")

# Evaluate the final model
from sklearn.metrics import classification_report

print("\nClassification Report with Best Model:")
print(classification_report(y_val, y_val_pred_best, target_names=[str(i) for i in range(28)]))

# Generate predictions for the test set
test_predictions = best_model.predict(X_test_tfidf)

# # Save predictions to a CSV file
# output = pd.DataFrame({"id": test["id"], "label": test_predictions})
# output.to_csv("submission_tuned.csv", index=False)
# print("Submission file saved as submission_tuned.csv")
