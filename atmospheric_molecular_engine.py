# atmospheric_molecular_engine.py

class AtmosphericStateContainer:
    """الحاوية الهندسية لتخزين الحالة الفيزيائية الحالية للغلاف الجوي في مشهد معين"""
    def __init__(self, temperature_celsius=15.0, pressure_pascal=101325.0):
        # درجة الحرارة السائدة في البيئة (بالدرجة المئوية)
        self.temperature_k = float(temperature_celsius) + 273.15  # تحويل إلى كلفن للعمليات الرياضية
        # الضغط الجوي عند مستوى سطح البحر (بالمقاييس العالمية باسكال)
        self.pressure = float(pressure_pascal)
        # الثابت العالمي للغازات (جول / مول.كلفن)
        self.R_constant = 8.31446
        # الكتلة المولية للهواء الجاف المحيط بنا (كجم/مول)
        self.molar_mass_air = 0.02897 
        # عدد أفوغادرو لحساب الجزيئات بدقة (جزيء/مول)
        self.avogadro_number = 6.02214e23


class Atmospheric_Molecular_Engine:
    """محرك رياضيات الجو: يحسب الكثافة والكتلة الجزيئية للهواء في حجم معين"""
    def __init__(self, atmospheric_state):
        self.env = atmospheric_state

    def Calculate_Air_Density(self):
        """حساب كثافة الهواء الحالية (كجم/م³) بناءً على الضغط والحرارة: Rho = (P * M) / (R * T)"""
        density = (self.env.pressure * self.env.molar_mass_air) / (self.env.R_constant * self.env.temperature_k)
        return float(density)

    def Calculate_Air_Mass_In_Volume(self, volume_cubic_meters):
        """حساب كتلة الهواء الصافية المتواجدة داخل حجم الفراغ الذي يشغله المجسم"""
        air_density = self.Calculate_Air_Density()
        # الكتلة = الكثافة × الحجم
        total_air_mass = air_density * float(volume_cubic_meters)
        return float(total_air_mass)

    def Calculate_Molecular_Count_In_Volume(self, volume_cubic_meters):
        """حساب العدد الفعلي المطلق لجزيئات الهواء التي سيصطدم بها المجسم داخل هذا الحجم"""
        # 1. حساب عدد المولات: n = (P * V) / (R * T)
        moles = (self.env.pressure * float(volume_cubic_meters)) / (self.env.R_constant * self.env.temperature_k)
        # 2. عدد الجزيئات = عدد المولات × عدد أفوغادرو
        total_molecules = moles * self.env.avogadro_number
        return float(total_molecules)

    def Calculate_Dynamic_Molecular_Resistance(self, body_volume, body_velocity_vector):
        """
        حساب قوة مقاومة كتلة الهواء الموجهة (بالنيوتن).
        تأخذ حجم المجسم وسرعته المتجهة الحالية، وتحسب الفرملة الناتجة عن إزاحة جزيئات الهواء.
        """
        air_density = self.Calculate_Air_Density()
        
        # فك مصفوفة السرعة الحالية القادمة من الجسم
        v_x = float(body_velocity_vector[0])
        v_y = float(body_velocity_vector[1])
        v_z = float(body_velocity_vector[2])
        
        # معامل افتراضي لشكل الجسم في الهواء (سيتم تخصيصه بدقة في محركات الأجسام لاحقاً)
        drag_coefficient = 0.47  # القيمة المعيارية لشكل الكرة أو المجسمات العادية
        
        # حساب المساحة السطحية التقريبية المواجهة بناءً على حجم الجسم (فرضية هندسية للمجسم)
        # المساحة المؤثرة = الجذر التكعيبي للحجم مربع (تقريب هندسي لعزل كود الجو عن تفاصيل المجسم)
        approx_frontal_area = (float(body_volume) ** (2.0 / 3.0)) * 0.6
        
        # حساب قوة المقاومة لكل محور على حدة بعكس اتجاه الحركة تماماً (فرملة الجزيئات)
        f_res_x = -0.5 * air_density * approx_frontal_area * drag_coefficient * (v_x * abs(v_x))
        f_res_y = -0.5 * air_density * approx_frontal_area * drag_coefficient * (v_y * abs(v_y))
        f_res_z = -0.5 * air_density * approx_frontal_area * drag_coefficient * (v_z * abs(v_z))
        
        return [f_res_x, f_res_y, f_res_z]


# ---------------------------------------------------------
# وحدة فحص هندسية مستقلة لمحرك رياضيات الهواء
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== فحص محرك رياضيات الهواء والكتلة الجزيئية المستقل ===")
    
    # 1. تهيئة أجواء طبيعية (15 درجة مئوية، ضغط جوي قياسي)
    normal_weather = AtmosphericStateContainer(temperature_celsius=15.0, pressure_pascal=101325.0)
    air_engine = Atmospheric_Molecular_Engine(normal_weather)
    
    # فرضية: لدينا حيز أو مجسم حجمه 2 متر مكعب (مثلاً حجم إزاحة مقاتل أو صخرة ضخمة)
    target_volume = 2.0 
    
    density_result = air_engine.Calculate_Air_Density()
    mass_result = air_engine.Calculate_Air_Mass_In_Volume(target_volume)
    molecules_count = air_engine.Calculate_Molecular_Count_In_Volume(target_volume)
    
    print(f"• كثافة الهواء المحسوبة في البيئة: {density_result:.4f} كجم/م³")
    print(f"• كتلة جزيئات الهواء الصافية المتواجدة في حجم {target_volume} م³ هي: {mass_result:.4f} كجم")
    print(f"• العدد المطلق لجزيئات الهواء داخل هذا الحجم: {molecules_count:.2e} جزيء")
    
    # محاكاة حركة مجسم يتحرك بسرعة أفقية وعمودية [Vx=5, Vy=-10, Vz=0] داخل هذا الجو
    test_velocity = [5.0, -10.0, 0.0]
    resistance_forces = air_engine.Calculate_Dynamic_Molecular_Resistance(target_volume, test_velocity)
    
    print("\n--- تأثير جزيئات الهواء (مصفوفة القوى المتجهة بالنيوتن) ---")
    print(f"-> المقاومة الأفقية المحور X (فرملة الركض): {resistance_forces[0]:.2f} نيوتن")
    print(f"-> المقاومة العمودية المحور Y (مقاومة الهبوط لأعلى): {resistance_forces[1]:.2f} نيوتن")
    print("========================================================")