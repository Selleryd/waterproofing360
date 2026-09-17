#!/usr/bin/env python3
"""Create a release inventory and ZIP of the current site without external dependencies."""
from pathlib import Path
import hashlib,json,zipfile,argparse
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--out',default=str(R.parent/'WATERPROOFING360_R5_GITHUB.zip'));a=p.parse_args();out=Path(a.out).resolve()
def eligible(f):return f.is_file() and not f.is_symlink() and '__pycache__' not in f.parts and '.git' not in f.parts and f.suffix not in {'.pyc','.zip','.woff','.woff2','.ttf','.otf','.eot'} and f!=out
files=sorted(f for f in R.rglob('*') if eligible(f) and f.name!='MANIFEST.json')
manifest={'release':'5.0.0','sha256_method':'hashlib.sha256, original bytes','files':[{'path':str(f.relative_to(R)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]}
(R/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(f for f in R.rglob('*') if eligible(f)):z.write(f,Path(R.name)/f.relative_to(R))
with zipfile.ZipFile(out) as z:
 if z.testzip():raise RuntimeError('ZIP CRC validation failed')
print(out);print('ZIP SHA256:',hashlib.sha256(out.read_bytes()).hexdigest())
