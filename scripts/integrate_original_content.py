import os
import shutil
import glob

downloads = r"c:\Users\diseg\Downloads"
project = r"c:\Users\diseg\Downloads\CLONE_capivaraclubhot_com_1791175079789"

workflows_dir = os.path.join(project, "workflows")
videos_dir = os.path.join(project, "videos")
imagens_dir = os.path.join(project, "imagens")

os.makedirs(workflows_dir, exist_ok=True)
os.makedirs(videos_dir, exist_ok=True)
os.makedirs(imagens_dir, exist_ok=True)

# 1. Copy all real Capivara JSON workflows
workflow_names = [
    "CAPIVARA DU HOT - GERAR VÍDEOS PROMPT.json",
    "CONTROLMOTION 2 - CAPIVARA DUHOT - VIDEO +18.json",
    "controlmotion-capivara-duhot.json",
    "faceswap-capivara-duhot.json",
    "SWAP - FLUX - CAPIVARA.json",
    "TROCA DE ROUPA - WF GRATIS.json",
    "UPSCALE IMG - CAPIVARA (GRÁTIS).json",
    "VARIOS ANGULOS.json",
    "KREA 2 - ROSTO + PROMPT.json",
    "MOTION+CONTROL+v7.json",
    "Motion+Control+-+Mudar_Apenas_Mulher.json"
]

copied_workflows = []
for f in os.listdir(downloads):
    for target in workflow_names:
        if target.lower() in f.lower() or f.lower() in target.lower():
            src = os.path.join(downloads, f)
            if f.endswith('.json'):
                dst = os.path.join(workflows_dir, f)
                shutil.copy2(src, dst)
                copied_workflows.append(f)
                print(f"Copied Workflow: {f} ({os.path.getsize(src)} bytes)")
                break

# 2. Copy all real video lessons and AI videos
video_files = [
    "PARTE 1.mp4", "PARTE 2.mp4", "PARTE 3.mp4", "PARTE 4.mp4", "PARTE 5.mp4", "PARTE 6.mp4", "PARTE 7.mp4",
    "jiebujie_00001_p86-audio_jiqat_1791101467.mp4",
    "jiebujie_00001_p87-audio_vqrpr_1791096741.mp4",
    "jiebujie_00001_p86-audio_eunfu_1790970228.mp4",
    "jiebujie_00001_p86-audio_kpzns_1790884991.mp4",
    "jiebujie_00001_p87-audio_pxiit_1790831885.mp4",
    "jiebujie_00001_p85-audio_lkbej_1790815028.mp4",
    "jiebujie_00001_p83-audio_timca_1790311698.mp4",
    "TUTORIAL 1 NEXO CREATOR.mp4"
]

copied_videos = []
for f in os.listdir(downloads):
    if f in video_files or (f.startswith("jiebujie") and f.endswith(".mp4")) or (f.startswith("PARTE ") and f.endswith(".mp4")):
        src = os.path.join(downloads, f)
        dst = os.path.join(videos_dir, f)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        copied_videos.append(f)
        print(f"Copied Video: {f} ({os.path.getsize(src)} bytes)")

# 3. Copy all original model photos
image_files = [
    "Retrato Natural no Banheiro Moderno.png",
    "Retrato praiano com coco verde em Ipanema.png",
    "Retrato Urbano Noturno com Bebida.png",
    "03a7c6ca-fffe-41cc-a48d-4b8c8505de11.png",
    "261754f0-e05c-41a4-9ff8-0a918f5baca4.png",
    "274a357c-6627-4a0b-9e59-69d130ef54c5.png",
    "d2787d39-7e8c-4494-94b0-6963a4e5d8f9.png",
    "dc531021-f93e-4e8c-9c68-49d0bc497b54.png"
]

copied_images = []
for f in image_files:
    src = os.path.join(downloads, f)
    if os.path.exists(src):
        dst = os.path.join(imagens_dir, f)
        shutil.copy2(src, dst)
        copied_images.append(f)
        print(f"Copied Image: {f}")

print("\n--- RESUMO DE CÓPIAS ORIGINAIS ---")
print(f"Workflows originais copiados: {len(copied_workflows)}")
print(f"Vídeos originais copiados: {len(copied_videos)}")
print(f"Imagens originais copiadas: {len(copied_images)}")
