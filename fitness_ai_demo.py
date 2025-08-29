# Health & Fitness AI Agent Coach - نسخة تجريبية
# مدرب ذكي للصحة واللياقة البدنية

import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# إعدادات API
OPENAI_API_KEY = "demo-mode"  # للتجربة بدون API

class FitnessLevel(Enum):
    BEGINNER = "مبتدئ"
    INTERMEDIATE = "متوسط"
    ADVANCED = "متقدم"

class WorkoutType(Enum):
    CARDIO = "كارديو"
    STRENGTH = "قوة"
    FLEXIBILITY = "مرونة"
    HIIT = "تدريب متقطع عالي الكثافة"

@dataclass
class UserProfile:
    """ملف المستخدم الشخصي"""
    name: str
    age: int
    weight: float  # بالكيلوغرام
    height: float  # بالسنتيمتر
    fitness_level: FitnessLevel
    goals: List[str]
    health_conditions: List[str]
    preferred_workouts: List[WorkoutType]
    available_time: int  # دقائق يومياً
    
    def calculate_bmi(self) -> float:
        """حساب مؤشر كتلة الجسم"""
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)
    
    def get_bmi_category(self) -> str:
        """تصنيف مؤشر كتلة الجسم"""
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "نقص الوزن"
        elif bmi < 25:
            return "وزن طبيعي"
        elif bmi < 30:
            return "زيادة الوزن"
        else:
            return "سمنة"

@dataclass
class WorkoutSession:
    """جلسة تمرين"""
    date: datetime.date
    type: WorkoutType
    duration: int  # بالدقائق
    exercises: List[Dict]
    calories_burned: int
    intensity: str  # خفيف، متوسط، عالي
    notes: str = ""

class HealthDataAnalyzer:
    """أداة تحليل البيانات الصحية"""
    
    def analyze_user_data(self, user_data: Dict) -> Dict:
        """تحليل بيانات المستخدم"""
        try:
            # تحويل البيانات إلى ملف مستخدم
            profile = UserProfile(
                name=user_data["name"],
                age=user_data["age"],
                weight=user_data["weight"],
                height=user_data["height"],
                fitness_level=FitnessLevel(user_data["fitness_level"]),
                goals=user_data["goals"],
                health_conditions=user_data.get("health_conditions", []),
                preferred_workouts=[WorkoutType(w) for w in user_data.get("preferred_workouts", [])],
                available_time=user_data.get("available_time", 30)
            )
            
            bmi = profile.calculate_bmi()
            bmi_category = profile.get_bmi_category()
            
            # تحليل مستوى اللياقة
            recommendations = []
            
            if bmi < 18.5:
                recommendations.append("زيادة السعرات الحرارية وتمارين القوة لبناء العضلات")
            elif bmi > 25:
                recommendations.append("تقليل السعرات الحرارية وزيادة تمارين الكارديو")
            else:
                recommendations.append("الحفاظ على النمط الصحي الحالي")
            
            # تحليل الأهداف
            goal_analysis = self._analyze_goals(profile.goals, profile.fitness_level)
            
            analysis = {
                "user_info": {
                    "name": profile.name,
                    "age": profile.age,
                    "bmi": bmi,
                    "bmi_category": bmi_category
                },
                "fitness_assessment": self._assess_fitness_level(profile),
                "recommendations": recommendations,
                "goal_analysis": goal_analysis,
                "weekly_schedule_suggestion": self._suggest_weekly_schedule(profile)
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"خطأ في تحليل البيانات: {str(e)}"}
    
    def _assess_fitness_level(self, profile: UserProfile) -> str:
        """تقييم مستوى اللياقة"""
        assessments = []
        
        # تقييم بناء على العمر والـ BMI
        bmi = profile.calculate_bmi()
        
        if profile.age < 30 and 18.5 <= bmi <= 24.9:
            assessments.append("حالة صحية ممتازة للعمر")
        elif profile.age >= 50:
            assessments.append("يُنصح بالتركيز على تمارين المرونة والتوازن")
        else:
            assessments.append("حالة صحية جيدة مع إمكانية التحسن")
            
        return " | ".join(assessments) if assessments else "تقييم عام جيد"
    
    def _analyze_goals(self, goals: List[str], fitness_level: FitnessLevel) -> Dict:
        """تحليل أهداف المستخدم"""
        goal_mapping = {
            "فقدان الوزن": {
                "priority": "عالية",
                "recommended_workouts": ["كارديو", "HIIT"],
                "duration": "30-45 دقيقة يومياً"
            },
            "بناء العضلات": {
                "priority": "عالية",
                "recommended_workouts": ["قوة", "مقاومة"],
                "duration": "45-60 دقيقة 4-5 مرات أسبوعياً"
            },
            "تحسين اللياقة": {
                "priority": "متوسطة",
                "recommended_workouts": ["كارديو", "قوة", "مرونة"],
                "duration": "30 دقيقة يومياً"
            }
        }
        
        analysis = {}
        for goal in goals:
            if goal in goal_mapping:
                analysis[goal] = goal_mapping[goal]
            else:
                analysis[goal] = {
                    "priority": "متوسطة",
                    "recommended_workouts": ["متنوع"],
                    "duration": "30 دقيقة يومياً"
                }
                
        return analysis
    
    def _suggest_weekly_schedule(self, profile: UserProfile) -> Dict:
        """اقتراح جدول أسبوعي"""
        if profile.available_time < 30:
            return {
                "frequency": "3-4 أيام أسبوعياً",
                "session_duration": "20-25 دقيقة",
                "focus": "تمارين عالية الكثافة قصيرة المدى"
            }
        elif profile.available_time < 60:
            return {
                "frequency": "4-5 أيام أسبوعياً", 
                "session_duration": "30-45 دقيقة",
                "focus": "توازن بين الكارديو والقوة"
            }
        else:
            return {
                "frequency": "5-6 أيام أسبوعياً",
                "session_duration": "45-60 دقيقة",
                "focus": "برنامج شامل متنوع"
            }

class WorkoutPlanner:
    """أداة تخطيط التمارين"""
    
    def create_workout_plan(self, requirements: Dict) -> Dict:
        """إنشاء خطة تمرين"""
        try:
            fitness_level = requirements.get("fitness_level", "BEGINNER")
            workout_type = requirements.get("workout_type", "CARDIO")
            duration = int(requirements.get("duration", 30))
            goals = requirements.get("goals", [])
            
            workout_plan = self._create_detailed_plan(
                fitness_level, workout_type, duration, goals
            )
            
            return workout_plan
            
        except Exception as e:
            return {"error": f"خطأ في إنشاء خطة التمرين: {str(e)}"}
    
    def _create_detailed_plan(self, fitness_level: str, workout_type: str, 
                           duration: int, goals: List[str]) -> Dict:
        """إنشاء خطة تمرين مفصلة"""
        
        exercises_db = {
            "CARDIO": {
                "BEGINNER": [
                    {"name": "المشي السريع", "duration": 10, "intensity": "خفيف"},
                    {"name": "صعود الدرج", "duration": 5, "intensity": "متوسط"},
                    {"name": "تمارين الإحماء", "duration": 5, "intensity": "خفيف"}
                ],
                "INTERMEDIATE": [
                    {"name": "الجري الخفيف", "duration": 15, "intensity": "متوسط"},
                    {"name": "نط الحبل", "duration": 10, "intensity": "عالي"},
                    {"name": "تمارين الأيروبيك", "duration": 15, "intensity": "متوسط"}
                ],
                "ADVANCED": [
                    {"name": "الجري السريع", "duration": 20, "intensity": "عالي"},
                    {"name": "تدريب متقطع", "duration": 15, "intensity": "عالي جداً"},
                    {"name": "تمارين بيربي", "duration": 10, "intensity": "عالي"}
                ]
            },
            "STRENGTH": {
                "BEGINNER": [
                    {"name": "تمرين الضغط (معدل)", "reps": "3x8", "intensity": "خفيف"},
                    {"name": "القرفصاء", "reps": "3x10", "intensity": "متوسط"},
                    {"name": "تمرين البلانك", "duration": "30 ثانية x3", "intensity": "متوسط"}
                ],
                "INTERMEDIATE": [
                    {"name": "تمرين الضغط", "reps": "3x12", "intensity": "متوسط"},
                    {"name": "القرفصاء مع الأثقال", "reps": "4x10", "intensity": "عالي"},
                    {"name": "تمرين العقلة", "reps": "3x5", "intensity": "عالي"}
                ],
                "ADVANCED": [
                    {"name": "تمرين الضغط المتفجر", "reps": "4x8", "intensity": "عالي"},
                    {"name": "الديدليفت", "reps": "4x6", "intensity": "عالي جداً"},
                    {"name": "تمارين الأوزان المركبة", "reps": "5x5", "intensity": "عالي جداً"}
                ]
            }
        }
        
        # اختيار التمارين المناسبة
        selected_exercises = exercises_db.get(workout_type, {}).get(fitness_level, [])
        
        workout_plan = {
            "session_info": {
                "type": workout_type,
                "level": fitness_level,
                "total_duration": duration,
                "estimated_calories": self._estimate_calories(workout_type, duration, fitness_level)
            },
            "warm_up": {
                "duration": 5,
                "exercises": ["تحريك المفاصل", "تمارين إطالة خفيفة"]
            },
            "main_workout": {
                "exercises": selected_exercises,
                "rest_between_sets": "30-60 ثانية"
            },
            "cool_down": {
                "duration": 5,
                "exercises": ["تمارين الإطالة", "تمارين التنفس العميق"]
            },
            "tips": self._get_workout_tips(workout_type, fitness_level)
        }
        
        return workout_plan
    
    def _estimate_calories(self, workout_type: str, duration: int, fitness_level: str) -> int:
        """تقدير السعرات المحروقة"""
        base_calories_per_minute = {
            "CARDIO": {"BEGINNER": 8, "INTERMEDIATE": 12, "ADVANCED": 15},
            "STRENGTH": {"BEGINNER": 6, "INTERMEDIATE": 8, "ADVANCED": 10},
            "HIIT": {"BEGINNER": 12, "INTERMEDIATE": 15, "ADVANCED": 18}
        }
        
        rate = base_calories_per_minute.get(workout_type, {}).get(fitness_level, 8)
        return duration * rate
    
    def _get_workout_tips(self, workout_type: str, fitness_level: str) -> List[str]:
        """نصائح للتمرين"""
        general_tips = [
            "اشرب الماء قبل وأثناء وبعد التمرين",
            "استمع لجسمك ولا تتجاهل الألم",
            "احرص على النوم الكافي للاستشفاء"
        ]
        
        specific_tips = {
            "CARDIO": ["ابدأ بوتيرة معتدلة وزد تدريجياً", "احرص على التنفس المنتظم"],
            "STRENGTH": ["ركز على الشكل الصحيح أكثر من الوزن", "دع العضلات تستريح 48 ساعة بين الجلسات"]
        }
        
        return general_tips + specific_tips.get(workout_type, [])

class ProgressTracker:
    """أداة تتبع التقدم"""
    
    def analyze_progress(self, progress_data: Dict) -> Dict:
        """تحليل بيانات التقدم"""
        try:
            current_weight = progress_data.get("current_weight")
            initial_weight = progress_data.get("initial_weight")
            workouts_completed = progress_data.get("workouts_completed", 0)
            days_active = progress_data.get("days_active", 0)
            
            analysis = self._analyze_detailed_progress(
                current_weight, initial_weight, workouts_completed, days_active
            )
            
            return analysis
            
        except Exception as e:
            return {"error": f"خطأ في تتبع التقدم: {str(e)}"}
    
    def _analyze_detailed_progress(self, current_weight: float, initial_weight: float,
                         workouts_completed: int, days_active: int) -> Dict:
        """تحليل التقدم المحرز"""
        
        weight_change = initial_weight - current_weight if initial_weight else 0
        weight_change_percent = (weight_change / initial_weight * 100) if initial_weight else 0
        
        # تقييم الالتزام
        commitment_score = min(100, (workouts_completed / max(days_active, 1)) * 100)
        
        # رسائل تحفيزية
        motivational_messages = []
        
        if weight_change > 0:
            motivational_messages.append(f"ممتاز! فقدت {weight_change:.1f} كيلو")
        elif weight_change < -1:
            motivational_messages.append("زيادة طفيفة في الوزن - قد تكون عضلات!")
        else:
            motivational_messages.append("استمر في المحافظة على وزنك")
            
        if commitment_score >= 80:
            motivational_messages.append("التزام ممتاز! استمر على هذا المنوال")
        elif commitment_score >= 60:
            motivational_messages.append("التزام جيد، يمكنك تحسينه أكثر")
        else:
            motivational_messages.append("حاول زيادة عدد أيام التمرين")
        
        return {
            "weight_progress": {
                "initial_weight": initial_weight,
                "current_weight": current_weight,
                "change": weight_change,
                "change_percent": round(weight_change_percent, 1)
            },
            "activity_stats": {
                "workouts_completed": workouts_completed,
                "days_active": days_active,
                "commitment_score": round(commitment_score, 1)
            },
            "motivational_messages": motivational_messages,
            "next_goals": self._suggest_next_goals(commitment_score, weight_change)
        }
    
    def _suggest_next_goals(self, commitment_score: float, weight_change: float) -> List[str]:
        """اقتراح أهداف جديدة"""
        suggestions = []
        
        if commitment_score < 70:
            suggestions.append("هدف: تمرين 4 أيام في الأسبوع القادم")
        
        if abs(weight_change) < 0.5:
            suggestions.append("هدف: تغيير نمط التمرين لكسر الثبات")
            
        suggestions.append("هدف: قياس محيط الخصر والعضلات")
        suggestions.append("هدف: تحسين مرونة الجسم")
        
        return suggestions[:3]  # أعلى 3 اقتراحات

class FitnessAIAgent:
    """الوكيل الذكي الرئيسي للياقة البدنية - نسخة تجريبية"""
    
    def __init__(self):
        """تهيئة الوكيل الذكي"""
        
        # إعداد الأدوات
        self.health_analyzer = HealthDataAnalyzer()
        self.workout_planner = WorkoutPlanner()
        self.progress_tracker = ProgressTracker()
        
        # قاعدة بيانات المستخدمين
        self.user_profiles = {}
        self.workout_history = {}
        
        print("🏋️ مرحباً بك في المدرب الذكي للياقة البدنية!")
        print("🤖 أنا مدربك الشخصي الذكي وسأساعدك في تحقيق أهدافك الصحية")
        print("-" * 60)
    
    def register_user(self, user_data: Dict) -> str:
        """تسجيل مستخدم جديد"""
        try:
            user_profile = UserProfile(
                name=user_data["name"],
                age=user_data["age"],
                weight=user_data["weight"],
                height=user_data["height"],
                fitness_level=FitnessLevel(user_data["fitness_level"]),
                goals=user_data["goals"],
                health_conditions=user_data.get("health_conditions", []),
                preferred_workouts=[WorkoutType(w) for w in user_data.get("preferred_workouts", [])],
                available_time=user_data.get("available_time", 30)
            )
            
            self.user_profiles[user_profile.name] = user_profile
            self.workout_history[user_profile.name] = []
            
            return f"مرحباً {user_profile.name}! تم تسجيلك بنجاح. أنا مدربك الشخصي الذكي وسأساعدك في تحقيق أهدافك الصحية."
            
        except Exception as e:
            return f"خطأ في التسجيل: {str(e)}"
    
    def analyze_health_data(self, user_name: str) -> str:
        """تحليل البيانات الصحية للمستخدم"""
        if user_name not in self.user_profiles:
            return "❌ المستخدم غير مسجل. يرجى التسجيل أولاً."
        
        profile = self.user_profiles[user_name]
        user_data = asdict(profile)
        
        # تحويل الـ Enums إلى strings
        user_data["fitness_level"] = profile.fitness_level.value
        user_data["preferred_workouts"] = [w.value for w in profile.preferred_workouts]
        
        analysis = self.health_analyzer.analyze_user_data(user_data)
        
        return self._format_health_analysis(analysis)
    
    def create_workout_plan(self, user_name: str, workout_type: str = "CARDIO", duration: int = 30) -> str:
        """إنشاء خطة تمرين للمستخدم"""
        if user_name not in self.user_profiles:
            return "❌ المستخدم غير مسجل. يرجى التسجيل أولاً."
        
        profile = self.user_profiles[user_name]
        
        requirements = {
            "fitness_level": profile.fitness_level.name,
            "workout_type": workout_type,
            "duration": duration,
            "goals": profile.goals
        }
        
        plan = self.workout_planner.create_workout_plan(requirements)
        
        return self._format_workout_plan(plan)
    
    def track_progress(self, user_name: str, current_weight: float, workouts_completed: int, days_active: int) -> str:
        """تتبع تقدم المستخدم"""
        if user_name not in self.user_profiles:
            return "❌ المستخدم غير مسجل. يرجى التسجيل أولاً."
        
        profile = self.user_profiles[user_name]
        
        progress_data = {
            "current_weight": current_weight,
            "initial_weight": profile.weight,
            "workouts_completed": workouts_completed,
            "days_active": days_active
        }
        
        analysis = self.progress_tracker.analyze_progress(progress_data)
        
        return self._format_progress_analysis(analysis)
    
    def _format_health_analysis(self, analysis: Dict) -> str:
        """تنسيق تحليل البيانات الصحية"""
        if "error" in analysis:
            return f"❌ {analysis['error']}"
        
        result = f"""
📊 **تحليل البيانات الصحية**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 **معلومات المستخدم:**
   • الاسم: {analysis['user_info']['name']}
   • العمر: {analysis['user_info']['age']} سنة
   • مؤشر كتلة الجسم (BMI): {analysis['user_info']['bmi']}
   • تصنيف الوزن: {analysis['user_info']['bmi_category']}

🏃 **تقييم مستوى اللياقة:**
   {analysis['fitness_assessment']}

💡 **التوصيات:**"""
        
        for rec in analysis['recommendations']:
            result += f"\n   • {rec}"
        
        result += f"""

🎯 **تحليل الأهداف:**"""
        
        for goal, details in analysis['goal_analysis'].items():
            result += f"""
   📌 {goal}:
      - الأولوية: {details['priority']}
      - التمارين المناسبة: {', '.join(details['recommended_workouts'])}
      - المدة المقترحة: {details['duration']}"""
        
        schedule = analysis['weekly_schedule_suggestion']
        result += f"""

📅 **الجدول الأسبوعي المقترح:**
   • التكرار: {schedule['frequency']}
   • مدة الجلسة: {schedule['session_duration']}
   • التركيز: {schedule['focus']}
"""
        
        return result
    
    def _format_workout_plan(self, plan: Dict) -> str:
        """تنسيق خطة التمرين"""
        if "error" in plan:
            return f"❌ {plan['error']}"
        
        session_info = plan['session_info']
        result = f"""
🏋️ **خطة التمرين**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 **معلومات الجلسة:**
   • نوع التمرين: {session_info['type']}
   • المستوى: {session_info['level']}
   • المدة الكاملة: {session_info['total_duration']} دقيقة
   • السعرات المتوقع حرقها: {session_info['estimated_calories']} سعرة

🔥 **الإحماء ({plan['warm_up']['duration']} دقائق):**"""
        
        for exercise in plan['warm_up']['exercises']:
            result += f"\n   • {exercise}"
        
        result += f"""

💪 **التمرين الرئيسي:**"""
        
        for exercise in plan['main_workout']['exercises']:
            result += f"\n   • {exercise['name']}"
            if 'duration' in exercise:
                result += f" - {exercise['duration']} دقيقة"
            if 'reps' in exercise:
                result += f" - {exercise['reps']}"
            result += f" ({exercise['intensity']})"
        
        result += f"\n   • الراحة بين المجموعات: {plan['main_workout']['rest_between_sets']}"
        
        result += f"""

🧘 **التهدئة ({plan['cool_down']['duration']} دقائق):**"""
        
        for exercise in plan['cool_down']['exercises']:
            result += f"\n   • {exercise}"
        
        result += f"""

💡 **نصائح مهمة:**"""
        
        for tip in plan['tips']:
            result += f"\n   • {tip}"
        
        return result
    
    def _format_progress_analysis(self, analysis: Dict) -> str:
        """تنسيق تحليل التقدم"""
        if "error" in analysis:
            return f"❌ {analysis['error']}"
        
        weight_progress = analysis['weight_progress']
        activity_stats = analysis['activity_stats']
        
        result = f"""
📈 **تحليل التقدم**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚖️ **تقدم الوزن:**
   • الوزن الأولي: {weight_progress['initial_weight']} كيلو
   • الوزن الحالي: {weight_progress['current_weight']} كيلو
   • التغيير: {weight_progress['change']:+.1f} كيلو ({weight_progress['change_percent']:+.1f}%)

🏃 **إحصائيات النشاط:**
   • التمارين المكتملة: {activity_stats['workouts_completed']}
   • الأيام النشطة: {activity_stats['days_active']}
   • درجة الالتزام: {activity_stats['commitment_score']:.1f}%

🎉 **رسائل تحفيزية:**"""
        
        for message in analysis['motivational_messages']:
            result += f"\n   • {message}"
        
        result += f"""

🎯 **الأهداف القادمة:**"""
        
        for goal in analysis['next_goals']:
            result += f"\n   • {goal}"
        
        return result

def interactive_demo():
    """عرض تفاعلي للمدرب الذكي"""
    
    agent = FitnessAIAgent()
    
    print("🏋️ أهلاً وسهلاً! دعنا نبدأ بتسجيلك في النظام")
    print("=" * 60)
    
    # جمع بيانات المستخدم
    try:
        name = input("📝 اسمك: ").strip()
        age = int(input("🎂 عمرك: ").strip())
        weight = float(input("⚖️ وزنك (بالكيلو): ").strip())
        height = float(input("📏 طولك (بالسم): ").strip())
        
        print("\n🏃 اختر مستوى لياقتك:")
        print("1. مبتدئ")
        print("2. متوسط")
        print("3. متقدم")
        
        fitness_choice = input("اختيارك (1-3): ").strip()
        fitness_levels = {"1": "مبتدئ", "2": "متوسط", "3": "متقدم"}
        fitness_level = fitness_levels.get(fitness_choice, "مبتدئ")
        
        print("\n🎯 ما هي أهدافك؟ (اختر رقم واحد أو أكثر مفصولة بفواصل)")
        print("1. فقدان الوزن")
        print("2. بناء العضلات")
        print("3. تحسين اللياقة")
        print("4. زيادة القوة")
        
        goals_input = input("اختيارك: ").strip()
        goals_mapping = {
            "1": "فقدان الوزن",
            "2": "بناء العضلات", 
            "3": "تحسين اللياقة",
            "4": "زيادة القوة"
        }
        
        goals = []
        for choice in goals_input.split(","):
            choice = choice.strip()
            if choice in goals_mapping:
                goals.append(goals_mapping[choice])
        
        if not goals:
            goals = ["تحسين اللياقة"]
        
        available_time = int(input("⏰ كم دقيقة متاحة لك يومياً للتمرين؟ ").strip() or "30")
        
        # إعداد بيانات المستخدم
        user_data = {
            "name": name,
            "age": age,
            "weight": weight,
            "height": height,
            "fitness_level": fitness_level,
            "goals": goals,
            "health_conditions": [],
            "preferred_workouts": ["كارديو", "قوة"],
            "available_time": available_time
        }
        
        # تسجيل المستخدم
        print("\n" + "=" * 60)
        registration_result = agent.register_user(user_data)
        print("✅", registration_result)
        
        # تحليل البيانات الصحية
        print("\n📊 دعني أحلل بياناتك الصحية...")
        health_analysis = agent.analyze_health_data(name)
        print(health_analysis)
        
        # إنشاء خطة تمرين
        print("\n🏋️ الآن سأنشئ لك خطة تمرين مخصصة...")
        workout_plan = agent.create_workout_plan(name, "CARDIO", available_time)
        print(workout_plan)
        
        # محاكاة تتبع التقدم
        print("\n📈 مثال على تتبع التقدم (بعد أسبوع من التمرين)...")
        progress_analysis = agent.track_progress(name, weight - 0.5, 5, 7)
        print(progress_analysis)
        
        print("\n🎉 انتهى العرض التوضيحي!")
        print("💡 يمكنك الآن استخدام المدرب الذكي لتحقيق أهدافك الصحية!")
        
    except KeyboardInterrupt:
        print("\n\n👋 شكراً لك! نراك قريباً!")
    except Exception as e:
        print(f"\n❌ حدث خطأ: {str(e)}")
        print("💡 تأكد من إدخال البيانات بالشكل الصحيح")

if __name__ == "__main__":
    interactive_demo()