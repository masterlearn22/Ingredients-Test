class RecommendationEngine:
    @staticmethod
    def fuzzify_value(value, low_range, medium_range, high_range):
        """
        Memfuzzifikasi nilai tunggal menjadi derajat keanggotaan Rendah, Sedang, Tinggi.
        low_range, medium_range, high_range adalah tuple yang mendefinisikan rentang untuk setiap himpunan fuzzy.
        """
        low = 0
        medium = 0
        high = 0

        if value <= low_range[1]:
            low = 1
        elif low_range[1] < value < medium_range[0]:
            low = (medium_range[0] - value) / (medium_range[0] - low_range[1])

        if medium_range[0] <= value <= medium_range[1]:
            medium = 1
        elif low_range[1] < value < medium_range[0]:
            medium = (value - low_range[1]) / (medium_range[0] - low_range[1])
        elif medium_range[1] < value < high_range[0]:
            medium = (high_range[0] - value) / (high_range[0] - medium_range[1])

        if value >= high_range[0]:
            high = 1
        elif medium_range[1] < value < high_range[0]:
            high = (value - medium_range[1]) / (high_range[0] - medium_range[1])

        return low, medium, high

    @staticmethod
    def fuzzify_min_value(value, low_range, sufficient_range, high_range):
        """
        Memfuzzifikasi nilai tunggal menjadi derajat keanggotaan Rendah, Cukup, Tinggi untuk persyaratan minimum.
        """
        low = 0
        sufficient = 0
        high = 0

        if value <= low_range[1]:
            low = 1
        elif low_range[1] < value < sufficient_range[0]:
            low = (sufficient_range[0] - value) / (sufficient_range[0] - low_range[1])

        if sufficient_range[0] <= value <= sufficient_range[1]:
            sufficient = 1
        elif low_range[1] < value < sufficient_range[0]:
            sufficient = (value - low_range[1]) / (sufficient_range[0] - low_range[1])
        elif sufficient_range[1] < value < high_range[0]:
            sufficient = (high_range[0] - value) / (high_range[0] - sufficient_range[1])

        if value >= high_range[0]:
            high = 1
        elif sufficient_range[1] < value < high_range[0]:
            high = (value - sufficient_range[1]) / (high_range[0] - sufficient_range[1])

        return low, sufficient, high

    @staticmethod
    def fuzzify_bmi(bmi):
        """
        Memfuzzifikasi nilai BMI menjadi derajat keanggotaan Underweight, Normal, Overweight.
        Rentang berdasarkan WHO: Underweight < 18.5, Normal 18.5-24.9, Overweight >= 25.
        Adjusted for new range (0-100 kg, 0-200 cm).
        """
        underweight = 0
        normal = 0
        overweight = 0

        # Underweight (<18.5)
        if bmi <= 16:
            underweight = 1
        elif 16 < bmi < 18.5:
            underweight = (18.5 - bmi) / (18.5 - 16)

        # Normal (18.5-24.9)
        if 18.5 <= bmi <= 24.9:
            normal = 1
        elif 16 < bmi < 18.5:
            normal = (bmi - 16) / (18.5 - 16)
        elif 24.9 < bmi < 27:
            normal = (27 - bmi) / (27 - 24.9)

        # Overweight (>=25)
        if bmi >= 27:
            overweight = 1
        elif 24.9 < bmi < 27:
            overweight = (bmi - 24.9) / (27 - 24.9)

        return underweight, normal, overweight

    @staticmethod
    def calculate_health_score(preferences):
        """
        Menghitung skor kesehatan menggunakan logika fuzzy dan metode Mamdani, dengan tambahan BMI.
        """
        calories = preferences["Kalori"]
        sugar = preferences["Gula (g)"]
        carbs = preferences["Karbohidrat (g)"]
        protein = preferences["Protein (g)"]
        fat = preferences["Lemak (g)"]
        fiber = preferences["Serat (g)"]
        vitamin_c = preferences["Vitamin C (mg)"]
        weight = preferences["Berat Badan (kg)"]
        height = preferences["Tinggi Badan (cm)"]

        # Hitung BMI
        if height > 0:  # Hindari pembagian oleh nol
            height_m = height / 100  # Konversi cm ke meter
            bmi = weight / (height_m ** 2)
        else:
            bmi = 0  # Default jika tinggi nol

        # Fuzzifikasi
        calories_fuzzy = RecommendationEngine.fuzzify_value(calories, (0, 250), (250, 450), (450, 2000))
        sugar_fuzzy = RecommendationEngine.fuzzify_value(sugar, (0, 10), (10, 25), (25, 65))
        carbs_fuzzy = RecommendationEngine.fuzzify_value(carbs, (0, 40), (40, 70), (70, 300))
        fat_fuzzy = RecommendationEngine.fuzzify_value(fat, (0, 10), (10, 25), (25, 29))
        protein_fuzzy = RecommendationEngine.fuzzify_min_value(protein, (0, 15), (15, 35), (35, 50))
        fiber_fuzzy = RecommendationEngine.fuzzify_min_value(fiber, (0, 3), (3, 7), (7, 10))
        vitamin_c_fuzzy = RecommendationEngine.fuzzify_min_value(vitamin_c, (0, 40), (40, 80), (80, 100))
        bmi_fuzzy = RecommendationEngine.fuzzify_bmi(bmi)

        health_levels = {
            "Sangat Tidak Sehat": 0,
            "Tidak Sehat": 0,
            "Sehat": 0,
            "Cukup Sehat": 0,
            "Sangat Sehat": 0
        }

        weights = {
            "Sangat Tidak Sehat": 2.0,
            "Tidak Sehat": 1.0,
            "Sehat": 1.0,
            "Cukup Sehat": 1.2,
            "Sangat Sehat": 1.3
        }

        # Rule 1: Sangat Tidak Sehat (all nutrients HIGH AND all min nutrients LOW AND BMI Underweight/Overweight)
        rule1 = min(
            max(calories_fuzzy[2], sugar_fuzzy[2], carbs_fuzzy[2], fat_fuzzy[2]),
            max(protein_fuzzy[0], fiber_fuzzy[0], vitamin_c_fuzzy[0]),
            max(bmi_fuzzy[0], bmi_fuzzy[2])
        )
        if (calories_fuzzy[2] == 1.0 and sugar_fuzzy[2] == 1.0 and carbs_fuzzy[2] == 1.0 and fat_fuzzy[2] == 1.0 and
            protein_fuzzy[0] == 1.0 and fiber_fuzzy[0] == 1.0 and vitamin_c_fuzzy[0] == 1.0 and
            (bmi_fuzzy[0] == 1.0 or bmi_fuzzy[2] == 1.0)):
            health_levels["Sangat Tidak Sehat"] = rule1 * weights["Sangat Tidak Sehat"]
            health_levels["Tidak Sehat"] = 0
            health_levels["Sehat"] = 0
            health_levels["Cukup Sehat"] = 0
            health_levels["Sangat Sehat"] = 0
            numerator = health_levels["Sangat Tidak Sehat"] * 10
            denominator = health_levels["Sangat Tidak Sehat"]
            return numerator / denominator if denominator != 0 else 50

        # Rule 2: Tidak Sehat (medium to high nutrients AND low to medium min nutrients AND BMI Underweight/Overweight)
        rule2 = min(
            max(calories_fuzzy[1], calories_fuzzy[2], sugar_fuzzy[1], sugar_fuzzy[2],
                carbs_fuzzy[1], carbs_fuzzy[2], fat_fuzzy[1], fat_fuzzy[2]),
            max(protein_fuzzy[0], protein_fuzzy[1], fiber_fuzzy[0], fiber_fuzzy[1], vitamin_c_fuzzy[0], vitamin_c_fuzzy[1]),
            max(bmi_fuzzy[0], bmi_fuzzy[2])
        )
        health_levels["Tidak Sehat"] = max(health_levels["Tidak Sehat"], rule2 * weights["Tidak Sehat"])

        # Rule 3: Sehat (low to medium nutrients AND sufficient min nutrients AND BMI Normal)
        rule3 = min(
            max(calories_fuzzy[0], calories_fuzzy[1], sugar_fuzzy[0], sugar_fuzzy[1],
                carbs_fuzzy[0], carbs_fuzzy[1], fat_fuzzy[0], fat_fuzzy[1]),
            max(protein_fuzzy[1], fiber_fuzzy[1], vitamin_c_fuzzy[1]),
            bmi_fuzzy[1]
        )
        health_levels["Sehat"] = max(health_levels["Sehat"], rule3 * weights["Sehat"])

        # Rule 4: Cukup Sehat (low nutrients AND sufficient to high min nutrients AND BMI Normal)
        rule4 = min(
            max(calories_fuzzy[0], sugar_fuzzy[0], carbs_fuzzy[0], fat_fuzzy[0]),
            max(protein_fuzzy[1], protein_fuzzy[2], fiber_fuzzy[1], fiber_fuzzy[2], vitamin_c_fuzzy[1], vitamin_c_fuzzy[2]),
            bmi_fuzzy[1]
        )
        health_levels["Cukup Sehat"] = max(health_levels["Cukup Sehat"], rule4 * weights["Cukup Sehat"])

        # Rule 5: Sangat Sehat (low nutrients AND high min nutrients AND BMI Normal)
        rule5 = min(
            max(calories_fuzzy[0], sugar_fuzzy[0], carbs_fuzzy[0], fat_fuzzy[0]),
            max(protein_fuzzy[2], fiber_fuzzy[2], vitamin_c_fuzzy[2]),
            bmi_fuzzy[1]
        )
        health_levels["Sangat Sehat"] = max(health_levels["Sangat Sehat"], rule5 * weights["Sangat Sehat"])

        # Rule 6: Tidak Sehat (high sugar OR fat AND low protein OR fiber AND BMI Underweight/Overweight)
        rule6 = min(
            max(sugar_fuzzy[2], fat_fuzzy[2]),
            max(protein_fuzzy[0], fiber_fuzzy[0]),
            max(bmi_fuzzy[0], bmi_fuzzy[2])
        )
        health_levels["Tidak Sehat"] = max(health_levels["Tidak Sehat"], rule6 * weights["Tidak Sehat"])

        # Rule 7: Cukup Sehat (low calories AND high protein OR fiber AND BMI Normal)
        rule7 = min(
            calories_fuzzy[0],
            max(protein_fuzzy[2], fiber_fuzzy[2]),
            bmi_fuzzy[1]
        )
        health_levels["Cukup Sehat"] = max(health_levels["Cukup Sehat"], rule7 * weights["Cukup Sehat"])

        # Defuzzifikasi
        crisp_values = {
            "Sangat Tidak Sehat": 10,
            "Tidak Sehat": 30,
            "Sehat": 50,
            "Cukup Sehat": 70,
            "Sangat Sehat": 90
        }

        numerator = sum(membership * crisp_values[level] for level, membership in health_levels.items())
        denominator = sum(health_levels.values())
        if denominator == 0:
            return 50
        score = numerator / denominator
        return score

    @staticmethod
    def categorize_health(score):
        if score >= 80:
            return "Sangat Sehat"
        elif score >= 60:
            return "Cukup Sehat"
        elif score >= 40:
            return "Sehat"
        elif score >= 20:
            return "Tidak Sehat"
        else:
            return "Sangat Tidak Sehat"