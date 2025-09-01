import numpy as np
from sklearn.metrics import roc_curve, auc, precision_recall_curve, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

# Generate dummy data
n_samples = 1000
true_labels = np.random.binomial(1, 0.5, n_samples)  # Balanced: ~500 negative (0), ~500 positive (1)
scores = np.zeros(n_samples)
predictions = np.zeros(n_samples)

# Simulate a high-performing model (~90% accuracy)
for i in range(n_samples):
    if true_labels[i] == 1:
        # Positive class: high probability of predicting positive
        scores[i] = np.random.beta(8, 2)  # Skew toward high probabilities (~0.8-1.0)
        predictions[i] = 1 if scores[i] > 0.5 else 0
    else:
        # Negative class: high probability of predicting negative
        scores[i] = np.random.beta(2, 8)  # Skew toward low probabilities (~0.0-0.2)
        predictions[i] = 1 if scores[i] > 0.5 else 0

# Debug: Check label and prediction distributions
print(f"True label distribution: Negative={np.sum(true_labels == 0)}, Positive={np.sum(true_labels == 1)}")
print(f"Prediction distribution: Negative={np.sum(predictions == 0)}, Positive={np.sum(predictions == 1)}")

# Create output directory for plots
output_dir = Path('results')
output_dir.mkdir(exist_ok=True)

# 1. Confusion Matrix
cm = confusion_matrix(true_labels, predictions, labels=[0, 1])
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.savefig(output_dir / 'confusion_matrix.png')
plt.close()

# 2. ROC Curve
fpr, tpr, _ = roc_curve(true_labels, scores)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='#ff7f0e', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='#1f77b4', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.savefig(output_dir / 'roc_curve.png')
plt.close()

# 3. Precision-Recall Curve
precision, recall, _ = precision_recall_curve(true_labels, scores)
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='#9467bd', lw=2, label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc='lower left')
plt.savefig(output_dir / 'precision_recall_curve.png')
plt.close()

# 4. Classification Report
report = classification_report(true_labels, predictions, target_names=['Negative', 'Positive'], output_dict=True, labels=[0, 1])
print("Classification Report:")
print(classification_report(true_labels, predictions, target_names=['Negative', 'Positive'], labels=[0, 1]))

# 5. Bar Plot for Precision, Recall, and F1 Score
metrics = {
    'Precision': [report['Negative']['precision'], report['Positive']['precision']],
    'Recall': [report['Negative']['recall'], report['Positive']['recall']],
    'F1-Score': [report['Negative']['f1-score'], report['Positive']['f1-score']]
}
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(2)
width = 0.25
ax.bar(x - width, metrics['Precision'], width, label='Precision', color='#4e79a7')  # Blue
ax.bar(x, metrics['Recall'], width, label='Recall', color='#59a14f')  # Green
ax.bar(x + width, metrics['F1-Score'], width, label='F1-Score', color='#e15759')  # Red
ax.set_xticks(x)
ax.set_xticklabels(['Negative', 'Positive'])
ax.set_ylabel('Score')
ax.set_title('Precision, Recall, and F1-Score by Class')
ax.legend()
plt.savefig(output_dir / 'metrics_bar_plot.png')
plt.close()

# 6. Prediction Distribution Plot
plt.figure(figsize=(8, 6))
sns.histplot(predictions, bins=2, color='#ff7f0e', stat='count')
plt.xticks([0, 1], ['Negative', 'Positive'])
plt.xlabel('Predicted Label')
plt.ylabel('Count')
plt.title('Prediction Distribution')
plt.savefig(output_dir / 'prediction_distribution.png')
plt.close()

# 7. Score Distribution Plot
plt.figure(figsize=(8, 6))
sns.histplot(scores, bins=50, color='#9467bd', stat='count')
plt.xlabel('Positive Class Probability')
plt.ylabel('Count')
plt.title('Score Distribution')
plt.savefig(output_dir / 'score_distribution.png')
plt.close()

print(f"Plots saved in {output_dir}")