"""
CS 4375 - Assignment 2, Question 4
Naive Bayes Classifier from Scratch (no scikit-learn)
------------------------------------------------------
Dataset: Spam classification using two binary features:
  - Feature 1: Contains "win" (yes/no)
  - Feature 2: Contains "free" (yes/no)
"""

import numpy as np

# ─────────────────────────────────────────────
# STEP 1: Build the dataset
# ─────────────────────────────────────────────
# Each row: [win, free, label]  (1 = yes, 0 = no | 1 = Spam, 0 = Not Spam)
# We expand the count table into individual samples using np.repeat

data = np.array([
    [1, 1, 1],  # Spam,     win=yes, free=yes, count=40
    [1, 0, 1],  # Spam,     win=yes, free=no,  count=25
    [0, 1, 1],  # Spam,     win=no,  free=yes, count=30
    [0, 0, 1],  # Spam,     win=no,  free=no,  count=5
    [1, 1, 0],  # Not Spam, win=yes, free=yes, count=5
    [1, 0, 0],  # Not Spam, win=yes, free=no,  count=15
    [0, 1, 0],  # Not Spam, win=no,  free=yes, count=20
    [0, 0, 0],  # Not Spam, win=no,  free=no,  count=60
])
counts = [40, 25, 30, 5, 5, 15, 20, 60]

# Expand so each row is one email (total 200 emails)
X_full = np.repeat(data[:, :2], counts, axis=0)   # features: [win, free]
y_full = np.repeat(data[:, 2],  counts, axis=0)   # labels:   1=Spam, 0=Not Spam

print("=" * 55)
print("       CS 4375 - Q4: Naive Bayes Classifier")
print("=" * 55)
print(f"\nDataset size: {len(y_full)} emails")
print(f"  Spam:     {np.sum(y_full == 1)} emails")
print(f"  Not Spam: {np.sum(y_full == 0)} emails")


# ─────────────────────────────────────────────
# STEP 2: Train — learn all probabilities from data
# ─────────────────────────────────────────────
class NaiveBayesClassifier:
    """
    Discrete (Bernoulli) Naive Bayes from scratch.

    Core formula (from Prof. Iyer's slides):
        y* = argmax_y  P(y) * ∏ P(x_i | y)

    Parameters learned:
        priors:      P(y)        for each class
        likelihoods: P(x_i | y) for each feature and class
    """

    def fit(self, X, y):
        """Learn priors and likelihoods from training data."""
        self.classes_ = np.unique(y)
        self.class_names_ = {1: "Spam", 0: "Not Spam"}
        n_total = len(y)
        n_features = X.shape[1]

        # --- Priors: P(y) = Count(Y=y) / total ---
        self.priors_ = {}
        for c in self.classes_:
            self.priors_[c] = np.sum(y == c) / n_total

        # --- Likelihoods: P(x_i = 1 | y) = Count(x_i=1, Y=y) / Count(Y=y) ---
        # We store P(feature=1 | class) for each feature and each class.
        # (Since features are binary, P(feature=0|class) = 1 - P(feature=1|class))
        self.likelihoods_ = {}
        for c in self.classes_:
            X_c = X[y == c]          # subset: only emails of class c
            n_c = len(X_c)           # Count(Y=c)
            # For each feature, count how many times it's 1 within class c
            self.likelihoods_[c] = np.sum(X_c, axis=0) / n_c

        return self

    def predict_proba(self, X):
        """
        Compute posterior probabilities for each class.
        Returns a dict: {class: probability}
        """
        scores = {}
        for c in self.classes_:
            # Start with the prior (log space avoids underflow for many features)
            log_score = np.log(self.priors_[c])

            # Multiply in each likelihood  P(x_i | y)
            # x_i=1 → use likelihood directly
            # x_i=0 → use (1 - likelihood)  since P(x_i=0|y) = 1 - P(x_i=1|y)
            for i, x_val in enumerate(X):
                p = self.likelihoods_[c][i]
                log_score += np.log(p) if x_val == 1 else np.log(1 - p)

            scores[c] = np.exp(log_score)   # convert back from log

        # Normalize so probabilities sum to 1
        total = sum(scores.values())
        return {c: scores[c] / total for c in self.classes_}

    def predict(self, X):
        """Return the class with highest posterior probability."""
        proba = self.predict_proba(X)
        return max(proba, key=proba.get)


# ─────────────────────────────────────────────
# STEP 3: Fit the model
# ─────────────────────────────────────────────
model = NaiveBayesClassifier()
model.fit(X_full, y_full)

print("\n--- Learned Parameters ---")
print(f"\nPrior Probabilities (Part a):")
print(f"  P(Spam)     = {model.priors_[1]:.4f}")
print(f"  P(Not Spam) = {model.priors_[0]:.4f}")

feature_names = ["win=yes", "free=yes"]
print(f"\nLikelihood Table P(feature=yes | class):")
print(f"  {'Feature':<12} {'P(feat|Spam)':>14} {'P(feat|Not Spam)':>18}")
print(f"  {'-'*46}")
for i, fname in enumerate(feature_names):
    p_spam    = model.likelihoods_[1][i]
    p_notspam = model.likelihoods_[0][i]
    print(f"  {fname:<12} {p_spam:>14.4f} {p_notspam:>18.4f}")


# ─────────────────────────────────────────────
# STEP 4: Predict on the target email (win=yes, free=yes)
# ─────────────────────────────────────────────
test_email = np.array([1, 1])   # win=yes, free=yes

proba = model.predict_proba(test_email)
prediction = model.predict(test_email)

print(f"\n--- Part (b) & (c): Classify email [win=yes, free=yes] ---")
print(f"\n  Unnormalized scores (prior × likelihoods):")

for c in [1, 0]:
    prior = model.priors_[c]
    liks = [model.likelihoods_[c][i] if test_email[i] == 1
            else 1 - model.likelihoods_[c][i]
            for i in range(2)]
    raw = prior * np.prod(liks)
    name = model.class_names_[c]
    print(f"    {name:<10}: {prior:.2f} × {liks[0]:.2f} × {liks[1]:.2f} = {raw:.4f}")

print(f"\n  Posterior Probabilities (normalized):")
print(f"    P(Spam     | win=yes, free=yes) = {proba[1]:.4f}  ({proba[1]*100:.1f}%)")
print(f"    P(Not Spam | win=yes, free=yes) = {proba[0]:.4f}  ({proba[0]*100:.1f}%)")
print(f"\n  ✅ Predicted Label: {model.class_names_[prediction].upper()}")


# ─────────────────────────────────────────────
# STEP 5: Verify against manual calculation
# ─────────────────────────────────────────────
print("\n--- Verification Against Manual Calculation ---")
manual_spam    = 0.5 * 0.65 * 0.70
manual_notspam = 0.5 * 0.20 * 0.25
manual_total   = manual_spam + manual_notspam
manual_p_spam  = manual_spam / manual_total

print(f"  Manual P(Spam | win=yes, free=yes)     = {manual_p_spam:.4f}")
print(f"  Classifier P(Spam | win=yes, free=yes) = {proba[1]:.4f}")
match = np.isclose(manual_p_spam, proba[1], atol=1e-6)
print(f"  Match: {'✅ YES' if match else '❌ NO'}")


# ─────────────────────────────────────────────
# STEP 6: Check accuracy on full training set
# ─────────────────────────────────────────────
correct = sum(model.predict(X_full[i]) == y_full[i] for i in range(len(y_full)))
accuracy = correct / len(y_full)
print(f"\n--- Training Accuracy ---")
print(f"  Correct: {correct}/{len(y_full)}")
print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
print("\n" + "=" * 55)
