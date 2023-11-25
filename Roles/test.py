from sklearn.metrics import classification_report
y_true = [0, 1, 2, 4, 5]
y_pred = [0, 1, 2, 4, 5]
target_names = ['class 0', 'class 1', 'class 2']
print(classification_report(y_true, y_pred))
print(classification_report(y_true, y_pred, target_names=target_names))
