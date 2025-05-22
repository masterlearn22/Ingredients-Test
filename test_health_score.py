from recommendation_engine import RecommendationEngine

def test_health_scores():
    test_cases = [
        # Test Case 1: Sangat Tidak Sehat (High nutrients, Low min nutrients, Underweight BMI)
        {
            "Kalori": 2000,
            "Gula (g)": 65,
            "Karbohidrat (g)": 300,
            "Protein (g)": 10,
            "Lemak (g)": 29,
            "Serat (g)": 1,
            "Vitamin C (mg)": 20,
            "Berat Badan (kg)": 40,
            "Tinggi Badan (cm)": 200  # BMI = 40 / (2^2) = 10 (Underweight)
        },
        # Test Case 2: Tidak Sehat (Medium-High nutrients, Low-Medium min nutrients, Overweight BMI)
        {
            "Kalori": 500,
            "Gula (g)": 30,
            "Karbohidrat (g)": 80,
            "Protein (g)": 20,
            "Lemak (g)": 20,
            "Serat (g)": 4,
            "Vitamin C (mg)": 50,
            "Berat Badan (kg)": 100,
            "Tinggi Badan (cm)": 150  # BMI = 100 / (1.5^2) ≈ 44.4 (Overweight)
        },
        # Test Case 3: Sehat (Low-Medium nutrients, Sufficient min nutrients, Normal BMI)
        {
            "Kalori": 300,
            "Gula (g)": 15,
            "Karbohidrat (g)": 50,
            "Protein (g)": 25,
            "Lemak (g)": 15,
            "Serat (g)": 5,
            "Vitamin C (mg)": 60,
            "Berat Badan (kg)": 70,
            "Tinggi Badan (cm)": 170  # BMI = 70 / (1.7^2) ≈ 24.2 (Normal)
        },
        # Test Case 4: Cukup Sehat (Low nutrients, Sufficient-High min nutrients, Normal BMI)
        {
            "Kalori": 200,
            "Gula (g)": 5,
            "Karbohidrat (g)": 30,
            "Protein (g)": 40,
            "Lemak (g)": 10,
            "Serat (g)": 8,
            "Vitamin C (mg)": 90,
            "Berat Badan (kg)": 60,
            "Tinggi Badan (cm)": 175  # BMI = 60 / (1.75^2) ≈ 19.6 (Normal)
        },
        # Test Case 5: Sangat Sehat (Low nutrients, High min nutrients, Normal BMI)
        {
            "Kalori": 100,
            "Gula (g)": 5,
            "Karbohidrat (g)": 20,
            "Protein (g)": 45,
            "Lemak (g)": 5,
            "Serat (g)": 9,
            "Vitamin C (mg)": 95,
            "Berat Badan (kg)": 65,
            "Tinggi Badan (cm)": 180  # BMI = 65 / (1.8^2) ≈ 20.1 (Normal)
        }
    ]

    for i, prefs in enumerate(test_cases, 1):
        score = RecommendationEngine.calculate_health_score(prefs)
        category = RecommendationEngine.categorize_health(score)
        print(f"Test Case {i}:")
        print(f"Input: {prefs}")
        print(f"Score: {score:.2f}")
        print(f"Category: {category}")
        print("-" * 50)

if __name__ == "__main__":
    test_health_scores()