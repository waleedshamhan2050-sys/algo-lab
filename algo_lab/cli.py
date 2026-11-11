#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
الواجهة التفاعلية لمختبر الخوارزميات — ورشة شِراع 5.
Algo Lab CLI — قائمة عربية واحدة تجمع مزايا المختبر الست.
"""
import shutil
import sys

from . import challenges, cpp_gen, languages, selfcheck
from .workbench import (
    CLEAN_SAMPLE,
    CLINIC_PLAN,
    EXAMPLES,
    clean_code_report,
    demo,
    flowchart,
    parse_pseudocode,
    run_pseudocode,
    run_tests,
    six_step_plan,
    to_python,
)

MENU = """=== مختبر الخوارزميات — ورشة 5: البرمجة ولغات البرمجة ===
البرمجة منطق وخوارزميات قبل الأكواد.
  1  بناء خوارزمية (شبه كود ← مخطط تدفق ← Python + C++ ← تشغيل فعلي)
  2  فاحص الكود النظيف (المبادئ الثمانية)
  3  دليل خطوات حل المشكلات الست (مثال العيادة + مشكلتك)
  4  دليل لغات البرمجة (التصنيف، التاريخ، واقتراح لغة حسب هدفك)
  5  فحص نوع المبرمج (الناقل / الحافظ / الماهر)
  6  تحديات المبرمجين ونصائحها
  7  العرض الكامل (أمثلة الورشة الثلاثة + الفحص + خطة العيادة)
  0  خروج
"""


def _pick_example():
    print("\nأمثلة الورشة:")
    for i, key in enumerate(("sum", "pass", "hello"), 1):
        print(f"  {i}  {EXAMPLES[key][0]}")
    print("  4  اكتب شبه كودك بنفسك")
    choice = input("اختر (1-4): ").strip()
    keys = {"1": "sum", "2": "pass", "3": "hello"}
    if choice in keys:
        return EXAMPLES[keys[choice]]
    if choice == "4":
        print("اكتب شبه الكود (سطر لكل خطوة، وأنهِ بسطر فارغ):")
        print("الكلمات: ابدأ / انتهِ / اقرأ X / اطبع X / X = تعبير / إذا شرط /")
        print("         وإلا / انتهِ إذا / بينما شرط / انتهِ بينما")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line.strip():
                break
            lines.append(line)
        return ("شبه كودك", "\n".join(lines), [])
    return None


def _build_algorithm():
    picked = _pick_example()
    if not picked:
        print("اختيار غير صحيح.")
        return
    title, pseudo, inputs = picked
    print(f"\n--- {title} ---")
    print("شبه الكود:\n" + pseudo)
    try:
        steps = parse_pseudocode(pseudo)
    except ValueError as exc:
        print(f"⚠️  {exc}")
        return
    print("\nمخطط التدفق:\n" + "\n".join(flowchart(steps)))
    print("\nترجمته إلى Python:\n" + "\n".join(to_python(steps)))
    print("\nترجمته إلى C++ (لغة أمثلة الورشة):\n"
          + cpp_gen.cpp_with_note(pseudo))
    if title.startswith("نجاح"):
        try:
            grade = input("أدخل درجة للتجربة (Enter = 70 ثم 40): ").strip()
            given = [int(grade)] if grade else [70, 40]
        except ValueError:
            given = [70, 40]
        for g in given:
            print(f"الناتج (الدرجة {g}):\n" + run_pseudocode(pseudo, [g]).rstrip())
    else:
        try:
            print("الناتج عند تشغيل Python:\n"
                  + run_pseudocode(pseudo, inputs).rstrip())
        except ValueError as exc:
            print(f"⚠️  التشغيل يحتاج مدخلات: {exc}")
    if shutil.which("g++"):
        try:
            cpp = cpp_gen.to_cpp(pseudo)
            if title.startswith("نجاح"):
                out = cpp_gen.run_cpp(cpp, [70])
                print("الناتج عند تشغيل C++ (الدرجة 70):\n" + out.rstrip())
            elif inputs:
                out = cpp_gen.run_cpp(cpp, inputs)
                print("الناتج عند تشغيل C++:\n" + out.rstrip())
            else:
                out = cpp_gen.run_cpp(cpp, [])
                print("الناتج عند تشغيل C++:\n" + out.rstrip())
            print("✅ الكود نفسه يعمل في Python وC++ — المنطق واحد، والصياغة فقط تختلف.")
        except (RuntimeError, ValueError) as exc:
            print(f"⚠️  تشغيل C++ تعذّر: {exc}")
    else:
        print("(g++ غير متوفر على هذا الجهاز — كود C++ مولَّد وجاهز للتجميع.)")


def _clean_code():
    print("\nالصق كود Python للفحص (أنهِ بسطر فارغ)، أو اكتب 'مثال' للكود الفوضوي،")
    print("أو 'نظيف' للكود النظيف من الورشة:")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    source = "\n".join(lines)
    if source.strip() == "مثال":
        from .workbench import MESSY_SAMPLE
        source = MESSY_SAMPLE
        title = "كود فوضوي (قبل)"
    elif source.strip() == "نظيف":
        source = CLEAN_SAMPLE
        title = "كود نظيف (بعد)"
    else:
        title = "كودك"
    try:
        report, _ = clean_code_report(source, title)
    except SyntaxError as exc:
        print(f"⚠️  الكود فيه خطأ صياغي لا يسمح بفحصه: {exc}")
        return
    print("\n" + report)


def _six_steps():
    print("\n" + six_step_plan(CLINIC_PLAN))
    answer = input("\nهل تريد بناء خطة لمشكلتك؟ (نعم/لا): ").strip()
    if answer not in ("نعم", "نعم", "yes", "y"):
        return
    name = input("ما المشكلة؟ ").strip() or "مشكلتي"
    plan = {
        "name": name,
        "inputs": input("المدخلات: ").strip() or "—",
        "outputs": input("المخرجات المطلوبة: ").strip() or "—",
        "constraints": input("القيود: ").strip() or "—",
        "subproblems": [s.strip() for s in
                        input("المشكلات الصغيرة (افصل بينها بفاصلة): ").split("،")
                        if s.strip()],
        "algorithm": input("الخوارزمية في سطر واحد: ").strip() or "ابدأ ← انتهِ",
        "tool": input("الأداة/اللغة: ").strip() or "Python",
        "tests": [s.strip() for s in
                  input("اختباراتك (افصل بينها بفاصلة): ").split("،") if s.strip()],
    }
    if not plan["subproblems"]:
        plan["subproblems"] = ["قسّم المشكلة إلى أجزاء صغيرة أولًا"]
    if not plan["tests"]:
        plan["tests"] = ["اختبر بمثال واحد معروف الناتج"]
    print("\n" + six_step_plan(plan))


def _languages():
    print("\n" + languages.languages_report())
    goal = input("\nما هدفك أو مشروعك؟ (اكتب هدفًا، أو Enter للتخطي): ").strip()
    if goal:
        lang, why = languages.recommend_language(goal)
        print(f"\nاللغة المقترحة لهدفك «{goal}»: {lang}")
        print(f"لماذا؟ {why}")
        print("وتذكّر: لا توجد «أفضل لغة» مطلقًا — هذه بداية مناسبة لا حكم نهائي.")


def _selfcheck():
    print("\n" + selfcheck.types_report())
    print("\nأجب بـ a أو b أو c عن كل سؤال:")
    answers = []
    for i, question in enumerate(selfcheck.QUESTIONS, 1):
        print(f"\n{i}. {question['q']}")
        for key in ("a", "b", "c"):
            print(f"   {key}) {question['options'][key][0]}")
        while True:
            ans = input("إجابتك: ").strip().lower()
            if ans in ("a", "b", "c"):
                answers.append(ans)
                break
            print("اختر a أو b أو c.")
    print("\n" + selfcheck.selfcheck_report(answers))


def _challenges():
    print("\n" + challenges.challenges_report())


def interactive():
    print(MENU)
    while True:
        try:
            choice = input("اختر رقمًا (0-7): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if choice == "0":
            break
        elif choice == "1":
            _build_algorithm()
        elif choice == "2":
            _clean_code()
        elif choice == "3":
            _six_steps()
        elif choice == "4":
            _languages()
        elif choice == "5":
            _selfcheck()
        elif choice == "6":
            _challenges()
        elif choice == "7":
            print("\n" + demo())
        else:
            print("اختر رقمًا من 0 إلى 7.")
        print("\n" + MENU)
    print("إلى اللقاء — ابدأ بالورقة والقلم، وابنِ الخوارزمية قبل الكود.")


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if "--test" in args:
        return run_tests()
    if "--demo" in args:
        print(demo())
        return None
    interactive()
    return None
