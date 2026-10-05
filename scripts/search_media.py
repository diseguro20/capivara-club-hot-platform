import glob, re

for fname in glob.glob('*.*'):
    if fname.endswith(('.png', '.jpg', '.jpeg', '.webp', '.ico', '.py')):
        continue
    try:
        with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        media_matches = re.findall(r'https?://[^\s\"\'<>]+(?:\.mp4|\.m3u8|\.webm|youtube|vimeo|panda|vturb|b-cdn|bunny)[^\s\"\'<>]*', content, re.I)
        if media_matches:
            print(f'Matches in {fname}:', media_matches)
        json_matches = re.findall(r'https?://[^\s\"\'<>]+\.json', content, re.I)
        if json_matches:
            print(f'JSON matches in {fname}:', json_matches)
    except Exception as e:
        pass
print('Done searching local files.')
