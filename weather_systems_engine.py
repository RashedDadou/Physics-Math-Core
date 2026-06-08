# weather_systems_engine.py

import math

class WeatherSystemZone:
    """
    الحاوية الهندسية لتحديد منطقة النظام الجوي (مرتفع أو منخفض) في الفراغ.
    تعتمد على مركز جغرافي ونطاق تأثير (نصف قطر).
    """
    def __init__(self, center_x, center_z, radius_meters, core_pressure_pascal):
        # المركز الجغرافي للنظام الجوي على الخريطة (X, Z)
        self.center_x = float(center_x)
        self.center_z = float(center_z)
        # نصف قطر منطقة تأثير المنخفض أو المرتفع
        self.radius = float(radius_meters)
        # الضغط في قلب أو مركز النظام الجوي (بالباسكال)
        # المنخفض الجوي يكون أقل من 101325 باسكال | المرتفع يكون أعلى
        self.core_pressure = float(core_pressure_pascal)

    def Calculate_Local_Pressure(self, object_x, object_z, standard_pressure=101325.0):
        """
        حساب الضغط الجوي الديناميكي عند موقع المجسم الحالي [X, Z].
        كلما اقترب المجسم من المركز، تأثر بضغط قلب النظام الجوي.
        """
        # حساب المسافة الأفقية بين المجسم ومركز النظام الجوي (نظرية فيثاغورس 2D)
        distance = math.sqrt((object_x - self.center_x)**2 + (object_z - self.center_z)**2)
        
        # إذا كان المجسم خارج نطاق تأثير المرتفع/المنخفض، يعود للضغط القياسي
        if distance >= self.radius:
            return standard_pressure
        
        # معامل القرب من المركز (1 عند المركز تماماً، و 0 عند أطراف النطاق)
        proximity_factor = 1.0 - (distance / self.radius)
        
        # تدرج الضغط: يتغير الضغط انسيابياً من الضغط القياسي إلى ضغط قلب النظام
        local_pressure = standard_pressure + (self.core_pressure - standard_pressure) * proximity_factor
        return local_pressure


class Low_Pressure_System(WeatherSystemZone):
    """محرك المنخفض الجوي: يتميز بضغط منخفض في المركز يسبب جذب الهواء وصعوده"""
    def __init__(self, center_x, center_z, radius_meters, core_pressure_pascal=99000.0):
        # القيمة الافتراضية لقلب المنخفض الجوي أقل من الضغط القياسي (مثلاً 99000 باسكال)
        super().__init__(center_x, center_z, radius_meters, core_pressure_pascal)
        self.system_type = "Low Pressure (Cyclone)"


class High_Pressure_System(WeatherSystemZone):
    """محرك المرتفع الجوي: يتميز بضغط مرتفع في المركز يسبب استقرار الهواء وهبوطه"""
    def __init__(self, center_x, center_z, radius_meters, core_pressure_pascal=103500.0):
        # القيمة الافتراضية لقلب المرتفع الجوي أعلى من الضغط القياسي (مثلاً 103500 باسكال)
        super().__init__(center_x, center_z, radius_meters, core_pressure_pascal)
        self.system_type = "High Pressure (Anticyclone)"


# ---------------------------------------------------------
# وحدة فحص هندسية مستقلة لنظام الطقس قبل ربطه بمحرك الهواء
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== فحص محرك أنظمة الطقس المستقل (مرتفع / منخفض) ===")
    
    # فرضية: لدينا منطقة منخفض جوي (عاصفة أو تقلب جوي) مركزها عند النقطة [X=100, Z=100] ونطاقها 500 متر
    storm_zone = Low_Pressure_System(center_x=100.0, center_z=100.0, radius_meters=500.0)
    
    # مجسم (مقاتل أو حجر) يتواجد قريباً جداً من مركز العاصفة عند [X=120, Z=110]
    object_x, object_z = 120.0, 110.0
    
    standard_p = 101325.0
    dynamic_p = storm_zone.Calculate_Local_Pressure(object_x, object_z, standard_p)
    
    print(f"• نوع النظام الجوي المتواجد في المنطقة: {storm_zone.system_type}")
    print(f"• الضغط الجوي المعياري القياسي: {standard_p} باسكال")
    print(f"• الضغط الجوي الديناميكي المحسوب عند موقع المجسم: {dynamic_p:.2f} باسكال")
    print(f"-> ملاحظة هندسية: الضغط انخفض بفعل اقتراب الجسم من قلب المنخفض الجوي، "
          f"هذه القيمة الممررة لمحرك الهواء ستجعل كتلة الهواء هناك أقل كثافة وأخف!")
    print("======================================================")