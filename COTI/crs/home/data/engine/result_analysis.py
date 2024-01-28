import json


with open("result_test.json", 'r') as f:
    data = json.load(f)

tp = 0
tn = 0
fp = 0
fn = 0

for item in data:
    for word in item['suggested_value']:
        if word in item['expected_value']:
            tp += 1
        else:
            fp += 1

    for word in item['expected_value']:
        if word not in item['suggested_value']:
            fn += 1

    tn += len(item['suggested_value']) + len(item['expected_value']) - tp - fp - fn

print(f"TP: {tp}")
print(f"TN: {tn}")
print(f"FP: {fp}")
print(f"FN: {fn}")

total = tp + tn + fp + fn

precision = tp / (tp + fp)
recall = tp / (tp + fn)
accuracy = (tp + tn) / total

print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"Accuracy: {accuracy:.3f}")