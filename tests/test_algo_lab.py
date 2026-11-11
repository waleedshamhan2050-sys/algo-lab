#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
الفحص الشامل لمختبر الخوارزميات — كل المزايا الست، نهايةً إلى نهاية.
Full end-to-end tests for Algo Lab (SHIRAA 2026, Workshop 5).

    python3 tests/test_algo_lab.py     # من جذر المشروع
    python3 main.py --test             # نفس الفحص من نقطة الدخول

يطبع ✅/❌ لكل فحص، وينتهي بـ PASS أو FAIL (ويخرج 0 أو 1).
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algo_lab import challenges, cpp_gen, languages, selfcheck
from algo_lab.workbench import (
    CLEAN_SAMPLE,
    CLINIC_PLAN,
    EXAMPLE_HELLO,
    EXAMPLE_PASS,
    EXAMPLE_SUM,
    MESSY_SAMPLE,
    check_clean_code,
    demo,
    flowchart,
    parse_pseudocode,
    run_pseudocode,
    run_tests as workbench_tests,
    six_step_plan,
    to_python,
)

RESULTS = []


def check(name, got, want=True):
    good = got == want
    RESULTS.append(good)
    mark = "✅" if good else "❌"
    extra = "" if good else f" (حصلنا على {got!r} بدل {want!r})"
    print(f"{mark} {name}{extra}")
    return good


def run_all():
    print("=== الفحص الشامل: مختبر الخوارزميات (ورشة 5) ===\n")
    print("--- 1. باني الخوارزميات: أمثلة الورشة الثلاثة (Python) ---")
    check("جمع عددين 5+10 = 15",
          run_pseudocode(EXAMPLE_SUM, [5, 10]), "15\n")
    check("نجاح (الدرجة 70)", run_pseudocode(EXAMPLE_PASS, [70]), "ناجح\n")
    check("رسوب (الدرجة 40)", run_pseudocode(EXAMPLE_PASS, [40]), "راسب\n")
    check("طباعة «مرحبًا» 3 مرات",
          run_pseudocode(EXAMPLE_HELLO, []), "مرحبًا\nمرحبًا\nمرحبًا\n")
    code = "\n".join(to_python(parse_pseudocode(EXAMPLE_SUM)))
    check("ترجمة Python فيها SUM = A + B", "SUM = A + B" in code)

    print("\n--- 2. توليد C++ وتشغيله فعليًا (g++) ---")
    cpp = cpp_gen.to_cpp(EXAMPLE_SUM)
    check("كود C++ فيه int main", "int main()" in cpp)
    check("كود C++ فيه std::cout", "std::cout" in cpp)
    check("كود C++ فيه return 0", "return 0;" in cpp)
    cpp_pass = cpp_gen.cpp_with_note(EXAMPLE_PASS)
    check("كود C++ للنجاح يترجم «الدرجة» إلى grade",
          "grade" in cpp_pass and "الدرجة" not in cpp_pass.split("\n", 1)[1])
    if shutil.which("g++"):
        check("تشغيل C++ لجمع عددين = 15",
              cpp_gen.run_cpp(cpp, [5, 10]), "15\n")
        check("تشغيل C++ للنجاح (70) = ناجح",
              cpp_gen.run_cpp(cpp_gen.to_cpp(EXAMPLE_PASS), [70]), "ناجح\n")
        check("تشغيل C++ للرسوب (40) = راسب",
              cpp_gen.run_cpp(cpp_gen.to_cpp(EXAMPLE_PASS), [40]), "راسب\n")
        check("تشغيل C++ لمرحبًا ×3",
              cpp_gen.run_cpp(cpp_gen.to_cpp(EXAMPLE_HELLO), []),
              "مرحبًا\nمرحبًا\nمرحبًا\n")
    else:
        print("⚠️  g++ غير متوفر — تم تخطي تشغيل C++ (التوليد مفحوص أعلاه)")

    print("\n--- 3. مخططات التدفق (أشكال الورشة) ---")
    fc = "\n".join(flowchart(parse_pseudocode(EXAMPLE_SUM)))
    check("مخطط الجمع فيه [ SUM = A + B ]", "[ SUM = A + B ]" in fc)
    check("مخطط الجمع فيه / اطبع SUM /", "/ اطبع SUM /" in fc)
    fc2 = "\n".join(flowchart(parse_pseudocode(EXAMPLE_PASS)))
    check("مخطط القرار فيه ◇ الدرجة", "◇ الدرجة >= 50 ؟" in fc2)
    fc3 = "\n".join(flowchart(parse_pseudocode(EXAMPLE_HELLO)))
    check("مخطط الحلقة فيه علامة العودة ↺", "↺" in fc3)

    print("\n--- 4. فاحص الكود النظيف (المبادئ الثمانية) ---")
    check("الكود الفوضوي عليه ≥5 ملاحظات", len(check_clean_code(MESSY_SAMPLE)) >= 5)
    check("الكود النظيف بلا ملاحظات", check_clean_code(CLEAN_SAMPLE), [])
    messy = check_clean_code(MESSY_SAMPLE)
    principles = {n for n, _, _ in messy}
    check("الملاحظات تغطي ≥4 مبادئ مختلفة", len(principles) >= 4)

    print("\n--- 5. دليل خطوات الحل الست ---")
    plan = six_step_plan(CLINIC_PLAN)
    check("الخطة فيها الخطوات الست",
          all(f"الخطوة {n}" in plan for n in range(1, 7)))
    check("خطة العيادة تذكر الأولوية", "الأولوية" in plan)
    check("خطة العيادة تذكر الحجز من البيت", "البيت" in plan)

    print("\n--- 6. دليل اللغات ---")
    lang, _ = languages.recommend_language("أريد بناء موقع ويب")
    check("الويب ← JavaScript", lang, "JavaScript")
    lang, _ = languages.recommend_language("ذكاء اصطناعي وتعلم آلة")
    check("الذكاء الاصطناعي ← Python", lang, "Python")
    lang, _ = languages.recommend_language("ألعاب")
    check("الألعاب ← C++", lang, "C++")
    lang, _ = languages.recommend_language("تطبيق أندرويد")
    check("الجوال ← Kotlin", lang, "Kotlin")
    lang, why = languages.recommend_language("شيء غير معروف إطلاقًا")
    check("الهدف الغامض ← C++ (رأي المدرب)", lang, "C++")
    report = languages.languages_report()
    check("الدليل يذكر SQL ليست لغة برمجة", "ليست لغة برمجة" in report)
    check("الدليل يذكر HTML لغة وصف لا برمجة", "HTML: لغة وصف لبنية الصفحة" in report)
    check("الدليل يذكر قاعدة «لا أفضل لغة»", "لا توجد «أفضل لغة»" in report)
    check("التاريخ فيه 6 محطات", len(languages.TIMELINE), 6)

    print("\n--- 7. فحص نوع المبرمج ---")
    all_carrier = selfcheck.assess(["a"] * 6)
    check("إجابات الناقل كلها ← الناقل", all_carrier["type"], "carrier")
    all_skilled = selfcheck.assess(["c"] * 6)
    check("إجابات الماهر كلها ← الماهر", all_skilled["type"], "skilled")
    all_mem = selfcheck.assess(["b"] * 6)
    check("إجابات الحافظ كلها ← الحافظ", all_mem["type"], "memorizer")
    check("نصيحة الماهر تذكر الشريك", "شريك" in all_skilled["advice"])
    check("قواعد الذكاء الاصطناعي 4 قواعد",
          len(selfcheck.AI_PARTNER_RULES), 4)

    print("\n--- 8. تحديات المبرمجين ---")
    check("التحديات 5", len(challenges.CHALLENGES), 5)
    check("كل تحدٍّ له نصيحة وقاعدة", all(
        c["tip"] and c["workshop_rule"] for c in challenges.CHALLENGES))

    print("\n--- 9. فحص المنضدة الأصلية (العملية 5) ---")
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        ok = workbench_tests()
    check("الفحص الذاتي للمنضدة PASS", ok, True)

    print("\n--- 10. العرض الكامل ---")
    demo_text = demo()
    check("العرض فيه الأمثلة الثلاثة",
          all(k in demo_text for k in ("جمع عددين", "نجاح أو رسوب", "مرحبًا")))
    check("العرض فيه قاعدة الورشة", "المنطق واحد في كل اللغات" in demo_text)

    passed = sum(RESULTS)
    total = len(RESULTS)
    print(f"\n=== النتيجة: {passed}/{total} — {'PASS' if all(RESULTS) else 'FAIL'} ===")
    return all(RESULTS)


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
