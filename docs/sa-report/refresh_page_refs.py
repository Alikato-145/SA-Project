from pathlib import Path
from pypdf import PdfReader
from docx import Document
from docx.oxml.ns import qn
import re,json,argparse
a=argparse.ArgumentParser();a.add_argument("--pdf",required=True);args=a.parse_args()
R=Path(__file__).resolve().parent;r=PdfReader(args.pdf);pages={}
def scan(items):
 for x in items:
  if isinstance(x,list):scan(x)
  else:pages[x.title]=r.get_destination_page_number(x)+1
scan(r.outline)
captions={}
for i,p in enumerate(r.pages):
 if i+1<pages.get('บทที่ 1 คณะผู้จัดทำ',1):continue
 for kind,num in re.findall(r'^(ภาพที่|ตารางที่)[^\d\n]{0,15}(\d+\.\d+)\b',p.extract_text(),re.M):captions.setdefault(kind+' '+num,i+1)
doc=Document(R/'Haris-SA-Report.docx');bookmarks={}
for b in doc.element.xpath('//w:bookmarkStart'):
 parent=b.getparent()
 if parent.tag==qn('w:p'):bookmarks[b.get(qn('w:name'))]=''.join(parent.xpath('.//w:t/text()'))
missing=[];count=0
for f in doc.element.xpath('//w:fldSimple'):
 instr=f.get(qn('w:instr'),'');m=re.match(r'PAGEREF\s+(\S+)',instr)
 if not m:continue
 title=bookmarks[m[1]];p=pages.get(title)
 if p is None:
  key=re.match(r'(ภาพที่|ตารางที่) (\d+\.\d+)',title)
  if key:p=captions.get(key[1]+' '+key[2])
 if p is None:missing.append((m[1],title));continue
 for t in f.iter(qn('w:t')):t.text=str(p)
 count+=1
assert not missing,missing
# Preserve dynamic Word fields and cache verified pages for initial display.
doc.save(R/'Haris-SA-Report.docx')
(R/'evidence/page-reference-verification.json').write_text(json.dumps({'pages':len(r.pages),'references_updated':count,'missing':missing},ensure_ascii=False));print('Verified pages',len(r.pages),'Updated references',count)
