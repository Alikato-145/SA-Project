"""Refresh only current model sections; never rebuild from the old rubric source."""
from pathlib import Path
import json
import re
import textwrap

R = Path(__file__).resolve().parent
E = R / "evidence"


def table(headers, rows):
    def cell(value):
        return str(value).replace("|", "/").replace("\n", "; ")
    return "| " + " | ".join(headers) + " |\n|" + "---|" * len(headers) + "\n" + "".join("| " + " | ".join(cell(v) for v in row) + " |\n" for row in rows)


def main():
    path = R / "README.md"
    s = path.read_text()
    model = json.loads((E / "sql/current20-model.json").read_text())
    old = json.loads((E / "sql/verified-queries.json").read_text())
    snapshot = json.loads((R.parent.parent / "backend/drizzle/meta/0006_snapshot.json").read_text())
    tables = {t["name"]: t for t in model["tables"]}
    assert len(tables) == 39 and model["foreignKeys"] == 91 and len(model["enums"]) == 25 and model["migrations"] == 7
    # The current editorial source is the input; no old-source reset or private backup dependency.
    original = s
    entity_meanings = {}
    for match in re.finditer(r"##### 3\.5\.4\.\d+ (\w+) Table\n(.*?)(?=\n##### 3\.5\.4\.\d+ |\n### 3\.6 |\Z)", original, re.S):
        entity_meanings[match[1]] = {m[1]: m[4] for m in re.finditer(r"^\| `([^`]+)` \| `([^`]+)` \| ([^|]+) \| ([^|]+) \|$", match[2], re.M)}
    meanings = {}
    meanings.update({
        "payment_method": "ช่องทางรับเงินที่ลงทะเบียน แยกจากหมายเลขติดต่อ",
        "promptpay_phone": "หมายเลขโทรศัพท์ผู้รับ PromptPay ที่ลงทะเบียน ไม่ใช่ contact phone",
        "is_social_security_member": "สถานะสมาชิกประกันสังคมตามช่วงการจ้าง",
        "is_social_security_member_snapshot": "สถานะสมาชิกที่เก็บเมื่อคำนวณและล็อกงวด",
        "social_security_base_snapshot": "ผลรวมฐานเงินเดือนรายวันที่ได้รับจริง ไม่รวมสวัสดิการ OT หรือรายการปรับ",
        "branch_id_snapshot": "สาขาประวัติของรายการจ่ายจากผลเงินเดือนที่ล็อก",
        "promptpay_phone_snapshot": "โทรศัพท์ผู้รับที่ถูกตรึงเมื่อเตรียมจ่าย ไม่แสดงค่าในรายงานตัวอย่าง",
        "account_number_ciphertext_snapshot": "เลขบัญชีเข้ารหัสที่ตรึงเมื่อเตรียมจ่าย ไม่แสดงค่า",
        "account_number_last4_snapshot": "เลขบัญชีท้ายสี่หลักสำหรับแสดงอย่างจำกัด",
        "account_holder_name_snapshot": "ชื่อผู้รับที่ตรึงเมื่อเตรียมจ่าย",
        "bank_code_snapshot": "รหัสธนาคารที่ตรึงเมื่อเตรียมจ่าย",
        "token_hash": "fingerprint สำหรับตรวจเพิกถอน session ไม่เก็บหรือแสดง token ดิบ",
        "revoked_at": "เวลาเพิกถอน session",
        "expires_at": "เวลาสิ้นอายุ session ที่เพิกถอน",
        "loan_id": "เงินกู้และแผนผ่อนที่สร้างเมื่ออนุมัติคำขอ",
        "reference_no": "เลขอ้างอิงที่เจ้าหน้าที่ระบุเมื่อยืนยันผลจ่ายภายนอก",
        "cancellation_reason": "เหตุผลยกเลิกรายการเตรียมจ่าย",
        "prepared_at": "เวลาตรึงรายการและปลายทางจ่าย",
        "prepared_by_user_account_id": "บัญชีเจ้าหน้าที่เตรียมจ่าย",
        "paid_at": "เวลาเจ้าหน้าที่ยืนยันผลจ่ายด้วยตนเอง ไม่ใช่ผลธนาคารอัตโนมัติ",
        "paid_by_user_account_id": "บัญชีเจ้าหน้าที่ยืนยันการจ่าย",
        "cancelled_at": "เวลายกเลิกรายการเตรียมจ่าย",
        "cancelled_by_user_account_id": "บัญชีเจ้าหน้าที่ยกเลิกรายการ",
    })
    descriptions = {"loan_requests": "คำขอเงินกู้และผลพิจารณา; อนุมัติจึงสร้างเงินกู้และแผนผ่อน", "payroll_payments": "รายการเตรียมจ่าย snapshot และสถานะการยืนยันหรือยกเลิก; ประวัติเพิ่มรายการอยู่ใน audit_logs", "revoked_session_tokens": "ประวัติเพิกถอน session สำหรับปฏิเสธ token ที่ออกจากระบบแล้ว"}
    refs = []
    for name, meta in tables.items():
        for constraint in meta["constraints"]:
            m = re.match(r"FOREIGN KEY \(([^)]+)\) REFERENCES (\w+)\(([^)]+)\)", constraint["definition"])
            if m:
                refs.append((name, *m.groups()))
    assert len(refs) == len(set(refs)) == 91

    def dictionary(name):
        meta = tables[name]
        snap = snapshot["tables"][f"public.{name}"]
        unique_columns = {index["columns"][0]["expression"] for index in snap["indexes"].values() if index["isUnique"] and not index.get("where") and len(index["columns"]) == 1}
        rows = []
        for c in meta["columns"]:
            keys = ["PK"] if c["pk"] else []
            keys += [f"FK → `{parent}`" for child, col, parent, _ in refs if child == name and col == c["name"]]
            if c["unique"] or c["name"] in unique_columns: keys.append("UQ")
            if c["notNull"] and not c["pk"]: keys.append("NN")
            new_meanings = {"id": "รหัสระเบียน", "employee_id": "พนักงานเจ้าของคำขอ", "principal_amount": "เงินต้นที่ขอกู้", "installment_count": "จำนวนงวดผ่อน 1–5 งวด", "status": "สถานะคำขอหรือรายการจ่ายตาม enum", "requested_by_user_account_id": "บัญชีผู้ยื่นคำขอ", "requested_at": "เวลายื่นคำขอ", "decided_by_user_account_id": "บัญชีผู้พิจารณาคำขอ", "decided_at": "เวลาบันทึกผลพิจารณา", "decision_note": "หมายเหตุการพิจารณา; การปฏิเสธต้องมีเหตุผล", "payroll_record_id": "ผลเงินเดือนที่ล็อกแล้วซึ่งเป็นต้นทางการจ่าย", "amount": "ยอดจ่ายที่ตรึงจากผลเงินเดือน", "created_at": "เวลาสร้างระเบียน", "updated_at": "เวลาแก้ไขระเบียนล่าสุด"}
            meaning = meanings.get(c["name"], new_meanings.get(c["name"], c["name"].replace("_", " ")) if name in descriptions else entity_meanings.get(name, {}).get(c["name"], c["name"].replace("_", " ")))
            if name == "revoked_session_tokens" and c["name"] == "user_account_id": meaning = "บัญชีผู้ใช้ที่ session ถูกเพิกถอน"
            if name == "advance_requests" and c["name"] == "reason": meaning = "เหตุผลคำขอใหม่บังคับ trimmed nonblank 1–1000 ตัวอักษร; legacy คง NULL"
            if name == "loan_requests" and c["name"] == "reason": meaning = "เหตุผลคำขอเงินกู้ ต้องมีค่าตามข้อกำหนด schema"
            rows.append([f'`{c["name"]}`', f'`{c["type"]}`', ", ".join(keys) or "—", meaning])
        result = table(["คอลัมน์", "ชนิดข้อมูล", "คีย์/ข้อกำหนด", "ความหมาย"], rows)
        return result

    def validation(name):
        rows = []
        for c in tables[name]["columns"]:
            rules = ["NOT NULL" if c["notNull"] else "nullable"]
            if c["unique"]: rules.append("UNIQUE")
            if c["enumValues"]: rules.append("enum: " + ", ".join(c["enumValues"]))
            if c["type"].startswith("numeric"): rules.append("exact decimal; ไม่ใช้ float")
            if c["type"] == "date": rules.append("ISO business date")
            if "time zone" in c["type"]: rules.append("timezone-aware timestamp")
            rules += [k["definition"] for k in tables[name]["constraints"] if k["kind"] == "c" and re.search(r"\b" + re.escape(c["name"]) + r"\b", k["definition"])]
            if name == "advance_requests" and c["name"] in ("reason", "decision_note"):
                rules.append("new reason / rejection note: trimmed nonblank, input length 1–1000; legacy NULL preserved")
            rows.append([c["name"], "; ".join(rules)])
        return table(["Attribute", "Validation / range"], rows)

    # Retain each existing table's surrounding prose and real historic sample evidence.
    for name in tables:
        pattern = rf"(##### 3\.5\.4\.\d+ {name} Table\n.*?)(?=\n##### 3\.5\.4\.\d+ |\n### 3\.6 |\Z)"
        m = re.search(pattern, s, re.S)
        if not m: continue
        b = m[1]
        b = re.sub(r"\| คอลัมน์ \| ชนิดข้อมูล \| คีย์/ข้อกำหนด \| ความหมาย \|\n(?:\|[^\n]*\n)+", lambda _: dictionary(name), b)
        b = re.sub(r"\| Attribute \| Validation / range \|\n(?:\|[^\n]*\n)+", lambda _: validation(name), b)
        # Partial unique indexes constrain only qualifying rows, never global cardinality.
        b = re.sub(r"\n\*\*Partial unique indexes.*?(?=\n\*\*|\n#####|\Z)", "\n", b, flags=re.S)
        partial = [index for index in tables[name]["indexes"] if "CREATE UNIQUE INDEX" in index["definition"] and " WHERE " in index["definition"]]
        if partial:
            note = "\n**Partial unique indexes — เฉพาะแถวที่เข้าเงื่อนไข ไม่ใช่ global UQ/1:1**\n\n" + table(["Index", "Columns", "Predicate"], [[idx["name"], re.search(r"USING \w+ \((.*?)\) WHERE", idx["definition"])[1], idx["definition"].split(" WHERE ", 1)[1]] for idx in partial]) + "\n"
            if name == "payroll_payments": note += "payroll_records 1:N payroll_payments สำหรับประวัติทั้งหมด; มีรายการ prepared หรือ paid ได้ไม่เกินหนึ่งรายการต่อ record\n\n"
            b += note
        s = s[:m.start()] + b + s[m.end():]
    s = s.replace("##### 3.5.4.37 ตัวอย่างข้อมูลประกอบความสัมพันธ์", "##### 3.5.4.40 ตัวอย่างข้อมูลประกอบความสัมพันธ์")
    additions = []
    for number, name, query_id in [(37, "loan_requests", "Q020"), (38, "payroll_payments", "Q021"), (39, "revoked_session_tokens", "Q022")]:
        if re.search(rf"##### 3\.5\.4\.\d+ {name} Table", s): continue
        q = next(e for e in model["entries"] if e["id"] == query_id)
        sample = "ไม่มีตัวอย่าง token หรือ hash เผยแพร่; ตรวจจำนวนที่ยังไม่หมดอายุแบบ aggregate ตาม Q022 เท่านั้น"
        if name != "revoked_session_tokens":
            sample = f"ผลอ่านจริง {len(q['rows'])} ระเบียน (สูงสุด 5) จาก disposable database; ไม่สร้างตัวอย่างแทนข้อมูลที่ไม่มี\n\n"
            sample += table(list(q["rows"][0]), [list(row.values()) for row in q["rows"]]) if q["rows"] else "ตารางยังว่างในชุดตรวจนี้"
        additions.append(f"##### 3.5.4.{number} {name} Table\n\n##### 3.5.4.{number}.1 Data Dictionary ของตาราง {name}\n\n**หน้าที่:** {descriptions[name]}\n\n" + dictionary(name) + "\n**การตรวจค่าและช่วงข้อมูลจาก schema/catalog**\n\n" + validation(name) + "\n**ตัวอย่างข้อมูลที่เปิดเผยได้**\n\n" + sample + "\n")
    s = s.replace("##### 3.5.4.40 ตัวอย่างข้อมูลประกอบความสัมพันธ์", "\n".join(additions) + "\n##### 3.5.4.40 ตัวอย่างข้อมูลประกอบความสัมพันธ์")
    s = re.sub(r"Data Dictionary ในบทนี้ปรับข้อกำหนด.*?(?=\n\n#####)", "Data Dictionary ตรวจตรงกับ executable Drizzle schema และ catalog PostgreSQL 16 ของฐานทดสอบ ณ 26 ตุลาคม 2026 รวม 39 ตาราง 91 FK 25 enums และ migration 7 รายการ หลักฐาน current20-model.json เก็บ metadata และ query ที่ไม่เปิดเผยข้อมูลลับ ไม่มีการแก้ schema จากการปรับรายงาน", s, count=1, flags=re.S)
    # Add the three current entities to all eight existing five-UC CRUD panels.
    crud_end = s.index("### 3.4 ")
    prefix, suffix = s[:crud_end], s[crud_end:]
    def crud_panel(m):
        content = m[0]
        ids = re.findall(r"UC\d{2}", content.splitlines()[0])
        maps = {"loan_requests": {"UC12": "C/R/U", "UC19": "R"}, "payroll_payments": {"UC18": "C/R/U", "UC19": "R"}, "revoked_session_tokens": {"UC01": "C/R"}}
        for name, mapping in maps.items():
            if f"| {name} |" not in content:
                content += "| " + name + " | " + " | ".join(mapping.get(i, "—") for i in ids) + " |\n"
        return content
    prefix = re.sub(r"\| ข้อมูล \| UC\d{2}[^\n]*\n(?:\|[^\n]*\n)+", crud_panel, prefix)
    s = prefix + suffix
    # Exact enum inventory and current catalog queries supplement historical 19 repository queries.
    enum_text = "#### 3.5.5 Enums ของแบบจำลองปัจจุบัน\n\n" + table(["Enum", "ค่าที่รองรับ"], [[e["name"], ", ".join(e["values"])] for e in model["enums"]]) + "\n"
    if "#### 3.5.5 Enums" in s:
        s = re.sub(r"#### 3\.5\.5 Enums.*?(?=### 3\.6 )", lambda _: enum_text, s, flags=re.S)
    else: s = s.replace("### 3.6 Class Diagram", enum_text + "### 3.6 Class Diagram")
    query_rows = "".join("| " + " | ".join([q["id"], ", ".join(q["uc"]), q["name"], "read-only current20 catalog verification"]) + " |\n" for q in model["entries"])
    if "| Q020 |" not in s:
        match = re.search(r"\| Q019 \|[^\n]*\n", s); assert match
        s = s[:match.end()] + query_rows + s[match.end():]
    qtext = "\nคำสั่ง Q020–Q024 เป็น read-only acceptance queries สำหรับแบบจำลองปัจจุบัน รันจริงกับฐานทดสอบแยก และไม่ใช้แทน authorization หรือ business service tests ผลอยู่ใน evidence/sql/current20-model.json; Q001–Q019 ด้านบนคงเป็นหลักฐาน repository เดิม\n\n"
    for q in model["entries"]:
        qtext += f"#### 3.11.{int(q['id'][1:])} {q['id']} {q['name']}\n\nUC: {', '.join(q['uc'])}; ประเภทหลักฐาน: {q['source']}\n\n```sql\n{q['sql']};\n```\n\nBind parameters: `{json.dumps(q['params'], ensure_ascii=False)}`; ผลรัน PASS จำนวน {q['resultCount']} แถว ณ {model['verifiedAt']}\n\n"
    if "#### 3.11.20 Q020" in s:
        start = s.index("คำสั่ง Q020–Q024 เป็น read-only acceptance queries")
        end = s.index("### 3.11.25 ", start)
        s = s[:start] + qtext.lstrip("\n") + s[end:]
    else:
        end = s.index("### 3.12 ") if "### 3.12 " in s else s.index("### 3.13 ") if "### 3.13 " in s else s.index("## บทที่ 4")
        s = s[:end] + qtext + s[end:]
    # Hash values are not needed in public sample evidence.
    s = re.sub(r"\b[a-f0-9]{64}\b", "[ปกปิดค่า hash]", s)
    charts = []
    def graph(name, nodes, edges, shapes=None):
        q = lambda value: json.dumps(str(value), ensure_ascii=False)
        dot = ['digraph G { graph [rankdir=LR,bgcolor="white",pad="0.3",nodesep="0.4",ranksep="0.7",dpi=72];', 'node [shape=box,style="rounded,filled",fillcolor="#f0f7f4",color="#427766",fontname="Tahoma",fontsize=18,margin="0.36,0.16"];', 'edge [fontname="Tahoma",fontsize=15,color="#526e62",arrowsize=0.7];']
        for key, label in nodes.items():
            label = "\n".join("\n".join(textwrap.wrap(line, width=48, break_long_words=False, break_on_hyphens=False)) for line in label.splitlines())
            dot.append(f'{q(key)} [label={q(label)}' + (f',shape={shapes[key]}' if shapes and key in shapes else '') + '];')
        for a, b, label in edges: dot.append(f'{q(a)} -> {q(b)} [label={q(label)}];')
        charts.append({"out": f"figures/{name}.png", "dot": "\n".join(dot + ["}"])})
        return f"![{name}](figures/{name}.png)"
    relations, overlays = [], []
    all_queries = old["entries"] + model["entries"]
    # Repeat entity boxes by parent/child role to avoid long chains that shrink labels in print.
    # Dictionary remains the complete attribute listing; each panel lists only its own FK columns.
    for i in range(0, len(refs), 8):
        group = refs[i:i+8]; nodes = {}; edges = []; shapes = {}; entities = {}
        for j, (child, col, parent, pcol) in enumerate(group):
            ckey, pkey = "child_" + child, "parent_" + parent
            entities[ckey] = child; entities[pkey] = parent
            child_cols = sorted({b for a, b, _, _ in group if a == child})
            nodes[ckey] = child + "\n[child] id [PK]\n" + "\n".join(c + " [FK]" for c in child_cols)
            nodes[pkey] = parent + "\n[parent] " + pcol + " [PK]"
            link = f"r{j}"; nodes[link] = col + "\nreferences"; shapes[link] = "diamond"
            meta = next(c for c in tables[child]["columns"] if c["name"] == col)
            snap = snapshot["tables"][f"public.{child}"]
            one = meta["unique"] or any(idx["isUnique"] and not idx.get("where") and len(idx["columns"]) == 1 and idx["columns"][0]["expression"] == col for idx in snap["indexes"].values())
            edges += [(ckey, link, ("1" if one else "N") + " / " + ("total" if meta["notNull"] else "partial")), (link, pkey, "1 / partial")]
        relations.append(graph(f"ERD-relations-{i//8+1:02}", nodes, edges, shapes))
        touched = {}
        all_queries = old["entries"] + model["entries"]
        for key, entity in entities.items():
            queries = [q for q in all_queries if entity in q.get("tables", []) or re.search(r'"' + entity + r'"', q["sql"])]
            attributes = set()
            for query in queries:
                if query["sql"].lower().startswith('update "' + entity + '"'):
                    attributes.update(re.findall(r'"(\w+)"\s*=', query["sql"].split(" where ")[0]))
            touched[key] = nodes[key] + "\nQueries: " + (", ".join(q["id"] for q in queries) or "—") + ("\nUPDATE attrs: " + ", ".join(sorted(attributes)) if attributes else "")
        overlays.append(graph(f"ERD-queries-{i//8+1:02}", touched, [("child_" + a, "parent_" + c, b + " → " + d) for a, b, c, d in group]))
    graph("Class-current20-extension", {
        "LoanRequestService": "LoanRequestService\ncreateRequest / listRequests\napproveRequest / rejectRequest",
        "loan_requests": "loan_requests\nemployee_id / principal_amount\ninstallment_count / reason / status / loan_id",
        "PaymentService": "createPayrollPaymentService (factory)\npreparePayrollPayments / getPromptpayQr\nconfirmPayrollPayment / cancelPreparedPayrollPayment\ngetPaymentSummary",
        "payroll_payments": "payroll_payments\npayroll_record_id / amount / status\nbranch_id_snapshot / frozen destination\nprepared actor / paid actor / cancel actor",
        "SessionService": "Session revocation service\nisRevoked / revokeSession",
        "revoked_session_tokens": "revoked_session_tokens\nuser_account_id / token_hash (protected)\nrevoked_at / expires_at",
    }, [("LoanRequestService", "loan_requests", "repository / transaction"), ("PaymentService", "payroll_payments", "repository / transaction"), ("SessionService", "revoked_session_tokens", "repository")])
    graph("concept-10", {
        "Actor": "ผู้ใช้ที่ผ่านการยืนยันตัวตน\nตาม role / scope",
        "P1": "1 จัดการองค์กร พนักงานและสิทธิ์", "P2": "2 เวลา ลา และ OT", "P3": "3 คำขอการเงินและหนี้",
        "P4": "4 คำนวณและล็อกรอบ", "P5": "5 เตรียมจ่าย บันทึกผล\nสลิป PDF/CSV และประวัติ",
        "D1": "D1 องค์กร บัญชี การจ้าง\nและ session revocation", "D2": "D2 เวลา ลา OT และ approval",
        "D3": "D3 เงินทดรอง คำขอเงินกู้\nสัญญา งวดผ่อนและหนี้", "D4": "D4 งวด ผลล็อก รายการย่อย\nปรับปรุงและ payment snapshots",
        "D5": "D5 สลิปและ delivery attempts", "D6": "D6 Audit append-only",
    }, [("Actor", p, "คำสั่งตามสิทธิ์") for p in ["P1", "P2", "P3", "P4", "P5"]]
       + [("P1", "D1", "อ่าน/บันทึก"), ("P2", "D2", "อ่าน/บันทึก"), ("P3", "D3", "อ่าน/บันทึก")]
       + [(d, "P4", "ข้อมูลคำนวณ") for d in ["D1", "D2", "D3"]]
       + [("P4", "D4", "บันทึกผล/ล็อก"), ("D4", "P5", "ผลล็อก/ปลายทางตรึง"), ("P5", "D4", "เตรียม/ยืนยัน/ยกเลิกจ่าย"), ("P5", "D5", "สลิป/ประวัติส่ง")]
       + [(p, "D6", "audit") for p in ["P1", "P2", "P3", "P4", "P5"]], {**{f"P{i}": "ellipse" for i in range(1, 6)}, **{f"D{i}": "cylinder" for i in range(1, 7)}})
    charts[-1]["dot"] = charts[-1]["dot"].replace("rankdir=LR", "rankdir=TB")
    start = s.index("#### 3.5.1 ER Diagram"); end = s.index("#### 3.5.3 Query Table", start)
    s = s[:start] + "#### 3.5.1 ER Diagram\n\nแบบจำลองเต็ม 39 ตาราง 91 FK 25 enums กล่อง entity ซ้ำตามบทบาท child/parent เพื่อให้ข้อความอ่านได้ในหน้ารายงาน; คอลัมน์ FK ในแต่ละภาพเป็นเฉพาะกลุ่มนั้น ส่วนรายการเต็มอยู่ใน Data Dictionary ทุก diamond แทน FK หนึ่งรายการ; child NOT NULL เป็น total participation ส่วน nullable เป็น partial; parent เป็น partial 1 ตาม PK การอ้างอิง FK ที่ unique แบบไม่มี predicate เป็น 1 มิฉะนั้น N; partial unique index จำกัดเฉพาะแถวที่เข้าเงื่อนไข จึงไม่เปลี่ยน cardinality ของประวัติทั้งหมด ข้อกำหนดที่ซับซ้อนให้ดู catalog/migration\n\n" + "\n\n".join(relations) + "\n\n#### 3.5.2 ER Diagram ที่มี Query\n\nแสดง PK/FK ของทุก entity พร้อม Query IDs ที่แตะข้อมูลนั้น; — หมายถึงไม่มี query สาธิตในทะเบียน ไม่ใช่ไม่มี implementation\n\n" + "\n\n".join(overlays) + "\n\n" + s[end:]
    if "figures/Class-current20-extension.png" not in s:
        s = s.replace("#### 3.6.2 State Diagram", "##### ส่วนขยายแบบจำลองตาม catalog ปัจจุบัน\n\nภาพส่วนขยายใช้ชื่อ use-case methods ที่มีอยู่จริง โดย payment และ session เป็น service factory ตามโค้ด ไม่อ้างว่าเป็น concrete OOP classes ตารางสามรายการที่เพิ่มจากแบบจำลองเดิมมีรายละเอียดครบใน Data Dictionary\n\n![Class-current20-extension](figures/Class-current20-extension.png)\n\n#### 3.6.2 State Diagram")
    path.write_text(s)
    (E / "current20-model-diagrams.json").write_text(json.dumps(charts, ensure_ascii=False, indent=2) + "\n")
    mappings = json.loads((E / "report-sql-traceability.json").read_text())
    mappings = [m for m in mappings if int(m["query"][1:]) < 20] + [{"query": q["id"], "useCases": q["uc"], "verifiedEvidence": "sql/current20-model.json"} for q in model["entries"]]
    (E / "report-sql-traceability.json").write_text(json.dumps(mappings, ensure_ascii=False, indent=2) + "\n")
    print("Refreshed 39 current dictionaries, 91 FK / 25 model diagrams, 25 enums and 5 current queries")


if __name__ == "__main__":
    main()
