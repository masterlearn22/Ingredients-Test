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
    def calculate_health_score(preferences):
        """
        Menghitung skor kesehatan menggunakan logika fuzzy dan metode Mamdani.
        """
        max_calories = preferences["Kalori Maksimum"]
        max_sugar = preferences["Gula Maksimum (g)"]
        max_carbs = preferences["Karbohidrat Maksimum (g)"]
        min_protein = preferences["Protein Minimum (g)"]
        max_fat = preferences["Lemak Maksimum (g)"]
        min_fiber = preferences["Serat Minimum (g)"]
        min_vitamin_c = preferences["Vitamin C Minimum (mg)"]

        calories_fuzzy = RecommendationEngine.fuzzify_value(max_calories, (0, 250), (250, 450), (450, 600))
        sugar_fuzzy = RecommendationEngine.fuzzify_value(max_sugar, (0, 10), (10, 25), (25, 50))
        carbs_fuzzy = RecommendationEngine.fuzzify_value(max_carbs, (0, 40), (40, 70), (70, 100))
        fat_fuzzy = RecommendationEngine.fuzzify_value(max_fat, (0, 10), (10, 25), (25, 50))

        protein_fuzzy = RecommendationEngine.fuzzify_min_value(min_protein, (0, 15), (15, 35), (35, 50))
        fiber_fuzzy = RecommendationEngine.fuzzify_min_value(min_fiber, (0, 3), (3, 7), (7, 10))
        vitamin_c_fuzzy = RecommendationEngine.fuzzify_min_value(min_vitamin_c, (0, 40), (40, 80), (80, 100))

        health_levels = {
            "Sangat Tidak Sehat": 0,
            "Tidak Sehat": 0,
            "Sehat": 0,
            "Cukup Sehat": 0,
            "Sangat Sehat": 0
        }

        weights = {
            "Sangat Tidak Sehat": 2.0,  # Further increased weight for extreme cases
            "Tidak Sehat": 1.0,
            "Sehat": 1.0,
            "Cukup Sehat": 1.2,
            "Sangat Sehat": 1.3
        }

        # Rule 1: Sangat Tidak Sehat (all max nutrients HIGH AND all min nutrients LOW)
        rule1 = min(max(calories_fuzzy[2], sugar_fuzzy[2], carbs_fuzzy[2], fat_fuzzy[2]),
                    max(protein_fuzzy[0], fiber_fuzzy[0], vitamin_c_fuzzy[0]))
        if (calories_fuzzy[2] == 1.0 and sugar_fuzzy[2] == 1.0 and carbs_fuzzy[2] == 1.0 and fat_fuzzy[2] == 1.0 and
            protein_fuzzy[0] == 1.0 and fiber_fuzzy[0] == 1.0 and vitamin_c_fuzzy[0] == 1.0):
            health_levels["Sangat Tidak Sehat"] = rule1 * weights["Sangat Tidak Sehat"]
            # If Rule 1 is fully triggered, override other rules
            health_levels["Tidak Sehat"] = 0
            health_levels["Sehat"] = 0
            health_levels["Cukup Sehat"] = 0
            health_levels["Sangat Sehat"] = 0
            numerator = health_levels["Sangat Tidak Sehat"] * 10
            denominator = health_levels["Sangat Tidak Sehat"]
            return numerator / denominator if denominator != 0 else 50

        # Rule 2: Tidak Sehat (medium to high max nutrients AND low to medium min nutrients)
        rule2 = min(max(calories_fuzzy[1], calories_fuzzy[2], sugar_fuzzy[1], sugar_fuzzy[2],
                        carbs_fuzzy[1], carbs_fuzzy[2], fat_fuzzy[1], fat_fuzzy[2]),
                    max(protein_fuzzy[0], protein_fuzzy[1], fiber_fuzzy[0], fiber_fuzzy[1], vitamin_c_fuzzy[0], vitamin_c_fuzzy[1]))
        health_levels["Tidak Sehat"] = max(health_levels["Tidak Sehat"], rule2 * weights["Tidak Sehat"])

        # Rule 3: Sehat (low to medium max nutrients AND sufficient min nutrients)
        rule3 = min(max(calories_fuzzy[0], calories_fuzzy[1], sugar_fuzzy[0], sugar_fuzzy[1],
                        carbs_fuzzy[0], carbs_fuzzy[1], fat_fuzzy[0], fat_fuzzy[1]),
                    max(protein_fuzzy[1], fiber_fuzzy[1], vitamin_c_fuzzy[1]))
        health_levels["Sehat"] = max(health_levels["Sehat"], rule3 * weights["Sehat"])

        # Rule 4: Cukup Sehat (low max nutrients AND sufficient to high min nutrients)
        rule4 = min(max(calories_fuzzy[0], sugar_fuzzy[0], carbs_fuzzy[0], fat_fuzzy[0]),
                    max(protein_fuzzy[1], protein_fuzzy[2], fiber_fuzzy[1], fiber_fuzzy[2], vitamin_c_fuzzy[1], vitamin_c_fuzzy[2]))
        health_levels["Cukup Sehat"] = max(health_levels["Cukup Sehat"], rule4 * weights["Cukup Sehat"])

        # Rule 5: Sangat Sehat (low max nutrients AND high min nutrients)
        rule5 = min(max(calories_fuzzy[0], sugar_fuzzy[0], carbs_fuzzy[0], fat_fuzzy[0]),
                    max(protein_fuzzy[2], fiber_fuzzy[2], vitamin_c_fuzzy[2]))
        health_levels["Sangat Sehat"] = max(health_levels["Sangat Sehat"], rule5 * weights["Sangat Sehat"])

        # Rule 6: Tidak Sehat (high sugar OR fat AND low protein OR fiber)
        rule6 = min(max(sugar_fuzzy[2], fat_fuzzy[2]),
                    max(protein_fuzzy[0], fiber_fuzzy[0]))
        health_levels["Tidak Sehat"] = max(health_levels["Tidak Sehat"], rule6 * weights["Tidak Sehat"])

        # Rule 7: Cukup Sehat (low calories AND high protein OR fiber)
        rule7 = min(calories_fuzzy[0],
                    max(protein_fuzzy[2], fiber_fuzzy[2]))
        health_levels["Cukup Sehat"] = max(health_levels["Cukup Sehat"], rule7 * weights["Cukup Sehat"])

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