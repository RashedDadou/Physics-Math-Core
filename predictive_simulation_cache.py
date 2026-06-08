# predictive_simulation_cache.py

class Predictive_Simulation_Cache:
    """نظام الذاكرة الذكية لحفظ الأنماط الفيزيائية الجوية والمائية وتطبيقها حفظياً"""
    def __init__(self):
        # قاعدة بيانات الأنماط البيئية المحفوظة (الذاكرة الحركية)
        self.learned_environmental_states = {}

    def Generate_State_Signature(self, wind_speed, air_pressure, water_volume):
        """توليد بصمة رقمية فريدة للحالة الجوية الحالية لسهولة البحث عنها في الذاكرة"""
        # تقريب القيم لصناعة مفتاح بحث مرن (مثلاً: رياح 122 كم/س تقرب إلى 120 لربطها بالنمط المحفوظ)
        key_wind = round(wind_speed / 5.0) * 5
        key_pressure = round(air_pressure / 500.0) * 500
        key_water = round(water_volume / 10.0) * 10
        return f"W{key_wind}_P{key_pressure}_V{key_water}"

    def Lookup_Or_Calculate(self, wind_speed, air_pressure, water_volume):
        """البحث في الذاكرة: هل تعلمنا هذا الطقس سابقاً أم نحتاج لإعادة الحساب؟"""
        signature = self.Generate_State_Signature(wind_speed, air_pressure, water_volume)
        
        if signature in self.learned_environmental_states:
            # الحفظ الذكي: استدعاء مصفوفة القوى الجاهزة فوراً (بسرعة خاطفة)
            return "MEMORIZED_STATE", self.learned_environmental_states[signature]
        else:
            # لم يتعلمها بعد: يطلب من محركات الجو والرياح والمياه الحساب من الصفر
            return "NEED_CALCULATION", signature

    def Commit_State_To_Memory(self, signature, calculated_force_vectors):
        """تخزين القوى المحسوبة حديثاً في ذاكرة الـ RL ليتم استدعاؤها حفظياً في المرات القادمة"""
        self.learned_environmental_states[signature] = calculated_force_vectors