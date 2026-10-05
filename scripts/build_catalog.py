import json
import os

workflows_dir = "workflows"
os.makedirs(workflows_dir, exist_ok=True)

# 1. Create sample/template ComfyUI workflows
wf1 = {
    "name": "Consistência de Rosto IP-Adapter + ControlNet",
    "description": "Mantém 100% da identidade facial da modelo em qualquer pose ou roupa.",
    "model": "SDXL 1.0 / Realistic Vision",
    "nodes": {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "realisticStockPhoto_v20.safetensors"}},
        "2": {"class_type": "IPAdapterModelLoader", "inputs": {"ipadapter_file": "ip-adapter-plus_sdxl_vit-h.safetensors"}},
        "3": {"class_type": "IPAdapterApply", "inputs": {"weight": 0.85, "noise": 0.35}},
        "4": {"class_type": "KSampler", "inputs": {"steps": 30, "cfg": 6.5, "sampler_name": "dpmpp_2m_sde", "scheduler": "karras"}}
    }
}

wf2 = {
    "name": "Flux Realismo Extremo & Textura de Pele",
    "description": "Workflow otimizado para modelo Flux Dev gerando poros reais e iluminação de estúdio.",
    "model": "Flux.1 Dev",
    "nodes": {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "flux1-dev.sft"}},
        "2": {"class_type": "DualCLIPLoader", "inputs": {"clip_name1": "t5xxl_fp8_e4m3fn.safetensors", "clip_name2": "clip_l.safetensors"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.sft"}},
        "4": {"class_type": "KSamplerFlux", "inputs": {"steps": 25, "guidance": 3.5}}
    }
}

wf3 = {
    "name": "Troca de Roupas & Cenários (Inpainting)",
    "description": "Substitui lingerie, biquínis e cenários preservando corpo e feições.",
    "model": "SDXL Inpainting",
    "nodes": {
        "1": {"class_type": "InpaintModelLoader", "inputs": {"model_name": "sdxl_inpaint.safetensors"}},
        "2": {"class_type": "VAEEncodeForInpaint", "inputs": {"grow_mask_by": 8}}
    }
}

wf4 = {
    "name": "Animação de Imagem para Vídeo (I2V)",
    "description": "Transforma a imagem estática da modelo em vídeo com piscadas, respiração e sorrisos.",
    "model": "AnimateDiff / SVD / CogVideo",
    "nodes": {
        "1": {"class_type": "AnimateDiffLoaderGen1", "inputs": {"model_name": "animatediffMotion_v15V2.ckpt"}},
        "2": {"class_type": "KSampler", "inputs": {"steps": 20, "frames": 24, "fps": 12}}
    }
}

wf5 = {
    "name": "Upscaling 4K Ultra-HD com Restauração de Rosto",
    "description": "Aumenta a resolução para 4K adicionando micro-detalhes à pele e cabelo.",
    "model": "4x-UltraSharp + CodeFormer",
    "nodes": {
        "1": {"class_type": "UpscaleModelLoader", "inputs": {"model_name": "4x-UltraSharp.pth"}},
        "2": {"class_type": "FaceRestoreCFWithModel", "inputs": {"fidelity": 0.9}}
    }
}

sample_workflows = [
    ("workflow-consistencia-rosto.json", wf1),
    ("workflow-flux-realismo.json", wf2),
    ("workflow-troca-roupas-inpainting.json", wf3),
    ("workflow-animacao-video-i2v.json", wf4),
    ("workflow-upscale-4k.json", wf5)
]

for filename, data in sample_workflows:
    with open(os.path.join(workflows_dir, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 2. Build full catalogo_produtos.json
catalogo = {
    "plataforma": {
        "nome": "CAPIVARA CLUB HOT",
        "url_origem": "https://capivaraclubhot.com",
        "descricao": "Plataforma completa para criação de modelos de Inteligência Artificial com consistência facial, nicho HOT e UGC.",
        "preco_atual": 87.90,
        "moeda": "BRL",
        "garantia_dias": 7,
        "metodo_pagamento": "PIX Instantâneo com QR Code",
        "suporte": "Acesso imediato após confirmação"
    },
    "estatisticas": {
        "prompts_testados": 200,
        "workflows": 10,
        "garantia": "7 dias total"
    },
    "carrossel_fotos": [
        {"id": 1, "arquivo": "imagens/foto-1.webp", "original": "fotos-carrossel/foto-1.jpeg", "titulo": "Modelo IA Consistente 1"},
        {"id": 2, "arquivo": "imagens/foto-2.webp", "original": "fotos-carrossel/foto-2.jpeg", "titulo": "Modelo IA Consistente 2"},
        {"id": 3, "arquivo": "imagens/foto-3.webp", "original": "fotos-carrossel/foto-3.png", "titulo": "Modelo IA Sensual 3"},
        {"id": 4, "arquivo": "imagens/foto-4.webp", "original": "fotos-carrossel/foto-4.png", "titulo": "Modelo IA UGC 4"},
        {"id": 5, "arquivo": "imagens/foto-5.webp", "original": "fotos-carrossel/foto-5.jpeg", "titulo": "Modelo IA Estúdio 5"},
        {"id": 6, "arquivo": "imagens/foto-6.webp", "original": "fotos-carrossel/foto-6.png", "titulo": "Modelo IA Praia 6"}
    ],
    "o_que_esta_incluido": [
        {"numero": "01", "categoria": "IMAGEM", "titulo": "Imagens ultra-realistas", "descricao": "Prompts preparados para criar fotos com aparência natural, diferentes poses, cenários, roupas e estilos."},
        {"numero": "02", "categoria": "VÍDEO", "titulo": "Dê vida às imagens", "descricao": "Estruturas de prompt para transformar ideias estáticas em cenas com movimento e aparência realista."},
        {"numero": "03", "categoria": "CONSISTÊNCIA", "titulo": "Rosto consistente", "descricao": "Crie uma personagem reconhecível em diferentes gerações, poses, ambientes e situações."},
        {"numero": "04", "categoria": "ESTILOS", "titulo": "Vários estilos", "descricao": "Explore diferentes propostas visuais sem precisar começar seus prompts do zero."},
        {"numero": "05", "categoria": "CENÁRIOS", "titulo": "Qualquer cenário", "descricao": "Praia, cidade, quarto, academia, viagens e muito mais, com prompts organizados para facilitar a criação."},
        {"numero": "06", "categoria": "ACESSO", "titulo": "Pronto para usar", "descricao": "Você recebe o material e pode começar a testar suas ideias imediatamente."}
    ],
    "faq": [
        {"pergunta": "Como recebo o acesso?", "resposta": "O acesso é disponibilizado imediatamente após a confirmação do pagamento via PIX."},
        {"pergunta": "Preciso saber programação?", "resposta": "Não. O material foi pensado para ser utilizado por quem quer trabalhar diretamente com criação de conteúdo por IA."},
        {"pergunta": "Posso usar os prompts para criar diferentes conteúdos?", "resposta": "Sim. Os prompts servem como base para você adaptar personagens, cenários, poses, estilos e ideias."},
        {"pergunta": "Existe garantia?", "resposta": "Sim. A oferta apresentada possui garantia incondicional de 7 dias."}
    ],
    "workflows_disponiveis": [
        {"id": "wf-1", "titulo": "Consistência de Rosto IP-Adapter", "arquivo": "workflows/workflow-consistencia-rosto.json", "formato": "JSON ComfyUI", "tags": ["Rosto", "Identidade", "SDXL"]},
        {"id": "wf-2", "titulo": "Flux Realismo Extremo & Textura", "arquivo": "workflows/workflow-flux-realismo.json", "formato": "JSON ComfyUI", "tags": ["Flux", "Ultra-HD", "Pele"]},
        {"id": "wf-3", "titulo": "Troca de Roupas & Cenários Inpainting", "arquivo": "workflows/workflow-troca-roupas-inpainting.json", "formato": "JSON ComfyUI", "tags": ["Inpaint", "Roupas", "Cenários"]},
        {"id": "wf-4", "titulo": "Animação Vídeo I2V", "arquivo": "workflows/workflow-animacao-video-i2v.json", "formato": "JSON ComfyUI", "tags": ["Vídeo", "Movimento", "AnimateDiff"]},
        {"id": "wf-5", "titulo": "Upscale 4K Restauração Facial", "arquivo": "workflows/workflow-upscale-4k.json", "formato": "JSON ComfyUI", "tags": ["Upscaling", "4K", "Detalhes"]}
    ],
    "categorias_prompts": [
        {"nome": "UGC & Redes Sociais", "qtd": 45, "icone": "camera"},
        {"nome": "Sensual & Lingerie", "qtd": 60, "icone": "fire"},
        {"nome": "Praia & Piscina", "qtd": 35, "icone": "sun"},
        {"nome": "Moda & Streetwear Urbano", "qtd": 30, "icone": "shopping-bag"},
        {"nome": "Fitness & Academia", "qtd": 25, "icone": "activity"},
        {"nome": "Close-up & Retrato", "qtd": 35, "icone": "user"}
    ]
}

with open("catalogo_produtos.json", "w", encoding="utf-8") as f:
    json.dump(catalogo, f, indent=2, ensure_ascii=False)

print("catalogo_produtos.json e workflows criados com sucesso!")
