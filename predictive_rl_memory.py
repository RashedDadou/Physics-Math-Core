# predictive_rl_memory.py

import math

class Predictive_RL_Memory:
    """
    مستودع الذاكرة الذكية (Predictive Neuro-Physics Layer)
    يتحكم في حفظ الأنماط الجوية والمائية وتطبيقها حفظياً دون إعادة الحسابات
    """
    def __init__(self):
        # قاموس الذاكرة الحركية لتخزين المتجهات الجاهزة
        self.memory_bank = {}
        # إحصائيات كفاءة المحرك لضمان الجودة
        self.total_lookups = 0
        self.memory_hits = 0

    def Generate_State_Signature(self, wind_speed_kmh, pressure_pascal, water_volume_m3):
        """تحويل الظروف البيئية المستمرة إلى بصمة رقمية مقاسة (Quantum Keys)"""
        # تقريب مرن للسرعة (كل 5 كم/س) والضغط (كل 500 باسكال) والحجم (كل 5 م³)
        snap_wind = int(round(wind_speed_kmh / 5.0) * 5)
        snap_pressure = int(round(pressure_pascal / 500.0) * 500)
        snap_water = int(round(water_volume_m3 / 5.0) * 5)
        
        return f"WIND_{snap_wind}__PRES_{snap_pressure}__WAT_{snap_water}"

    def Request_Simulation_Vectors(self, wind_speed_kmh, pressure_pascal, water_volume_m3):
        """
        بوابة العبور المركزية: فحص الذاكرة للتطبيق الحفظي السريع
        تعيد (True + المصفوفة الحركية) في حال الحفظ، أو (False) إذا كان النمط جديداً
        """
        self.total_lookups += 1
        signature = self.Generate_State_Signature(wind_speed_kmh, pressure_pascal, water_volume_m3)
        
        if signature in self.memory_bank:
            self.memory_hits += 1
            # استدعاء حفظي فوري وتجاوز تشغيل محركات الفيزياء
            return True, self.memory_bank[signature]
        
        # النمط غير مسجل، يتطلب تشغيل الحسابات الصارمة من المحركات الأصلية
        return False, signature

    def Commit_Calculated_Pattern(self, signature, force_vectors_output):
        """حقن وحفظ النمط الفيزيائي المحسوب حديثاً في الذاكرة لمنع تكراره مستقبلاً"""
        self.memory_bank[signature] = force_vectors_output

    def Get_Optimization_Report(self):
        """حساب نسبة التفوق وفرص توفير المعالجة اللحظية"""
        if self.total_lookups == 0:
            return 0.0
        # نسبة النجاح الحفظي
        efficiency_rate = (self.memory_hits / self.total_lookups) * 100.0
        return efficiency_rate


# ---------------------------------------------------------
# وحدة فحص وتشغيل ميكانيكية مستقلة لمحاكي الـ RL التنبؤي
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== فحص محرك الذاكرة العضلية والـ RL التنبؤي ===")
    
    rl_layer = Predictive_RL_Memory()
    
    # محاكاة الإطار الأول (Frame 1): رياح 122 كم/س، ضغط منخفض 99100 باسكال، حجم بركة 12 م³
    # المحرك يفحص الذاكرة
    is_memorized, result = rl_layer.Request_Simulation_Vectors(122.4, 99100.0, 12.2)
    print(f"\n[الإطار 1] فحص الذاكرة للنمط البيئي الأول:")
    
    if not is_memorized:
        print(f"-> النتيجة: النمط غير محفوظ. البصمة المتولدة: {result}")
        print("-> إجراء هندسي: تشغيل محرك الهواء والرياح والمياه لحساب القوى...")
        
        # فرضية مخرجات القوى المحسوبة بالنيوتن [Fx, Fy, Fz]
        calculated_forces = [340.5, 45.2, -12.8]
        
        # تخزينها في الـ RL
        rl_layer.Commit_Calculated_Pattern(result, calculated_forces)
        print("-> تم حفظ النمط بنجاح في الذاكرة العضلية للكون.")

    # محاكاة الإطار الثاني (Frame 2): تغير طفيف جداً في الأجواء (رياح 121 كم/س، ضغط 99200، ماء 11.8)
    # بفضل التقريب المرن، سيتطابق النمط مع البصمة المحفوظة تماماً!
    is_memorized_again, result_forces = rl_layer.Request_Simulation_Vectors(121.0, 99200.0, 11.8)
    print(f"\n[الإطار 2] فحص الذاكرة عند تغير الأجواء طفيفاً:")
    
    if is_memorized_again:
        print("-> النتيجة: تم العثور على النمط في الذاكرة العضلية (Memory Hit)!")
        print(f"-> القوى المحقونة حفظياً فوراً وبدون حسابات: {result_forces} نيوتن.")
        print("-> قفزة معالجة: تم توفير 100% من طاقة المعالج في هذا الإطار.")

    # تقرير الكفاءة الشامل
    efficiency = rl_layer.Get_Optimization_Report()
    print(f"\n=== تقرير كفاءة نظام الـ RL الحفظي: {efficiency:.1f}% توفير في الجهد الحسابي ===")
    print("======================================================")