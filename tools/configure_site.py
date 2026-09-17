#!/usr/bin/env python3
"""Set the deployed public URL and deliberate indexability, then rebuild the static files.
This never uploads, changes DNS, or writes to GitHub.
"""
from pathlib import Path
from urllib.parse import urlsplit
import argparse,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--url',required=True,help='Actual final site URL, including a GitHub repository path if used.')
g=p.add_mutually_exclusive_group(required=True);g.add_argument('--index',action='store_true',help='Allow search indexing for the configured production site.');g.add_argument('--preview',action='store_true',help='Retain noindex for a review/staging site.')
a=p.parse_args();u=urlsplit(a.url.strip())
if u.scheme!='https' or not u.netloc or u.username or u.password or u.query or u.fragment or any(c in a.url for c in '<>"\\'):
 p.error('Provide an actual HTTPS site URL, without credentials, a query, or a fragment.')
if any(x in u.path.split('/') for x in ('.','..')):p.error('Site path may not contain . or .. segments.')
settings=json.loads((R/'content/settings.json').read_text());settings.update(public_url=a.url.strip().rstrip('/'),indexable=bool(a.index))
(R/'content/settings.json').write_text(json.dumps(settings,indent=2))
for tool in ['build.py','make_preview.py']:subprocess.run([sys.executable,str(R/'tools'/tool)],check=True)
print('Rebuilt locally for',settings['public_url']);print('Search indexing:', 'enabled' if a.index else 'disabled');print('No deployment, domain, or GitHub change was performed.')
