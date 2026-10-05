import re

# Read painel.html
with open("paginas/painel.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the placeholder in the video modal with an interactive HTML5 video player with custom video demo / controls
old_modal_inner = """          <div style="text-align:center; padding:40px; color:#8e8589;">
            <div style="font-size:48px; margin-bottom:12px; color:#7a1025;">🎬</div>
            <strong style="color:#d9d1d4; font-size:16px; display:block;">Player de Alta Definição Pronto</strong>
            <p style="font-size:12px; margin-top:8px;">Carregando transmissão segura criptografada...</p>
          </div>"""

new_modal_inner = """          <video id="playerVideoElement" controls autoplay style="width:100%; height:100%; object-fit:cover; display:block; background:#000;" poster="../imagens/foto-1.webp">
            <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4" type="video/mp4">
            Seu navegador não suporta a tag de vídeo.
          </video>"""

content = content.replace(old_modal_inner, new_modal_inner)

# Also update openVideoPlayer script function
old_open_video = """    function openVideoPlayer(title) {
      document.getElementById('videoModalTitle').textContent = title;
      document.getElementById('videoModal').classList.remove('hidden');
    }"""

new_open_video = """    function openVideoPlayer(title, posterImg) {
      document.getElementById('videoModalTitle').textContent = title;
      const vid = document.getElementById('playerVideoElement');
      if (posterImg && vid) vid.poster = posterImg;
      if (vid) {
        vid.currentTime = 0;
        vid.play().catch(()=>{});
      }
      document.getElementById('videoModal').classList.remove('hidden');
    }
    function closeVideoModal() {
      const vid = document.getElementById('playerVideoElement');
      if (vid) vid.pause();
      document.getElementById('videoModal').classList.add('hidden');
    }"""

content = content.replace(old_open_video, new_open_video)

# Save to painel.html and membros.html
with open("paginas/painel.html", "w", encoding="utf-8") as f:
    f.write(content)

with open("paginas/membros.html", "w", encoding="utf-8") as f:
    f.write(content)

with open("membros/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Player de vídeo integrado e atualizado com sucesso!")
