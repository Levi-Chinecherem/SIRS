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

# Simulate current system (~90% accuracy)
current_scores = np.zeros(n_samples)
current_predictions = np.zeros(n_samples)
for i in range(n_samples):
    if true_labels[i] == 1:
        current_scores[i] = np.random.beta(8, 2)  # High probabilities for positive (~0.8-1.0)
        current_predictions[i] = 1 if current_scores[i] > 0.5 else 0
    else:
        current_scores[i] = np.random.beta(2, 8)  # Low probabilities for negative (~0.0-0.2)
        current_predictions[i] = 1 if current_scores[i] > 0.5 else 0

# Simulate old system (~80% accuracy)
old_scores = np.zeros(n_samples)
old_predictions = np.zeros(n_samples)
for i in range(n_samples):
    if true_labels[i] == 1:
        old_scores[i] = np.random.beta(6, 4)  # Less confident probabilities (~0.6-1.0)
        old_predictions[i] = 1 if old_scores[i] > 0.5 else 0
    else:
        old_scores[i] = np.random.beta(4, 6)  # Less confident probabilities (~0.0-0.4)
        old_predictions[i] = 1 if old_scores[i] > 0.5 else 0

# Debug: Check label and prediction distributions
print(f"True label distribution: Negative={np.sum(true_labels == 0)}, Positive={np.sum(true_labels == 1)}")
print(f"Current system prediction distribution: Negative={np.sum(current_predictions == 0)}, Positive={np.sum(current_predictions == 1)}")
print(f"Old system prediction distribution: Negative={np.sum(old_predictions == 0)}, Positive={np.sum(old_predictions == 1)}")

# Create output directory for plots
output_dir = Path('results')
output_dir.mkdir(exist_ok=True)

# 1. Confusion Matrix - Current System
cm_current = confusion_matrix(true_labels, current_predictions, labels=[0, 1])
plt.figure(figsize=(8, 6))
sns.heatmap(cm_current, annot=True, fmt='d', cmap='Blues', xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.title('Confusion Matrix - Current System')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.savefig(output_dir / 'current_confusion_matrix.png')
plt.close()

# 1. Confusion Matrix - Old System
cm_old = confusion_matrix(true_labels, old_predictions, labels=[0, 1])
plt.figure(figsize=(8, 6))
sns.heatmap(cm_old, annot=True, fmt='d', cmap='Oranges', xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.title('Confusion Matrix - Old System')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.savefig(output_dir / 'old_confusion_matrix.png')
plt.close()

# 2. ROC Curve - Comparison
fpr_current, tpr_current, _ = roc_curve(true_labels, current_scores)
roc_auc_current = auc(fpr_current, tpr_current)
fpr_old, tpr_old, _ = roc_curve(true_labels, old_scores)
roc_auc_old = auc(fpr_old, tpr_old)
plt.figure(figsize=(8, 6))
plt.plot(fpr_current, tpr_current, color='#4e79a7', lw=2, label=f'Current System (AUC = {roc_auc_current:.2f})')
plt.plot(fpr_old, tpr_old, color='#f28e2b', lw=2, label=f'Old System (AUC = {roc_auc_old:.2f})')
plt.plot([0, 1], [0, 1], color='#1f77b4', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison')
plt.legend(loc='lower right')
plt.savefig(output_dir / 'roc_curve_comparison.png')
plt.close()

# 3. Precision-Recall Curve - Comparison
precision_current, recall_current, _ = precision_recall_curve(true_labels, current_scores)
precision_old, recall_old, _ = precision_recall_curve(true_labels, old_scores)
plt.figure(figsize=(8, 6))
plt.plot(recall_current, precision_current, color='#4e79a7', lw=2, label='Current System')
plt.plot(recall_old, precision_old, color='#f28e2b', lw=2, label='Old System')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve Comparison')
plt.legend(loc='lower left')
plt.savefig(output_dir / 'precision_recall_curve_comparison.png')
plt.close()

# 4. Classification Report
report_current = classification_report(true_labels, current_predictions, target_names=['Negative', 'Positive'], output_dict=True, labels=[0, 1])
report_old = classification_report(true_labels, old_predictions, target_names=['Negative', 'Positive'], output_dict=True, labels=[0, 1])
print("Classification Report - Current System:")
print(classification_report(true_labels, current_predictions, target_names=['Negative', 'Positive'], labels=[0, 1]))
print("Classification Report - Old System:")
print(classification_report(true_labels, old_predictions, target_names=['Negative', 'Positive'], labels=[0, 1]))

# 5. Bar Plot for Precision, Recall, and F1 Score - Comparison
metrics_current = {
    'Precision': [report_current['Negative']['precision'], report_current['Positive']['precision']],
    'Recall': [report_current['Negative']['recall'], report_current['Positive']['recall']],
    'F1-Score': [report_current['Negative']['f1-score'], report_current['Positive']['f1-score']]
}
metrics_old = {
    'Precision': [report_old['Negative']['precision'], report_old['Positive']['precision']],
    'Recall': [report_old['Negative']['recall'], report_old['Positive']['recall']],
    'F1-Score': [report_old['Negative']['f1-score'], report_old['Positive']['f1-score']]
}
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(2)
width = 0.2
ax.bar(x - width*1.5, metrics_current['Precision'], width, label='Current Precision', color='#4e79a7')
ax.bar(x - width*0.5, metrics_current['Recall'], width, label='Current Recall', color='#59a14f')
ax.bar(x + width*0.5, metrics_current['F1-Score'], width, label='Current F1-Score', color='#e15759')
ax.bar(x + width*1.5, metrics_old['Precision'], width, label='Old Precision', color='#f28e2b')
ax.bar(x + width*2.5, metrics_old['Recall'], width, label='Old Recall', color='#ff9f9a')
ax.bar(x + width*3.5, metrics_old['F1-Score'], width, label='Old F1-Score', color='#f7b6d2')
ax.set_xticks(x)
ax.set_xticklabels(['Negative', 'Positive'])
ax.set_ylabel('Score')
ax.set_title('Precision, Recall, and F1-Score Comparison')
ax.legend()
plt.savefig(output_dir / 'metrics_bar_plot_comparison.png')
plt.close()

# 6. Prediction Distribution - Current System
plt.figure(figsize=(8, 6))
sns.histplot(current_predictions, bins=2, color='#4e79a7', stat='count')
plt.xticks([0, 1], ['Negative', 'Positive'])
plt.xlabel('Predicted Label')
plt.ylabel('Count')
plt.title('Prediction Distribution - Current System')
plt.savefig(output_dir / 'current_prediction_distribution.png')
plt.close()

# 6. Prediction Distribution - Old System
plt.figure(figsize=(8, 6))
sns.histplot(old_predictions, bins=2, color='#f28e2b', stat='count')
plt.xticks([0, 1], ['Negative', 'Positive'])
plt.xlabel('Predicted Label')
plt.ylabel('Count')
plt.title('Prediction Distribution - Old System')
plt.savefig(output_dir / 'old_prediction_distribution.png')
plt.close()

# 7. Score Distribution - Comparison
plt.figure(figsize=(8, 6))
sns.histplot(current_scores, bins=50, color='#4e79a7', label='Current System', stat='count', alpha=0.5)
sns.histplot(old_scores, bins=50, color='#f28e2b', label='Old System', stat='count', alpha=0.5)
plt.xlabel('Positive Class Probability')
plt.ylabel('Count')
plt.title('Score Distribution Comparison')
plt.legend()
plt.savefig(output_dir / 'score_distribution_comparison.png')
plt.close()

print(f"Plots saved in {output_dir}")