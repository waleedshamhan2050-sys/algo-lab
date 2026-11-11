#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
توليد كود C++ من شبه الكود العربي — ورشة شِراع 5 (البرمجة ولغات البرمجة).
Generate C++ from the Arabic pseudocode parsed by workbench.py.

المنطق واحد في كل اللغات، ولا يختلف إلا الصياغة (Syntax) — لذلك نفس
الخطوات المُحلَّلة تُترجَم إلى Python (في workbench.py) وإلى C++ هنا،
وهي لغة أمثلة الورشة نفسها (جمع عددين بلغة C++: ‏a=5 وb=10 وSUM=a+b).

ملاحظة عن الأسماء: شبه الكود يستخدم أسماء عربية أحيانًا (مثل «الدرجة»)،
وأسماء C++ في أمثلة الورشة لاتينية — لذلك تُترجَم الأسماء العربية إلى
أسماء لاتينية مكافئة عند توليد C++ (الدرجة ← grade)؛ ويُوثَّق التحويل
في تعليق أعلى الكود المولَّد.
"""
import re
import subprocess
import tempfile

from .workbench import EXAMPLE_HELLO, EXAMPLE_PASS, EXAMPLE_SUM, parse_pseudocode

# أسماء عربية تظهر في أمثلة الورشة ← مقابلها اللاتيني في C++
NAME_MAP = {
    "الدرجة": "grade",
    "المجموع": "total",
    "العدد": "number",
    "العداد": "i",
    "الناتج": "result",
    "القيمة": "value",
}

_ARABIC_WORD = re.compile(r"[\u0600-\u06FF]+")


def _translate_names(text):
    """يستبدل الأسماء العربية المعروفة بمقابلها اللاتيني داخل تعبير أو شرط."""
    def repl(match):
        return NAME_MAP.get(match.group(0), match.group(0))

    return _ARABIC_WORD.sub(repl, text)


def _expr(value):
    """تعبير قابل للطباعة في C++: سلسلة نصية بين علامتي اقتباس تُبقى كما هي،
    وغيرها يُترجَم (أسماء عربية ← لاتينية)."""
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value
    return _translate_names(value)


def _cpp_lines(steps, indent, declared):
    """سطور C++ من الخطوات، مع تتبّع المتغيرات المُصرَّح بها."""
    out = []
    pad = "    " * indent
    for st in steps:
        kind = st[0]
        if kind == "start":
            out.append(pad + "// بداية الخوارزمية")
        elif kind == "end":
            out.append(pad + "// نهاية الخوارزمية")
        elif kind == "read":
            var = _translate_names(st[1])
            if var not in declared:
                out.append(pad + f"int {var};")
                declared.add(var)
            out.append(pad + f"std::cin >> {var};")
        elif kind == "print":
            out.append(pad + f"std::cout << {_expr(st[1])} << std::endl;")
        elif kind == "assign":
            var = _translate_names(st[1])
            expr = _translate_names(st[2])
            if var not in declared:
                out.append(pad + f"auto {var} = {expr};")
                declared.add(var)
            else:
                out.append(pad + f"{var} = {expr};")
        elif kind == "if":
            out.append(pad + f"if ({_translate_names(st[1])}) {{")
            out += _cpp_lines(st[2], indent + 1, declared)
            if st[3]:
                out.append(pad + "} else {")
                out += _cpp_lines(st[3], indent + 1, declared)
            out.append(pad + "}")
        elif kind == "while":
            out.append(pad + f"while ({_translate_names(st[1])}) {{")
            out += _cpp_lines(st[2], indent + 1, declared)
            out.append(pad + "}")
    return out


def to_cpp(pseudocode_text):
    """يترجم شبه كود عربي إلى برنامج C++ كامل (قابل للتجميع)."""
    steps = parse_pseudocode(pseudocode_text)
    body = _cpp_lines(steps, 2, set())
    program = ["#include <iostream>", "", "int main() {"]
    program += body
    program += ["    return 0;", "}"]
    return "\n".join(program) + "\n"


def cpp_with_note(pseudocode_text):
    """البرنامج مع تعليق يشرح تحويل الأسماء العربية (إن وُجدت)."""
    used = sorted({w for w in _ARABIC_WORD.findall(pseudocode_text)
                   if w in NAME_MAP})
    program = to_cpp(pseudocode_text)
    if used:
        note = "// الأسماء العربية في شبه الكود تُرجمت هكذا في C++: " + ", ".join(
            f"{w} ← {NAME_MAP[w]}" for w in used)
        return note + "\n" + program
    return program


def run_cpp(source, inputs):
    """يُجمّع كود C++ بـ g++ ويشغّله بالمدخلات المعطاة، ويعيد ما طُبع.
    يرفع RuntimeError إن لم يوجد g++ أو فشل التجميع."""
    with tempfile.TemporaryDirectory() as tmp:
        src = f"{tmp}/prog.cpp"
        exe = f"{tmp}/prog"
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(source)
        gcc = subprocess.run(["g++", "-std=c++17", "-o", exe, src],
                             capture_output=True, text=True)
        if gcc.returncode != 0:
            raise RuntimeError(f"فشل تجميع C++:\n{gcc.stderr}")
        stdin = "\n".join(str(v) for v in inputs)
        if stdin:
            stdin += "\n"
        run = subprocess.run([exe], input=stdin, capture_output=True,
                             text=True, timeout=10)
        if run.returncode != 0:
            raise RuntimeError(f"فشل تشغيل C++ (خرج {run.returncode}):\n"
                               f"{run.stderr}")
        return run.stdout


# أمثلة الورشة الثلاثة جاهزة بكود C++ (للعرض والاختبار)
CPP_EXAMPLES = {
    "sum": to_cpp(EXAMPLE_SUM),
    "pass": cpp_with_note(EXAMPLE_PASS),
    "hello": to_cpp(EXAMPLE_HELLO),
}
