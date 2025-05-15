class FoodData:
    def __init__(self):
        # Inisialisasi kelas tanpa data makanan
        self.health_levels = [
            "Sangat Tidak Sehat",
            "Tidak Sehat", 
            "Cukup Sehat", 
            "Sehat", 
            "Sangat Sehat"
        ]
        
        # Deskripsi untuk setiap tingkat kesehatan
        self.health_descriptions = {
            "Sangat Tidak Sehat": "Profil nutrisi membutuhkan perbaikan besar. Terlalu banyak kalori, gula, dan lemak, serta terlalu sedikit protein, serat, dan vitamin.",
            "Tidak Sehat": "Profil nutrisi membutuhkan perbaikan signifikan. Perlu mengurangi asupan gula dan lemak serta meningkatkan protein dan serat.",
            "Cukup Sehat": "Profil nutrisi cukup baik dengan beberapa area yang perlu ditingkatkan. Pertimbangkan untuk menyeimbangkan asupan nutrisi.",
            "Sehat": "Profil nutrisi seimbang dengan proporsi yang baik antara nutrisi makro dan mikro.",
            "Sangat Sehat": "Profil nutrisi sangat baik dengan keseimbangan optimal antara nutrisi. Rendah kalori, gula, dan lemak, serta tinggi protein, serat, dan vitamin."
        }
        
        # Rekomendasi umum untuk setiap tingkat kesehatan
        self.health_recommendations = {
            "Sangat Tidak Sehat": [
                "Kurangi asupan kalori secara signifikan",
                "Batasi gula dan lemak secara drastis",
                "Tingkatkan asupan protein, serat, dan vitamin secara substansial"
            ],
            "Tidak Sehat": [
                "Kurangi asupan gula dan lemak",
                "Tingkatkan asupan protein dan serat",
                "Perhatikan jumlah kalori harian"
            ],
            "Cukup Sehat": [
                "Pertahankan batasan kalori saat ini",
                "Sedikit tingkatkan asupan protein atau serat",
                "Pertimbangkan untuk mengurangi gula sedikit lagi"
            ],
            "Sehat": [
                "Pertahankan keseimbangan nutrisi saat ini",
                "Jaga konsistensi dalam pola makan",
                "Pastikan variasi sumber nutrisi"
            ],
            "Sangat Sehat": [
                "Pertahankan pola makan yang sangat baik ini",
                "Terus fokus pada protein dan serat tinggi",
                "Jaga asupan gula dan lemak tetap rendah"
            ]
        }
    
    def get_health_levels(self):
        """Mendapatkan daftar tingkat kesehatan"""
        return self.health_levels
    
    def get_health_description(self, level):
        """Mendapatkan deskripsi untuk tingkat kesehatan tertentu"""
        return self.health_descriptions.get(level, "")
    
    def get_health_recommendations(self, level):
        """Mendapatkan rekomendasi untuk tingkat kesehatan tertentu"""
        return self.health_recommendations.get(level, [])
    
    # Metode berikut dipertahankan untuk kompatibilitas dengan kode yang ada
    # tetapi tidak lagi menggunakan data makanan
    
    def add_food(self, name, nutritional_info):
        """Metode ini dipertahankan untuk kompatibilitas tetapi tidak melakukan apa-apa"""
        pass
    
    def update_food(self, name, nutritional_info):
        """Metode ini dipertahankan untuk kompatibilitas tetapi tidak melakukan apa-apa"""
        return False
    
    def delete_food(self, name):
        """Metode ini dipertahankan untuk kompatibilitas tetapi tidak melakukan apa-apa"""
        return False
    
    def get_food(self, name):
        """Metode ini dipertahankan untuk kompatibilitas tetapi tidak melakukan apa-apa"""
        return None
    
    def get_all_foods(self):
        """Metode ini dipertahankan untuk kompatibilitas tetapi mengembalikan dict kosong"""
        return {}
    
    def add_sample_foods(self):
        """Metode ini dipertahankan untuk kompatibilitas tetapi tidak melakukan apa-apa"""
        pass
