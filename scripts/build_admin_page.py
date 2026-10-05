admin_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel do Administrador — CAPIVARA CLUB HOT</title>
  <link rel="icon" href="../icons/favicon-32.png">
  <meta name="theme-color" content="#050304">
  <link rel="stylesheet" href="../assets/ui.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-1.css">
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="../assets/ui.js"></script>

  <style>
    body {
      background: #080305;
      color: #eee;
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 24px;
    }
    .admin-wrap {
      max-width: 1100px;
      margin: 0 auto;
    }
    .admin-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 28px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      padding-bottom: 18px;
    }
    .admin-title {
      font-family: 'Anton', sans-serif;
      font-size: 24px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .metrics {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 28px;
    }
    .metric-card {
      background: rgba(18, 9, 13, 0.7);
      border: 1px solid rgba(152, 29, 56, 0.4);
      padding: 20px;
      border-radius: 14px;
    }
    .metric-card span {
      font-size: 12px;
      color: #a79da1;
      text-transform: uppercase;
      font-weight: 700;
    }
    .metric-card strong {
      display: block;
      font-size: 28px;
      color: #f1d5dd;
      font-family: 'Anton', sans-serif;
      margin-top: 8px;
    }
    .sales-table {
      width: 100%;
      border-collapse: collapse;
      background: rgba(18, 9, 13, 0.6);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(255,255,255,0.08);
    }
    .sales-table th, .sales-table td {
      padding: 14px 18px;
      text-align: left;
      font-size: 13px;
    }
    .sales-table th {
      background: rgba(122, 16, 37, 0.2);
      color: #f1d5dd;
      font-weight: 700;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .sales-table tr:not(:last-child) td {
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .badge-paid {
      background: #06251d;
      color: #00e58a;
      border: 1px solid rgba(0, 229, 138, 0.3);
      padding: 4px 10px;
      border-radius: 99px;
      font-size: 11px;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <div class="admin-wrap">
    <div class="admin-header">
      <div class="admin-title">
        <img src="../imagens/logo.webp" height="32" alt="Logo">
        PAINEL DO PROPRIETÁRIO — CAPIVARA CLUB HOT
      </div>
      <div>
        <a href="painel.html" style="color:#d85b72; text-decoration:none; font-size:13px; font-weight:700;">Área de Membros →</a>
      </div>
    </div>

    <div class="metrics">
      <div class="metric-card">
        <span>Faturamento Hoje</span>
        <strong>R$ 3.867,60</strong>
      </div>
      <div class="metric-card">
        <span>Vendas Aprovadas (PIX)</span>
        <strong>44</strong>
      </div>
      <div class="metric-card">
        <span>Taxa de Conversão PIX</span>
        <strong>88.4%</strong>
      </div>
      <div class="metric-card">
        <span>Saques de Afiliados Pendentes</span>
        <strong>R$ 439,50</strong>
      </div>
    </div>

    <h2 style="font-family:'Anton'; font-size:18px; margin:20px 0 12px;">ÚLTIMAS VENDAS CONFIRMADAS (PIX)</h2>
    <table class="sales-table">
      <thead>
        <tr>
          <th>Horário</th>
          <th>Cliente</th>
          <th>E-mail</th>
          <th>Valor</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Agora há pouco</td>
          <td>Lucas M. Andrade</td>
          <td>lucas.m***@gmail.com</td>
          <td>R$ 87,90</td>
          <td><span class="badge-paid">APROVADO</span></td>
        </tr>
        <tr>
          <td>Há 12 min</td>
          <td>Rafael S. Oliveira</td>
          <td>rafael***@hotmail.com</td>
          <td>R$ 87,90</td>
          <td><span class="badge-paid">APROVADO</span></td>
        </tr>
        <tr>
          <td>Há 38 min</td>
          <td>Eduardo Costa</td>
          <td>dudu***@gmail.com</td>
          <td>R$ 87,90</td>
          <td><span class="badge-paid">APROVADO</span></td>
        </tr>
        <tr>
          <td>Há 1h</td>
          <td>Marcos Vinicius</td>
          <td>m.vinicius***@outlook.com</td>
          <td>R$ 87,90</td>
          <td><span class="badge-paid">APROVADO</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
"""

with open("paginas/admin.html", "w", encoding="utf-8") as f:
    f.write(admin_html)

print("paginas/admin.html criado com sucesso!")
