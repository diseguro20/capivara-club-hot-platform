import urllib.request

url = 'http://localhost:5500/member-scripts/area_membros_esteira_interna_ferramentas-1.js?v=20261005-gallery-fix'
with urllib.request.urlopen(url) as r:
    content = r.read().decode('utf-8')
    print('Script fetched successfully! Total length:', len(content))
    print('Contains direct gallery src:', 'src="/member-assets/gallery/${index}-1.jpeg"' in content)
    print('Contains loadMemberGalleryImages in openPage:', "if (page === 'galeria') loadMemberGalleryImages()" in content)
