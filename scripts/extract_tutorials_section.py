with open('scripts/membros_autenticado.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
tut_match = re.search(r'(<section[^>]*data-content=["\']tutoriais["\'][^>]*>.*?</section>)', html, re.S)
if tut_match:
    print("Found data-content='tutoriais' section! Length:", len(tut_match.group(1)))
    with open('scripts/section_tutoriais.html', 'w', encoding='utf-8') as out:
        out.write(tut_match.group(1))
    print("Saved to scripts/section_tutoriais.html")
else:
    # search for id="tutoriais" or similar
    tut_id = re.search(r'(<[^>]+id=["\']tutoriais["\'][^>]*>.*?</section>)', html, re.S)
    if tut_id:
        print("Found id='tutoriais' section!")
        with open('scripts/section_tutoriais.html', 'w', encoding='utf-8') as out:
            out.write(tut_id.group(1))
