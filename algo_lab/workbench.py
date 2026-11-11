#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
منضدة الخوارزميات — التطبيق العملي لورشة 5 (البرمجة ولغات البرمجة)
Algorithm Workbench — SHIRAA Workshop 5

يطبّق محاور الورشة الأربعة على أمثلتها نفسها:
  1. شبه الكود (Pseudocode): اكتب الخوارزمية بالعربية، تُترجم إلى Python
     وتُنفَّذ فعليًا — الأمثلة الثلاثة من الورشة: جمع عددين، نجاح/رسوب
     طالب، وطباعة «مرحبًا» 3 مرات بحلقة WHILE.
  2. مخططات التدفق (Flowcharts): نفس الخوارزمية تُرسم بأشكال الورشة
     (بيضاوي للبداية/النهاية، متوازي أضلاع للإدخال/الإخراج، مستطيل
     للعمليات، معيّن للقرار).
  3. الكود النظيف: فاحص يطبّق مبادئ الورشة الثمانية على أي كود Python.
  4. خطوات حل المشكلات الست: مخطط جاهز يبني خطة أي مشكلة
     (فهم ← تفكيك ← خوارزمية ← أداة ← كود ← اختبار).

مكتبة Python القياسية فقط — لا مفاتيح، لا إنترنت، لا حسابات.

    python3 algo_workbench.py            # تفاعلي: جرّب أمثلة الورشة
    python3 algo_workbench.py --demo     # العرض الكامل (الأمثلة الثلاثة
                                           # + مخطط التدفق + فحص الكود النظيف
                                           # + خطة العيادة بخطواتها الست)
    python3 algo_workbench.py --test     # فحص ذاتي
"""
import ast
import contextlib
import io
import re
import sys
from collections import Counter

# ---------------------------------------------------------------- أمثلة الورشة
EXAMPLE_SUM = """ابدأ
اقرأ A
اقرأ B
SUM = A + B
اطبع SUM
انتهِ"""

EXAMPLE_PASS = """ابدأ
اقرأ الدرجة
إذا الدرجة >= 50
اطبع "ناجح"
وإلا
اطبع "راسب"
انتهِ إذا
انتهِ"""

EXAMPLE_HELLO = """ابدأ
i = 1
بينما i <= 3
اطبع "مرحبًا"
i = i + 1
انتهِ بينما
انتهِ"""

EXAMPLES = {
    "sum": ("جمع عددين (A=5 ،B=10)", EXAMPLE_SUM, [5, 10]),
    "pass": ("نجاح أو رسوب طالب (الدرجة 70 ثم 40)", EXAMPLE_PASS, [70]),
    "hello": ("طباعة «مرحبًا» 3 مرات (حلقة WHILE)", EXAMPLE_HELLO, []),
}

# ------------------------------------------------------- شبه الكود: التحليل
# اللهجة: سطر لكل خطوة؛ الكتل تُغلق صراحة بـ «انتهِ إذا» / «انتهِ بينما».
# الكلمات: ابدأ / انتهِ / اقرأ X / اطبع X / X = تعبير / إذا شرط / وإلا /
#          انتهِ إذا / بينما شرط / انتهِ بينما. الأسماء العربية مسموحة.


def parse_pseudocode(text):
    """يحلّل شبه الكود إلى خطوات متداخلة. يرفع ValueError لسطر غير مفهوم."""
    lines = [ln.strip() for ln in text.strip().splitlines()]
    steps, _ = _parse_block(lines, 0, ())
    return steps


def _parse_block(lines, i, stop):
    steps = []
    while i < len(lines):
        raw = lines[i]
        if not raw:
            i += 1
            continue
        if raw in stop:
            return steps, i
        if raw == "ابدأ":
            steps.append(("start",))
            i += 1
        elif raw == "انتهِ":
            steps.append(("end",))
            i += 1
        elif raw.startswith("اقرأ "):
            steps.append(("read", raw[5:].strip()))
            i += 1
        elif raw.startswith("اطبع "):
            steps.append(("print", raw[5:].strip()))
            i += 1
        elif raw.startswith("إذا "):
            cond = raw[4:].strip()
            then, i = _parse_block(lines, i + 1, ("وإلا", "انتهِ إذا"))
            els = []
            if i < len(lines) and lines[i] == "وإلا":
                els, i = _parse_block(lines, i + 1, ("انتهِ إذا",))
            i += 1  # استهلاك «انتهِ إذا»
            steps.append(("if", cond, then, els))
        elif raw.startswith("بينما "):
            cond = raw[6:].strip()
            body, i = _parse_block(lines, i + 1, ("انتهِ بينما",))
            i += 1  # استهلاك «انتهِ بينما»
            steps.append(("while", cond, body))
        elif "=" in raw:
            var, expr = raw.split("=", 1)
            steps.append(("assign", var.strip(), expr.strip()))
            i += 1
        else:
            raise ValueError(f"سطر غير مفهوم في شبه الكود: {raw!r}")
    return steps, i


def to_python(steps, indent=0):
    """يترجم الخطوات إلى كود Python (المنطق واحد، وتختلف الصياغة فقط)."""
    out = []
    pad = "    " * indent
    for st in steps:
        kind = st[0]
        if kind == "start":
            out.append(pad + "# بداية الخوارزمية")
        elif kind == "end":
            out.append(pad + "# نهاية الخوارزمية")
        elif kind == "read":
            out.append(f"{pad}{st[1]} = _read()")
        elif kind == "print":
            out.append(f"{pad}print({st[1]})")
        elif kind == "assign":
            out.append(f"{pad}{st[1]} = {st[2]}")
        elif kind == "if":
            out.append(f"{pad}if {st[1]}:")
            out += to_python(st[2], indent + 1)
            if st[3]:
                out.append(pad + "else:")
                out += to_python(st[3], indent + 1)
        elif kind == "while":
            out.append(f"{pad}while {st[1]}:")
            out += to_python(st[2], indent + 1)
    return out


def run_pseudocode(text, inputs):
    """ينفّذ شبه الكود بقائمة مدخلات، ويعيد ما طُبع (نصًا)."""
    steps = parse_pseudocode(text)
    source = "\n".join(to_python(steps))
    queue = list(inputs)

    def _read():
        if not queue:
            raise ValueError("نفدت المدخلات: الخوارزمية طلبت قراءة بلا قيمة")
        return queue.pop(0)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(source, {"_read": _read})
    return buf.getvalue()


# --------------------------------------------------- مخطط التدفق (ASCII)
def flowchart(steps, indent=0):
    """يرسم مخطط التدفق بأشكال الورشة: () بداية/نهاية، // إدخال/إخراج،
    [] عملية، ◇ قرار."""
    lines = []
    pad = "  " * indent
    for st in steps:
        kind = st[0]
        if kind == "start":
            lines.append(f"{pad}( ابدأ )")
        elif kind == "end":
            lines.append(f"{pad}( انتهِ )")
        elif kind == "read":
            lines.append(f"{pad}/ اقرأ {st[1]} /")
        elif kind == "print":
            lines.append(f"{pad}/ اطبع {st[1]} /")
        elif kind == "assign":
            lines.append(f"{pad}[ {st[1]} = {st[2]} ]")
        elif kind == "if":
            lines.append(f"{pad}◇ {st[1]} ؟")
            lines.append(f"{pad}  ├─ نعم:")
            lines += flowchart(st[2], indent + 2)
            if st[3]:
                lines.append(f"{pad}  └─ لا:")
                lines += flowchart(st[3], indent + 2)
        elif kind == "while":
            lines.append(f"{pad}◇ {st[1]} ؟  (حلقة)")
            lines += flowchart(st[2], indent + 1)
            lines.append(f"{pad}  ↺ عودة إلى الشرط")
    return lines


# ------------------------------------------------------- الكود النظيف: الفاحص
# كل مبدأ من الثمانية يُفحص بما يمكن قياسه آليًا؛ ما لا يُقاس يُذكَّر به
# في التقرير لا أن يُدَّعى فحصه (مثلاً: «اشرح لماذا» لا يفحصها آلي.
PRINCIPLES = {
    1: "وضوح التسمية بأسماء ذات معنى",
    2: "البساطة (اختر الحل الأبسط)",
    3: "التنظيم",
    4: "المهمة الواحدة لكل دالة",
    5: "عدم التكرار DRY",
    6: "التعليقات الهادفة (اشرح «لماذا» لا «كيف»)",
    7: "الاتساق في التسمية والأسلوب",
    8: "قابلية الصيانة",
}

MESSY_SAMPLE = '''def f(x, y):  # هذه الدالة تجمع
    a = x + y
    print(a)
    b = x + y
    print(b)
    c = x + y
    print(c)
    totalPrice = x * 2
    total_price = y * 3
    if a >= 50:
        return a
    return 0
'''

CLEAN_SAMPLE = '''"""وحدة حساب درجات الطلاب — مثال نظيف من مبادئ الورشة."""

PASS_THRESHOLD = 50


def add_scores(first_score, second_score):
    """يجمع درجتين ويعيد المجموع."""
    return first_score + second_score


def is_passing(total_score):
    """هل المجموع ناجح؟ يقارن بعتبة النجاح المسمّاة."""
    return total_score >= PASS_THRESHOLD


def report(total_score):
    """يطبع النتيجة فقط — الحساب في دالة أخرى (مهمة واحدة)."""
    print("ناجح" if is_passing(total_score) else "راسب")
'''


def check_clean_code(source):
    """يفحص كود Python ويعيد قائمة ملاحظات (رقم المبدأ، المستوى، الرسالة).
    الملاحظات اقتراحات تعليمية — القرار النهائي للإنسان دائمًا."""
    findings = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if len(node.id) == 1 and node.id not in ("i", "j", "k", "_"):
                findings.append((1, "FLAG",
                                 f"اسم من حرف واحد: {node.id!r} — سمِّه باسم ذي معنى"))
        if isinstance(node, ast.FunctionDef):
            span = node.end_lineno - node.lineno + 1
            if span > 15:
                findings.append((2, "FLAG",
                                 f"الدالة {node.name!r} طويلة ({span} سطرًا) — قسّمها إلى دوال أصغر"))
            if not ast.get_docstring(node):
                findings.append((8, "FLAG",
                                 f"الدالة {node.name!r} بلا docstring — وثّق ماذا تفعل ولماذا"))
            calls = [n.func.id for n in ast.walk(node)
                     if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
            has_io = any(c in ("print", "input") for c in calls)
            has_calc = any(isinstance(n, ast.BinOp) for n in ast.walk(node))
            if has_io and has_calc:
                findings.append((4, "FLAG",
                                 f"الدالة {node.name!r} تجمع إدخال/إخراج وحسابًا — افصل المهمتين"))
    lines = [ln.strip() for ln in source.splitlines()
             if ln.strip() and not ln.strip().startswith("#")]
    for line, n in Counter(lines).items():
        if n >= 2 and len(line) > 3:
            findings.append((5, "FLAG",
                             f"سطر مكرر {n} مرات (DRY): {line!r} — ضعه في دالة واستدعِها"))
    for raw in source.splitlines():
        if "#" in raw:
            code, _, comment = raw.partition("#")
            code, comment = code.strip(), comment.strip()
            if code and comment and comment in code:
                findings.append((6, "FLAG",
                                 f"تعليق يكرر الكود: {comment!r} — اشرح «لماذا» لا «كيف»"))
    names = [n.id for n in ast.walk(tree) if isinstance(n, ast.Name)]
    camel = [n for n in names if re.search(r"[a-z][A-Z]", n)]
    snake = [n for n in names if "_" in n and n.islower()]
    if camel and snake:
        findings.append((7, "FLAG",
                         f"خلط بين camelCase ({camel[0]!r}) وsnake_case ({snake[0]!r}) — وحّد الأسلوب"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for c in node.comparators:
                if (isinstance(c, ast.Constant) and isinstance(c.value, (int, float))
                        and c.value not in (0, 1)):
                    findings.append((8, "FLAG",
                                     f"رقم سحري {c.value} في مقارنة — ضعه في ثابت مسمّى"))
    return findings


def clean_code_report(source, title):
    """تقرير مقروء لفحص الكود النظيف."""
    findings = check_clean_code(source)
    out = [f"--- فحص الكود النظيف: {title} ---"]
    if not findings:
        out.append("✅ نظيف: لا ملاحظات على المبادئ الثمانية القابلة للفحص.")
    for num, _, msg in findings:
        out.append(f"⚠️  المبدأ {num} ({PRINCIPLES[num]}): {msg}")
    out.append("تذكير: المبادئ 2 و3 تُقاس جزئيًا هنا؛ راجع كودك بنفسك للبساطة والتنظيم.")
    return "\n".join(out), findings


# ------------------------------------------- خطوات حل المشكلات الست (الورشة)
CLINIC_PLAN = {
    "name": "نظام حجز مواعيد عيادة (مثال الورشة)",
    "inputs": "بيانات المريض (الاسم، العمر، الحالة)، والمواعيد المتاحة",
    "outputs": "موعد محدد بأولوية حسب الحالة والعمر، يُحجز من البيت بوقت محدد",
    "constraints": "موعد واحد لكل مريض؛ الأولوية للحالات الحرجة وكبار السن؛ لا حجز مكرر لنفس الموعد",
    "subproblems": [
        "تسجيل بيانات المريض",
        "حساب أولوية المريض من الحالة والعمر",
        "عرض المواعيد المتاحة",
        "تأكيد الحجز وحفظه",
    ],
    "algorithm": ("ابدأ ← اقرأ بيانات المريض ← احسب الأولوية ← اعرض المواعيد المتاحة\n"
                  "← إذا اختار المريض موعدًا متاحًا فاحجزه واطبع التأكيد وإلا اعرض بديلًا ← انتهِ"),
    "tool": "Python أولًا (نسخة طرفية)، ثم واجهة ويب حين يثبت المنطق",
    "tests": [
        "حجز مريض عادي في موعد متاح ← يُحجَز ويُطبَع التأكيد",
        "مريض حرج بعد مريض عادي ← يتقدم في الأولوية",
        "محاولة حجز موعد محجوز ← يُرفَض ويُعرَض بديل",
    ],
}


def six_step_plan(p):
    """يبني خطة حل مشكلة بخطوات الورشة الست من وصف مختصر."""
    lines = [
        f"=== خطة حل المشكلة: {p['name']} ===",
        f"الخطوة 1 — الفهم الكامل: المدخلات: {p['inputs']}؛ المخرجات: {p['outputs']}؛ القيود: {p['constraints']}.",
        "الخطوة 2 — التفكيك إلى مشكلات صغيرة:",
    ]
    lines += [f"   - {s}" for s in p["subproblems"]]
    lines.append(f"الخطوة 3 — التخطيط وبناء خوارزمية: {p['algorithm']}")
    lines.append(f"الخطوة 4 — اختيار الأداة/اللغة: {p['tool']}")
    lines.append("الخطوة 5 — كتابة الكود: اكتب الخوارزمية شبه كود أولًا، ثم ترجمها (جرّبها في منضدة الخوارزميات).")
    lines.append("الخطوة 6 — الاختبار وتصحيح الأخطاء:")
    lines += [f"   - {t}" for t in p["tests"]]
    return "\n".join(lines)


# ------------------------------------------------------------------ العرض
def demo():
    """العرض الكامل: الأمثلة الثلاثة + مخطط تدفق + فحص الكود + خطة العيادة."""
    parts = ["=== منضدة الخوارزميات — ورشة 5: البرمجة ولغات البرمجة ==="]
    for key in ("sum", "pass", "hello"):
        title, pseudo, inputs = EXAMPLES[key]
        steps = parse_pseudocode(pseudo)
        code = "\n".join(to_python(steps))
        if key == "pass":
            out = run_pseudocode(pseudo, [70]) + run_pseudocode(pseudo, [40])
        else:
            out = run_pseudocode(pseudo, inputs)
        parts.append(f"\n--- {title} ---")
        parts.append("شبه الكود:\n" + pseudo)
        parts.append("ترجمته إلى Python:\n" + code)
        parts.append("الناتج عند التشغيل:\n" + out.rstrip())
    parts.append("\n--- مخطط التدفق: جمع عددين ---")
    parts.append("\n".join(flowchart(parse_pseudocode(EXAMPLE_SUM))))
    parts.append("\n--- مخطط التدفق: نجاح أو رسوب ---")
    parts.append("\n".join(flowchart(parse_pseudocode(EXAMPLE_PASS))))
    report, _ = clean_code_report(MESSY_SAMPLE, "كود فوضوي (قبل)")
    parts.append("\n" + report)
    report, _ = clean_code_report(CLEAN_SAMPLE, "كود نظيف (بعد)")
    parts.append("\n" + report)
    parts.append("\n" + six_step_plan(CLINIC_PLAN))
    parts.append("\nقاعدة الورشة: المنطق واحد في كل اللغات، ولا يختلف إلا الصياغة "
                 "(Syntax) — من أتقن الخوارزمية انتقل بين اللغات في أيام.")
    return "\n".join(parts)


def run_tests():
    """الفحص الذاتي: مخرجات الأمثلة الثلاثة + المخطط + فاحص الكود + الخطة."""
    ok = True

    def check(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print(f"{'✅' if good else '❌'} {name}: {got!r}"
              + ("" if good else f" (المتوقع {want!r})"))
        return good

    check("جمع عددين 5+10", run_pseudocode(EXAMPLE_SUM, [5, 10]), "15\n")
    check("نجاح (70)", run_pseudocode(EXAMPLE_PASS, [70]), "ناجح\n")
    check("رسوب (40)", run_pseudocode(EXAMPLE_PASS, [40]), "راسب\n")
    check("مرحبًا ×3", run_pseudocode(EXAMPLE_HELLO, []),
          "مرحبًا\nمرحبًا\nمرحبًا\n")
    fc = "\n".join(flowchart(parse_pseudocode(EXAMPLE_SUM)))
    check("مخطط التدفق فيه [ SUM = A + B ]", "[ SUM = A + B ]" in fc, True)
    check("مخطط التدفق فيه / اطبع SUM /", "/ اطبع SUM /" in fc, True)
    fc2 = "\n".join(flowchart(parse_pseudocode(EXAMPLE_PASS)))
    check("مخطط القرار فيه ◇", "◇ الدرجة >= 50 ؟" in fc2, True)
    messy = check_clean_code(MESSY_SAMPLE)
    check("الكود الفوضوي عليه ملاحظات (≥5)", len(messy) >= 5, True)
    clean = check_clean_code(CLEAN_SAMPLE)
    check("الكود النظيف بلا ملاحظات", clean, [])
    plan = six_step_plan(CLINIC_PLAN)
    check("الخطة فيها الخطوات الست",
          all(f"الخطوة {n}" in plan for n in range(1, 7)), True)
    code = "\n".join(to_python(parse_pseudocode(EXAMPLE_SUM)))
    check("الترجمة فيها SUM = A + B", "SUM = A + B" in code, True)
    print(f"\n=== النتيجة: {'PASS' if ok else 'FAIL'} ===")
    return ok


def interactive():
    print("منضدة الخوارزميات — أمثلة ورشة 5 (اكتب رقمًا أو 'خروج'):")
    for i, key in enumerate(("sum", "pass", "hello"), 1):
        print(f"  {i}  {EXAMPLES[key][0]}")
    while True:
        try:
            choice = input("اختر مثالًا (1/2/3) أو 'خروج': ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if choice in ("خروج", "exit", "quit", ""):
            break
        key = {"1": "sum", "2": "pass", "3": "hello"}.get(choice)
        if not key:
            print("اختر 1 أو 2 أو 3.")
            continue
        title, pseudo, inputs = EXAMPLES[key]
        print(f"\n--- {title} ---\nشبه الكود:\n{pseudo}")
        print("مخطط التدفق:\n" + "\n".join(flowchart(parse_pseudocode(pseudo))))
        if key == "pass":
            grades = input("أدخل درجة للتجربة (Enter = 70 ثم 40): ").strip()
            ins = [int(grades)] if grades else [70]
            print("الناتج:\n" + run_pseudocode(pseudo, ins).rstrip())
            if not grades:
                print("والدرجة 40:\n" + run_pseudocode(pseudo, [40]).rstrip())
        else:
            print("الناتج:\n" + run_pseudocode(pseudo, inputs).rstrip())
    print("إلى اللقاء — ابدأ بالورقة والقلم، وابنِ الخوارزمية قبل الكود.")


def main():
    args = sys.argv[1:]
    if "--test" in args:
        sys.exit(0 if run_tests() else 1)
    if "--demo" in args:
        print(demo())
        return
    interactive()


if __name__ == "__main__":
    main()
