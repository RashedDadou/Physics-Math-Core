# hydrological_volume_engine.py

class WaterMaterialProperties:
    """تحديد الخصائص الفيزيائية والكثافة لنوع الماء"""
    def __init__(self, water_type="salt_water"):
        self.water_type = water_type
        # الكثافة القياسية (كجم/متر مكعب) بناءً على نوع الماء
        if water_type == "fresh_water":
            self.density = 1000.0  # مياه الأمطار والأنهار
        else:
            self.density = 1025.0  # مياه البحار والمحيطات (الافتراضية للمشهد)


class Hydrological_Volume_Engine:
    """محرك رياضيات المياه: يحسب أوزان وكتل المياه داخل كادر المشهد المصمم فقط"""
    def __init__(self, water_properties):
        self.props = water_properties

    def Calculate_Raindrop_Mass(self, radius_mm=1.5):
        """
        1. حساب كتلة قطرة المطر الواحدة بالميليغرام
        معادلة حجم الكرة: V = (4/3) * pi * r^3
        """
        radius_meters = float(radius_mm) / 1000.0  # تحويل المليمتر إلى متر
        volume_m3 = (4.0 / 3.0) * 3.141592653589793 * (radius_meters ** 3)
        
        # الكتلة بالكيلوغرام = الحجم × الكثافة (مياه عذبة للأمطار)
        mass_kg = volume_m3 * 1000.0 
        mass_mg = mass_kg * 1e6  # تحويل إلى ميليغرام
        
        return mass_kg, mass_mg

    def Calculate_Puddle_Mass(self, length, width, avg_depth):
        """
        2. حساب كتلة بركة ماء مستقرة على الشاطئ (بالكيلوغرام)
        الحجم = الطول × العرض × متوسط العمق
        """
        volume_m3 = float(length) * float(width) * float(avg_depth)
        mass_kg = volume_m3 * self.props.density
        return mass_kg, volume_m3

    def Calculate_Viewport_Sea_Mass(self, camera_view_width, visible_shore_length, max_depth_limit):
        """
        3. حساب كتلة مياه البحر المتواجدة داخل كادر التوليد البصري (المحيط الافتراضي للمشهد)
        تُحسب بناءً على المساحة الرؤيوية الفعالة للكاميرا وعمق المياه المتدرج.
        """
        # نعتبر أن قاع البحر يتدرج في العمق (شكل إسفيني/مثلثي من الشاطئ إلى الداخل)
        # الحجم الافتراضي للمنشور = الطول × العرض × (أقصى عمق / 2)
        volume_m3 = float(camera_view_width) * float(visible_shore_length) * (float(max_depth_limit) / 2.0)
        mass_kg = volume_m3 * self.props.density
        mass_tonnes = mass_kg / 1000.0  # تحويل إلى طن متري للكميات الكبيرة
        
        return mass_kg, mass_tonnes, volume_m3


# ---------------------------------------------------------
# وحدة فحص وتشغيل ميكانيكية مستقلة لمحرك أوزان المياه
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== فحص محرك رياضيات أوزان المياه داخل كادر المشهد ===")
    
    # 1. تهيئة خصائص المياه (مياه بحر مالحة لشاطئ الفتاة)
    sea_water = WaterMaterialProperties(water_type="salt_water")
    fresh_water = WaterMaterialProperties(water_type="fresh_water")
    
    hydro_engine = Hydrological_Volume_Engine(sea_water)
    rain_engine = Hydrological_Volume_Engine(fresh_water)
    
    print("\n[المستوى الأول: قطرات المطر الساقطة في المشهد]")
    r_kg, r_mg = rain_engine.Calculate_Raindrop_Mass(radius_mm=2.0)
    print(f"• قطرة مطر بنصف قطر 2 ملم -> كتلتها الصافية: {r_mg:.2f} ميليغرام ({r_kg:.6f} كجم)")

    print("\n[المستوى الثاني: بركة مياه مالحة على رمل الشاطئ]")
    p_kg, p_vol = hydro_engine.Calculate_Puddle_Mass(length=3.0, width=1.5, avg_depth=0.1)
    print(f"• بركة أبعادها (3م × 1.5م) وعمق 10 سم -> حجمها: {p_vol:.2f} م³ | كتلتها: {p_kg:.2f} كجم")

    print("\n[المستوى الثالث: كتلة مياه البحر الافتراضية داخل كادر الكاميرا]")
    # فرضية مشهد الفتاة: الكاميرا ترى عرض 30 متر، وعمق الرؤية لداخل البحر 20 متر، وأقصى عمق مائي في الكادر 3 أمتار
    s_kg, s_tons, s_vol = hydro_engine.Calculate_Viewport_Sea_Mass(
        camera_view_width=30.0, visible_shore_length=20.0, max_depth_limit=3.0
    )
    print(f"• المساحة المائية المنظورة للكاميرا تشغل حجماً قدره: {s_vol:.2f} م³")
    print(f"• الكتلة الرياضية الصافية لماء البحر المواجه للكاميرا: {s_kg:.2f} كجم (أي حوالي {s_tons:.2f} طن!)")
    print("\n-> ملاحظة هندسية: المحرك نجح في حصر أوزان المياه من الميليغرام إلى الأطنان "
          "بناءً على حدود الكادر المصمم دون الغرق في حسابات المحيط الكامل.")
    print("======================================================")