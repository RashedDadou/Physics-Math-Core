# sovereign_gravity_engine.py

class RigidBodyState:
    """الحاوية الهندسية لتخزين بيانات وموقع أي شكل أو مجسم في الفراغ"""
    def __init__(self, x=0.0, y=0.0, z=0.0, vx=0.0, vy=0.0, vz=0.0):
        # الموقع الحالي في الفراغ ثلاثي الأبعاد
        self.position = [float(x), float(y), float(z)]
        # السرعة المتجهة الحالية (يمكن استقبال سرعات ابتدائية من محركات الكائنات كـ الركض أو القفز)
        self.velocity = [float(vx), float(vy), float(vz)]
        # التسارع الميكانيكي النقي
        self.acceleration = [0.0, 0.0, 0.0]
        # مستشعر حالة الارتطام بالارضية الافتراضية للكون
        self.is_grounded = False


class Sovereign_Gravity_Controller:
    """محرك الرياضيات المركزي للجاذبية الأرضية الموحدة (الطبقة الصفرية)"""
    def __init__(self, gravity_constant=9.81, world_floor_y=0.0):
        # الثابت الكوني لعجلة الجاذبية
        self.g = float(gravity_constant)
        # مستوى أرضية العالم (الصفر الجغرافي الذي تتوقف عنده الجاذبية)
        self.floor_y = float(world_floor_y)

    def Apply_Gravity_Field(self, body):
        """تطبيق تسارع الجاذبية الموحد لأسفل على أي مادة أو مجسم طالما لم يلمس الأرض"""
        if body.is_grounded:
            body.acceleration = [0.0, 0.0, 0.0]
            return

        body.acceleration[0] = 0.0
        body.acceleration[1] = -self.g  # سحب صارم نحو مركز الأرض
        body.acceleration[2] = 0.0

    def Integrate_Motion_State(self, body, delta_time):
        """تحديث السرعة والموقع بناءً على التسارع الموحد في الفراغ النقي"""
        if body.is_grounded:
            return

        # 1. تحديث السرعة المتجهة: V = V + (A * dt)
        body.velocity[0] += body.acceleration[0] * delta_time
        body.velocity[1] += body.acceleration[1] * delta_time
        body.velocity[2] += body.acceleration[2] * delta_time

        # 2. تحديث الموقع في الفراغ: P = P + (V * dt)
        body.position[0] += body.velocity[0] * delta_time
        body.position[1] += body.velocity[1] * delta_time
        body.position[2] += body.velocity[2] * delta_time

        # 3. صمام الأمان: مستشعر الارتطام بأرضية العالم
        if body.position[1] <= self.floor_y:
            body.position[1] = self.floor_y  # تثبيت الجسم على الأرض بدقة
            body.velocity = [0.0, 0.0, 0.0]  # تصفير طاقة الحركة الصفرية
            body.acceleration = [0.0, 0.0, 0.0]
            body.is_grounded = True


class Pure_Sovereign_Pull_Engine:
    """محرك السحب النقي المباشر (طريقة بديلة للتحديث اللحظي المباشر للسرعة)"""
    def __init__(self, pull_constant=9.81, world_floor_y=0.0):
        self.g = float(pull_constant)
        self.floor_y = float(world_floor_y)

    def Apply_Sovereign_Pull(self, body, delta_time):
        """تحديث سرعة السحب والموقع مباشرة للمحور العمودي"""
        if body.position[1] <= self.floor_y:
            body.position[1] = self.floor_y
            body.velocity = [0.0, 0.0, 0.0]
            return

        # السحب الموحد يؤثر على السرعة العمودية مباشرة
        body.velocity[1] -= self.g * delta_time

        # تحديث الإحداثيات
        body.position[0] += body.velocity[0] * delta_time
        body.position[1] += body.velocity[1] * delta_time
        body.position[2] += body.velocity[2] * delta_time
        
        if body.position[1] <= self.floor_y:
            body.position[1] = self.floor_y
            body.velocity = [0.0, 0.0, 0.0]


# ---------------------------------------------------------
# محاكاة لإثبات سحب مجسمين مختلفين تماماً (حجر ساكن ضد مقاتل يقفز)
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== فحص شمولية محرك الجاذبية الموحد لأي مادة ومجسم ===")
    
    gravity_core = Sovereign_Gravity_Controller(gravity_constant=9.81, world_floor_y=0.0)
    dt = 0.1
    
    # المجسم 1: حجر ساكن تماماً يسقط من ارتفاع 5 أمتار
    stone = RigidBodyState(x=0.0, y=5.0, z=0.0)
    
    # المجسم 2: مقاتل يركض بسرعة 4 م/ث أفقياً وقفز للأعلى بسرعة ابتدائية 10 م/ث من الأرض
    fighter = RigidBodyState(x=0.0, y=0.0, z=0.0, vx=4.0, vy=10.0, vz=0.0)
    
    print("\n--- محاكاة حركة المجسمين في نفس حقل الجاذبية الموحد ---")
    for frame in range(1, 6):
        # تطبيق نفس الحقل على الاثنين بالتساوي
        gravity_core.Apply_Gravity_Field(stone)
        gravity_core.Apply_Gravity_Field(fighter)
        
        # مكاملة الحركة
        gravity_core.Integrate_Motion_State(stone, dt)
        gravity_core.Integrate_Motion_State(fighter, dt)
        
        print(f"الإطار {frame} | الحجر: الموقع Y={stone.position[1]:.2f} م، السرعة Vy={stone.velocity[1]:.2f} م/ث")
        print(f"         | المقاتل: الموقع [X={fighter.position[0]:.2f}, Y={fighter.position[1]:.2f}] م، السرعة Vy={fighter.velocity[1]:.2f} م/ث")
        print("-" * 75)