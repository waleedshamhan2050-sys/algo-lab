#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
واجهة ويب اختيارية لمختبر الخوارزميات (تحتاج Streamlit — غير إلزامية).
Optional Streamlit UI for Algo Lab (needs Streamlit; the CLI works without it).

    streamlit run app_streamlit.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import streamlit as st
except ImportError:  # pragma: no cover
    print("هذه الواجهة تحتاج Streamlit: pip install streamlit")
    print("والواجهة الطرفية تعمل بدونه: python3 main.py")
    raise SystemExit(1)

from algo_lab import challenges, cpp_gen, languages, selfcheck
from algo_lab.workbench import (
    CLEAN_SAMPLE,
    CLINIC_PLAN,
    EXAMPLES,
    MESSY_SAMPLE,
    clean_code_report,
    flowchart,
    parse_pseudocode,
    run_pseudocode,
    six_step_plan,
    to_python,
)

st.set_page_config(page_title="مختبر الخوارزميات — Algo Lab", layout="wide")
st.title("🧪 مختبر الخوارزميات — Algo Lab")
st.caption("البرمجة منطق وخوارزميات قبل الأكواد — ورشة شِراع 5، 11 نوفمبر 2026")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "باني الخوارزميات", "الكود النظيف", "خطوات الحل الست",
    "دليل اللغات", "نوع المبرمج", "التحديات",
])

with tab1:
    st.header("باني الخوارزميات")
    choice = st.selectbox("اختر مثالًا من الورشة",
                          [EXAMPLES[k][0] for k in ("sum", "pass", "hello")])
    keys = ("sum", "pass", "hello")
    title, pseudo, inputs = EXAMPLES[keys[
        [EXAMPLES[k][0] for k in keys].index(choice)]]
    st.subheader("شبه الكود")
    st.code(pseudo, language="text")
    steps = parse_pseudocode(pseudo)
    st.subheader("مخطط التدفق")
    st.code("\n".join(flowchart(steps)), language="text")
    st.subheader("Python")
    st.code("\n".join(to_python(steps)), language="python")
    st.subheader("C++")
    st.code(cpp_gen.cpp_with_note(pseudo), language="cpp")
    if st.button("شغّل الخوارزمية", key="run_example"):
        if title.startswith("نجاح"):
            st.write("الدرجة 70 ←", run_pseudocode(pseudo, [70]).strip())
            st.write("الدرجة 40 ←", run_pseudocode(pseudo, [40]).strip())
        else:
            st.code(run_pseudocode(pseudo, inputs), language="text")

with tab2:
    st.header("فاحص الكود النظيف — المبادئ الثمانية")
    sample = st.radio("اختر كودًا", ["كودك", "مثال فوضوي", "مثال نظيف"])
    if sample == "مثال فوضوي":
        source = MESSY_SAMPLE
    elif sample == "مثال نظيف":
        source = CLEAN_SAMPLE
    else:
        source = st.text_area("الصق كود Python هنا", height=200)
    if st.button("افحص الكود"):
        try:
            report, _ = clean_code_report(source, sample)
            st.code(report, language="text")
        except SyntaxError as exc:
            st.error(f"خطأ صياغي في الكود: {exc}")

with tab3:
    st.header("خطوات حل المشكلات الست")
    st.code(six_step_plan(CLINIC_PLAN), language="text")

with tab4:
    st.header("دليل لغات البرمجة")
    st.code(languages.languages_report(), language="text")
    goal = st.text_input("ما هدفك أو مشروعك؟")
    if goal:
        lang, why = languages.recommend_language(goal)
        st.success(f"اللغة المقترحة: {lang} — {why}")

with tab5:
    st.header("فحص نوع المبرمج — الناقل / الحافظ / الماهر")
    answers = []
    for question in selfcheck.QUESTIONS:
        pick = st.radio(question["q"],
                        [f"{k}) {v[0]}" for k, v in question["options"].items()],
                        key=question["q"])
        answers.append(pick[0])
    if st.button("اعرف نتيجتك"):
        st.code(selfcheck.selfcheck_report(answers), language="text")

with tab6:
    st.header("تحديات المبرمجين ونصائحها")
    st.code(challenges.challenges_report(), language="text")
