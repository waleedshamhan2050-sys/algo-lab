# مختبر الخوارزميات — Algo Lab 🧪

**تعلّم البرمجة كما علّمتها ورشة شِراع 5: المنطق والخوارزميات قبل الأكواد.**

> «البرمجة منطق وخوارزميات قبل الأكواد — من أتقن المنطق انتقل بين اللغات في أيام، ومن حفظ الأكواد دون فهم يستبدله الذكاء الاصطناعي.»
> — م. مفضّل عبد الملك الشرعبي، ورشة «البرمجة ولغات البرمجة»، شِراع 2026، 11 نوفمبر 2026

**Learn programming the Workshop 5 way: logic and algorithms BEFORE code.**

---

## ما هذا؟ | What is it?

تطبيق عملي عربي لتعلّم البرمجة من الصفر، مبني على ورشة 5 من هاكاثون شِراع 2026 (SHIRAA). يأخذك من الفكرة إلى الخوارزمية إلى الكود — بالترتيب الصحيح الذي علّمه المدرب: ابدأ بالورقة والقلم، وابنِ الخوارزمية قبل الكود.

An Arabic hands-on app for learning programming from zero, built from Workshop 5 of the SHIRAA 2026 hackathon. It takes you from the idea to the algorithm to the code — in the order the trainer taught: start with paper and pen, build the algorithm before the code.

## المزايا | Features

1. **باني الخوارزميات | Algorithm builder** — اكتب شبه كود بالعربية فيُترجم إلى Python **وC++** (لغة أمثلة الورشة) ويُنفَّذ فعليًا، مع مخطط تدفق ASCII بأشكال الورشة. الأمثلة الثلاثة من الورشة مدمجة: جمع عددين (5+10=15)، نجاح/رسوب طالب (الدرجة ≥ 50)، وطباعة «مرحبًا» 3 مرات بحلقة WHILE.
   Write Arabic pseudocode → it translates to Python **and C++** and really runs, with an ASCII flowchart in the workshop's shapes. The workshop's three examples are built in.
2. **فاحص الكود النظيف | Clean-code checker** — يفحص أي دالة Python بمبادئ الورشة الثمانية (وضوح التسمية، البساطة، التنظيم، المهمة الواحدة، DRY، التعليقات الهادفة، الاتساق، قابلية الصيانة) ويقترح الإصلاح.
   Checks any Python function against the workshop's 8 clean-code principles and suggests fixes.
3. **دليل خطوات الحل الست | 6-step problem solver** — فهم ← تفكيك ← خوارزمية ← أداة ← كود ← اختبار، مع مثال الورشة نفسه: نظام حجز مواعيد عيادة بأولوية حسب الحالة والعمر.
4. **دليل لغات البرمجة | Language guide** — التصنيف (منخفضة/عالية المستوى، وبحسب الاستخدام)، والتاريخ (لغة الآلة ← التجميعية ← C ← C++ ← الويب ← السحابة والجوال)، وقاعدة «لا توجد أفضل لغة مطلقًا» — مع مقترح لغة حسب هدفك.
5. **فحص نوع المبرمج | Programmer self-check** — الناقل / الحافظ / الماهر: ستة أسئلة تعرف بها أين تقف وكيف تصبح «الماهر»، مع قواعد استخدام الذكاء الاصطناعي شريكًا لا بديلًا عن الفهم.
6. **تحديات المبرمجين | Challenges & tips** — التحديات الخمسة من الورشة (تشتت المصادر، التنقل بين الكورسات دون تطبيق، حفظ الأوامر دون منطق، الأدوات قبل الأساس، الخوف من الأخطاء) مع نصيحة عملية لكل تحدٍّ.

## التشغيل | Run it

لا حاجة لتثبيت أي شيء — مكتبة Python القياسية فقط. No dependencies — Python standard library only.

```bash
python3 main.py            # القائمة التفاعلية | interactive menu
python3 main.py --demo     # العرض الكامل | full demo
python3 main.py --test     # الفحص الشامل | full test suite
```

واجهة ويب اختيارية (تحتاج Streamlit): `streamlit run app_streamlit.py`
Optional web UI (needs Streamlit): `streamlit run app_streamlit.py`

يتطلب Python 3.8+. تشغيل أكواد C++ المولَّدة يحتاج `g++` (اختياري — التوليد يعمل بدونه).
Requires Python 3.8+. Running the generated C++ needs `g++` (optional — generation works without it).

## بنية المشروع | Structure

```
algo-lab/
├── main.py                  # نقطة الدخول | entry point
├── app_streamlit.py         # واجهة ويب اختيارية | optional web UI
├── algo_lab/
│   ├── workbench.py         # محرك شبه الكود والمنضدة (العملية الأصلية)
│   ├── cpp_gen.py           # توليد C++ وتجميعه وتشغيله
│   ├── languages.py         # دليل اللغات والتاريخ والمقترح
│   ├── selfcheck.py         # فحص نوع المبرمج
│   ├── challenges.py        # التحديات الخمسة ونصائحها
│   └── cli.py               # القائمة التفاعلية
└── tests/
    └── test_algo_lab.py     # الفحص الشامل (42 فحصًا)
```

## المصدر | Source

- ورشة 5 «البرمجة ولغات البرمجة»، م. مفضّل عبد الملك الشرعبي، شِراع 2026، 11 نوفمبر 2026.
- الملخص الكامل والتطبيق العملي الأصلي محفوظان في مساحة شِراع.
- Workshop 5 «Programming and Programming Languages», Eng. Mufaddal Al-Sharabi, SHIRAA 2026, 11 Nov 2026.

## الرخصة | License

MIT — وليد شمهان (Waleed Shamhan), 2026.
