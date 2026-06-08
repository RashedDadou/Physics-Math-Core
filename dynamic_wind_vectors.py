# dynamic_wind_vectors.py

import math

class Dynamic_Wind_Vectors:
    """محرك رياح متطور يعتمد على طبقتين متدرجتين لتوليد متجهات السرعة للهواء"""
    
    def __init__(self):
        # تحويل الحدود التي حددتها أنت إلى متر/ثانية (القسمة على 3.6)
        self.MIN_NORMAL_WIND = 20.0 / 3.6   # ~ 5.55 م/ث
        self.MAX_NORMAL_WIND = 120.0 / 3.6  # ~ 33.33 م/ث
        
        self.MIN_CYCLONE_WIND = 400.0 / 3.6 # ~ 111.11 م/ث
        self.MAX_CYCLONE_WIND = 500.0 / 3.6 # ~ 138.88 م/ث

    def Get_Standard_Wind_Vector(self, severity_factor=0.5, direction_angles=[45.0, 0.0]):
        """
        الطبقة الأولى: الرياح العادية والعواصف (20 إلى 120 كم/ساعة)
        severity_factor: عامل الشدة من 0 (أهدأ ريح 20 كم/س) إلى 1 (أعنف عاصفة 120 كم/س)
        direction_angles: زوايا اتجاه الرياح [الأفقية، العمودية] بالدرجات
        """
        # حصر العامل بين 0 و 1 لسلامة الحسابات
        severity_factor = max(0.0, min(1.0, float(severity_factor)))
        
        # حساب السرعة الصافية بالتدرج ضمن النطاق الأول
        wind_speed = self.MIN_NORMAL_WIND + (self.MAX_NORMAL_WIND - self.MIN_NORMAL_WIND) * severity_factor
        
        # تحويل الزوايا إلى راديان وتوليد مصفوفة السرعة ثلاثية الأبعاد [Wx, Wy, Wz]
        rad_horizontal = math.radians(direction_angles[0])
        w_x = wind_speed * math.cos(rad_horizontal)
        w_y = 0.0  # الرياح العادية تكون أفقية موازية للأرض غالباً
        w_z = wind_speed * math.sin(rad_horizontal)
        
        return [w_x, w_y, w_z], wind_speed * 3.6

    def Get_Destructive_Cyclone_Vector(self, core_x, core_z, object_x, object_z, severity_factor=0.5):
        """
        الطبقة الثانية: الأعاصير المدمرة والمنخفضات الحادة (400 إلى 500 كم/ساعة)
        تتميز بحركة دورانية لولبية (Vortex) حول مركز المنخفض الجوي الحاد.
        """
        severity_factor = max(0.0, min(1.0, float(severity_factor)))
        
        # حساب السرعة الصافية بالتدرج ضمن النطاق الإعصاري المرعب
        cyclone_speed = self.MIN_CYCLONE_WIND + (self.MAX_CYCLONE_WIND - self.MIN_CYCLONE_WIND) * severity_factor
        
        # حساب المتجه من مركز الإعصار إلى المجسم
        dx = object_x - core_x
        dz = object_z - core_z
        distance = math.sqrt(dx**2 + dz**2)
        
        if distance == 0:
            return [0.0, 0.0, 0.0], 0.0
        
        # المتجهات المماسية الدائرية (صناعة الدوران اللولبي للإعصار)
        tangent_x = -dz / distance
        tangent_z = dx / distance
        
        # حساب سرعة الرياح المتجهة ثلاثية الأبعاد (مع فتح السقف برمجياً)
        w_x = tangent_x * cyclone_speed
        w_z = tangent_z * cyclone_speed
        
        # في الأعاصير المدمرة، هناك سحب عمودي للأعلى بفعل المنخفض الجوي الحاد
        w_y = cyclone_speed * 0.2  # الرياح ترفع الأشياء للأعلى بنسبة 20% من قوتها الأفقية
        
        return [w_x, w_y, w_z], cyclone_speed * 3.6


# ---------------------------------------------------------
# وحدة فحص وتشغيل ميكانيكية مستقلة لطبقتي الرياح
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== فحص محرك سرعة الرياح ذو الطبقتين المتدرجتين ===")
    
    wind_engine = Dynamic_Wind_Vectors()
    
    # 1. فحص الطبقة الأولى: عاصفة قوية بنسبة 80% من النطاق الأول
    normal_vector, normal_kmh = wind_engine.Get_Standard_Wind_Vector(severity_factor=0.8, direction_angles=[90.0, 0.0])
    print(f"\n[الطبقة الأولى: العواصف]")
    print(f"• سرعة الرياح المحسوبة: {normal_kmh:.2f} كم/ساعة")
    print(f"• مصفوفة المتجهات الصافية [Wx, Wy, Wz]: [{normal_vector[0]:.2f}, {normal_vector[1]:.2f}, {normal_vector[2]:.2f}] م/ث")
    
    # 2. فحص الطبقة الثانية: إعصار مدمر مركزه [0,0] والمجسم يتواجد عند [100, 0]
    cyclone_vector, cyclone_kmh = wind_engine.Get_Destructive_Cyclone_Vector(
        core_x=0.0, core_z=0.0, object_x=100.0, object_z=0.0, severity_factor=0.5
    )
    print(f"\n[الطبقة الثانية: الأعاصير المدمرة]")
    print(f"• سرعة الإعصار في هذه النقطة: {cyclone_kmh:.2f} كم/ساعة")
    print(f"• مصفوفة العصف الدوراني والصعودي المحسوبة: "
          f"[Wx={cyclone_vector[0]:.2f}, Wy={cyclone_vector[1]:.2f}, Wz={cyclone_vector[2]:.2f}] م/ث")
    print("====================================================")