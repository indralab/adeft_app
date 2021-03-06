import os
import re
import json
import argparse


from indra_db.util.content_scripts import get_stmts_with_agent_text_like

from adeft_app.locations import DATA_PATH
from adeft_app.filenames import escape_filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get statements with agent'
                                     'text matching a pattern')
    parser.add_argument('pattern')
    parser.add_argument('keep', nargs='?')

    args = parser.parse_args()
    pattern = args.pattern
    keep = args.keep
    if not keep:
        keep = ''
    keep = re.compile(keep)
    stmt_dict = get_stmts_with_agent_text_like(pattern,
                                               filter_genes=True)
    for shortform, stmts in stmt_dict.items():
        if (shortform[0] in ['-', '.'] or
                set(shortform) & set(': ')):
            continue
        cased_shortform = escape_filename(shortform)
        if re.match(keep, shortform):
            with open(os.path.join(DATA_PATH,
                                   'statements',
                                   f'{cased_shortform}_statements.json'),
                      'w') as f:
                json.dump(stmts, f)
