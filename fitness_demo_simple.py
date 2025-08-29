# مثال مبسط للمدرب الذكي - بدون تفاعل
# Health & Fitness AI Agent Coach - Simple Demo

import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

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

class HealthDataAnalyzer:
    """أداة تحليل البيانات الصحية"""
    
    def analyze_user_data(self, profile: UserProfile) -> Dict:
        """تحليل بيانات المستخدم"""
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
        
        analysis = {
            "user_info": {
                "name": profile.name,
                "age": profile.age,
                "bmi": bmi,
                "bmi_category": bmi_category
            },
            "fitness_assessment": self._assess_fitness_level(profile),
            "recommendations": recommendations,
            "goal_analysis": self._analyze_goals(profile.goals),
            "weekly_schedule": self._suggest_weekly_schedule(profile)
        }
        
        return analysis
    
    def _assess_fitness_level(self, profile: UserProfile) -> str:
        """تقييم مستوى اللياقة"""
        bmi = profile.calculate_bmi()
        
        if profile.age < 30 and 18.5 <= bmi <= 24.9:
            return "حالة صحية ممتازة للعمر"
        elif profile.age >= 50:
            return "يُنصح بالتركيز على تمارين المرونة والتوازن"
        else:
            return "حالة صحية جيدة مع إمكانية التحسن"
    
    def _analyze_goals(self, goals: List[str]) -> Dict:
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
    
    def create_workout_plan(self, fitness_level: str, workout_type: str, duration: int) -> Dict:
        """إنشاء خطة تمرين"""
        
        exercises_db = {
            "CARDIO": {
                "مبتدئ": [
                    {"name": "المشي السريع", "duration": 10, "intensity": "خفيف"},
                    {"name": "صعود الدرج", "duration": 5, "intensity": "متوسط"},
                    {"name": "تمارين الإحماء", "duration": 5, "intensity": "خفيف"}
                ],
                "متوسط": [
                    {"name": "الجري الخفيف", "duration": 15, "intensity": "متوسط"},
                    {"name": "نط الحبل", "duration": 10, "intensity": "عالي"},
                    {"name": "تمارين الأيروبيك", "duration": 15, "intensity": "متوسط"}
                ],
                "متقدم": [
                    {"name": "الجري السريع", "duration": 20, "intensity": "عالي"},
                    {"name": "تدريب متقطع", "duration": 15, "intensity": "عالي جداً"},
                    {"name": "تمارين بيربي", "duration": 10, "intensity": "عالي"}
                ]
            },
            "STRENGTH": {
                "مبتدئ": [
                    {"name": "تمرين الضغط (معدل)", "reps": "3x8", "intensity": "خفيف"},
                    {"name": "القرفصاء", "reps": "3x10", "intensity": "متوسط"},
                    {"name": "تمرين البلانك", "duration": "30 ثانية x3", "intensity": "متوسط"}
                ],
                "متوسط": [
                    {"name": "تمرين الضغط", "reps": "3x12", "intensity": "متوسط"},
                    {"name": "القرفصاء مع الأثقال", "reps": "4x10", "intensity": "عالي"},
                    {"name": "تمرين العقلة", "reps": "3x5", "intensity": "عالي"}
                ],
                "متقدم": [
                    {"name": "تمرين الضغط المتفجر", "reps": "4x8", "intensity": "عالي"},
                    {"name": "الديدليفت", "reps": "4x6", "intensity": "عالي جداً"},
                    {"name": "تمارين الأوزان المركبة", "reps": "5x5", "intensity": "عالي جداً"}
                ]
            }
        }
        
        # اختيار التمارين المناسبة
        selected_exercises = exercises_db.get(workout_type, {}).get(fitness_level, [])
        
        # تقدير السعرات المحروقة
        calories_per_minute = {"CARDIO": 12, "STRENGTH": 8}
        estimated_calories = duration * calories_per_minute.get(workout_type, 10)
        
        workout_plan = {
            "session_info": {
                "type": workout_type,
                "level": fitness_level,
                "total_duration": duration,
                "estimated_calories": estimated_calories
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
            "tips": [
                "اشرب الماء قبل وأثناء وبعد التمرين",
                "استمع لجسمك ولا تتجاهل الألم",
                "احرص على النوم الكافي للاستشفاء"
            ]
        }
        
        return workout_plan

def print_formatted_analysis(analysis: Dict):
    """طباعة التحليل بشكل منسق"""
    print("📊 **تحليل البيانات الصحية**")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    user_info = analysis['user_info']
    print(f"👤 **معلومات المستخدم:**")
    print(f"   • الاسم: {user_info['name']}")
    print(f"   • العمر: {user_info['age']} سنة")
    print(f"   • مؤشر كتلة الجسم (BMI): {user_info['bmi']}")
    print(f"   • تصنيف الوزن: {user_info['bmi_category']}")
    
    print(f"\n🏃 **تقييم مستوى اللياقة:**")
    print(f"   {analysis['fitness_assessment']}")
    
    print(f"\n💡 **التوصيات:**")
    for rec in analysis['recommendations']:
        print(f"   • {rec}")
    
    print(f"\n🎯 **تحليل الأهداف:**")
    for goal, details in analysis['goal_analysis'].items():
        print(f"   📌 {goal}:")
        print(f"      - الأولوية: {details['priority']}")
        print(f"      - التمارين المناسبة: {', '.join(details['recommended_workouts'])}")
        print(f"      - المدة المقترحة: {details['duration']}")
    
    schedule = analysis['weekly_schedule']
    print(f"\n📅 **الجدول الأسبوعي المقترح:**")
    print(f"   • التكرار: {schedule['frequency']}")
    print(f"   • مدة الجلسة: {schedule['session_duration']}")
    print(f"   • التركيز: {schedule['focus']}")

def print_formatted_workout_plan(plan: Dict):
    """طباعة خطة التمرين بشكل منسق"""
    print("\n🏋️ **خطة التمرين**")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    session_info = plan['session_info']
    print(f"📋 **معلومات الجلسة:**")
    print(f"   • نوع التمرين: {session_info['type']}")
    print(f"   • المستوى: {session_info['level']}")
    print(f"   • المدة الكاملة: {session_info['total_duration']} دقيقة")
    print(f"   • السعرات المتوقع حرقها: {session_info['estimated_calories']} سعرة")
    
    print(f"\n🔥 **الإحماء ({plan['warm_up']['duration']} دقائق):**")
    for exercise in plan['warm_up']['exercises']:
        print(f"   • {exercise}")
    
    print(f"\n💪 **التمرين الرئيسي:**")
    for exercise in plan['main_workout']['exercises']:
        print(f"   • {exercise['name']}", end="")
        if 'duration' in exercise:
            print(f" - {exercise['duration']} دقيقة", end="")
        if 'reps' in exercise:
            print(f" - {exercise['reps']}", end="")
        print(f" ({exercise['intensity']})")
    
    print(f"   • الراحة بين المجموعات: {plan['main_workout']['rest_between_sets']}")
    
    print(f"\n🧘 **التهدئة ({plan['cool_down']['duration']} دقائق):**")
    for exercise in plan['cool_down']['exercises']:
        print(f"   • {exercise}")
    
    print(f"\n💡 **نصائح مهمة:**")
    for tip in plan['tips']:
        print(f"   • {tip}")

def demo_fitness_agent():
    """عرض توضيحي للمدرب الذكي"""
    
    print("🏋️ مرحباً بك في المدرب الذكي للياقة البدنية!")
    print("🤖 سأعرض لك مثالاً حقيقياً على كيفية عمل النظام")
    print("=" * 80)
    
    # إنشاء ملف مستخدم تجريبي
    user_profile = UserProfile(
        name="أحمد محمد",
        age=28,
        weight=80,
        height=175,
        fitness_level=FitnessLevel.BEGINNER,
        goals=["فقدان الوزن", "تحسين اللياقة"],
        health_conditions=[],
        preferred_workouts=[WorkoutType.CARDIO, WorkoutType.STRENGTH],
        available_time=45
    )
    
    print(f"✅ تم إنشاء ملف المستخدم: {user_profile.name}")
    print(f"   العمر: {user_profile.age} | الوزن: {user_profile.weight} كيلو | الطول: {user_profile.height} سم")
    print(f"   المستوى: {user_profile.fitness_level.value} | الوقت المتاح: {user_profile.available_time} دقيقة")
    
    # تحليل البيانات الصحية
    print("\n📊 جاري تحليل البيانات الصحية...")
    analyzer = HealthDataAnalyzer()
    analysis = analyzer.analyze_user_data(user_profile)
    print_formatted_analysis(analysis)
    
    # إنشاء خطة تمرين كارديو
    print("\n🏃 جاري إنشاء خطة تمرين كارديو...")
    planner = WorkoutPlanner()
    cardio_plan = planner.create_workout_plan(
        user_profile.fitness_level.value, 
        "CARDIO", 
        user_profile.available_time
    )
    print_formatted_workout_plan(cardio_plan)
    
    # إنشاء خطة تمرين قوة
    print("\n💪 جاري إنشاء خطة تمرين قوة...")
    strength_plan = planner.create_workout_plan(
        user_profile.fitness_level.value,
        "STRENGTH", 
        user_profile.available_time
    )
    print_formatted_workout_plan(strength_plan)
    
    print("\n🎉 انتهى العرض التوضيحي!")
    print("💡 هذا مثال حقيقي على كيفية عمل المدرب الذكي للياقة البدنية")
    print("🚀 يمكن توسيع النظام ليشمل الذكاء الاصطناعي والمحادثات التفاعلية")

if __name__ == "__main__":
    demo_fitness_agent()