def calculate_health_score(age, heart_rate, systolic_bp, spo2, blood_sugar):
    score = 100
    reasons = []
    tips = []

    # AGE
    if age > 70:
        score -= 20
        reasons.append("Advanced age increases cardiovascular risk")
        tips.append("Schedule regular preventive screenings")
    elif age > 55:
        score -= 10
        reasons.append("Age is a moderate cardiovascular risk factor")
        tips.append("Maintain an active lifestyle and monitor vitals")
    elif age > 40:
        score -= 5

    # HEART RATE
    if heart_rate > 100:
        score -= 25
        reasons.append("Significantly elevated heart rate detected")
        tips.append("Reduce stress & caffeine; consult a doctor if persistent")
    elif heart_rate > 85:
        score -= 10
        reasons.append("Slightly elevated heart rate")
        tips.append("Try relaxation techniques and limit stimulants")
    elif heart_rate < 60:
        score -= 8
        reasons.append("Heart rate below normal range (bradycardia)")
        tips.append("Consult a doctor about low resting heart rate")

    # BLOOD PRESSURE
    if systolic_bp > 140:
        score -= 30
        reasons.append("Stage 2 hypertension — high cardiovascular risk")
        tips.append("Seek medical consultation immediately; reduce salt intake")
    elif systolic_bp > 130:
        score -= 20
        reasons.append("Stage 1 hypertension detected")
        tips.append("Lifestyle changes and possible medication review recommended")
    elif systolic_bp > 120:
        score -= 10
        reasons.append("Elevated blood pressure (pre-hypertension)")
        tips.append("Reduce sodium and increase physical activity")
    elif systolic_bp < 90:
        score -= 10
        reasons.append("Low blood pressure detected")
        tips.append("Increase fluid intake; consult a doctor")

    # SPO2
    if spo2 < 80:
        score -= 40
        reasons.append("Critically low oxygen saturation — urgent attention needed")
        tips.append("Seek emergency medical care immediately")
    elif spo2 < 90:
        score -= 25
        reasons.append("Low oxygen saturation detected")
        tips.append("Consult a doctor about breathing difficulties")
    elif spo2 < 95:
        score -= 10
        reasons.append("Moderately low oxygen level")
        tips.append("Consult a doctor and monitor oxygen levels closely")

    # BLOOD SUGAR
    if blood_sugar < 70:
        score -= 30
        reasons.append("Low blood sugar (hypoglycemia) — needs attention")
        tips.append("Consume fast-acting carbohydrates; consult a doctor")
    elif 70 <= blood_sugar <= 100:
        pass  # Normal
    elif 100 < blood_sugar <= 125:
        score -= 15
        reasons.append("Pre-diabetes range blood sugar")
        tips.append("Exercise regularly and follow a balanced diet")
    else:
        score -= 25
        reasons.append("High blood sugar — diabetes risk")
        tips.append("Consult a doctor; monitor diet and sugar intake")

    score = max(0, min(100, score))

    if not reasons:
        reasons.append("All vitals are within healthy ranges — great job!")
        tips.append("Keep maintaining your healthy lifestyle")

    if score >= 85:   grade = "Excellent"
    elif score >= 70: grade = "Good"
    elif score >= 50: grade = "Fair"
    elif score >= 30: grade = "Poor"
    else:             grade = "Critical"

    return {"score": score, "reasons": reasons, "tips": tips, "grade": grade}
