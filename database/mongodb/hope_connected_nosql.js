// =====================================================================
// Hope Connected - banco não relacional (MongoDB)
// Banco: hope_connected_nosql
//
// Coleções:
//   impressoras_3d    -> as impressoras cadastradas pelos fornecedores
//   detalhes_impressao -> configurações de impressão e link do arquivo STL
//                         de cada solicitação
//
// Como rodar:
//   - mongosh:  mongosh --file hope_connected_nosql.js
//   - Compass:  conecte em mongodb://localhost:27017, abra o "MONGOSH"
//               (parte de baixo da tela), cole o script inteiro e aperte Enter.
//
// ATENÇÃO: o script APAGA as duas coleções e cria tudo de novo.
// =====================================================================

db = db.getSiblingDB("hope_connected_nosql");

db.impressoras_3d.drop();
db.detalhes_impressao.drop();

// ---------------------------------------------------------------------
// 1. impressoras_3d
//    id_usuario_fornecedor = id do fornecedor na tabela usuarios (MySQL)
//    volume_impressao      = tamanho máximo de impressão, em milímetros
//    Os _id fixos abaixo também aparecem no script SQL de dados de exemplo
//    (campo id_impressora de atendimentos_solicitacao).
// ---------------------------------------------------------------------
db.impressoras_3d.insertMany([
  {
    _id: ObjectId("665f1c2a8b3e4d0012a00001"),
    id_usuario_fornecedor: 456,
    marca_modelo: "Creality Ender 3 V2",
    tecnologia: "FDM",
    volume_impressao: { x_mm: 220, y_mm: 220, z_mm: 250 },
    status_disponibilidade: "Disponível"
  },
  {
    _id: ObjectId("665f1c2a8b3e4d0012a00002"),
    id_usuario_fornecedor: 456,
    marca_modelo: "Anycubic Photon Mono X",
    tecnologia: "SLA",
    volume_impressao: { x_mm: 192, y_mm: 120, z_mm: 245 },
    status_disponibilidade: "Em Uso"
  },
  {
    _id: ObjectId("665f1c2a8b3e4d0012a00003"),
    id_usuario_fornecedor: 789,
    marca_modelo: "Bambu Lab P1S",
    tecnologia: "FDM",
    volume_impressao: { x_mm: 256, y_mm: 256, z_mm: 256 },
    status_disponibilidade: "Disponível"
  }
]);

// ---------------------------------------------------------------------
// 2. detalhes_impressao
//    id_solicitacao  = id da solicitação na tabela solicitacoes (MySQL)
//    url_arquivo_stl = só o LINK do arquivo 3D (o arquivo em si não fica aqui)
//    Os links abaixo são fictícios, só para exemplo.
// ---------------------------------------------------------------------
db.detalhes_impressao.insertMany([
  {
    id_solicitacao: 1,
    url_arquivo_stl: "https://exemplo.com/stl/protese-de-mao.stl",
    altura_camada_mm: 0.2,
    densidade_preenchimento_pct: 40,
    temperatura_bico_celsius: 210,
    suportes_necessarios: true
  },
  {
    id_solicitacao: 2,
    url_arquivo_stl: "https://exemplo.com/stl/ortese-de-punho.stl",
    altura_camada_mm: 0.16,
    densidade_preenchimento_pct: 30,
    temperatura_bico_celsius: 235,
    suportes_necessarios: false
  },
  {
    id_solicitacao: 3,
    url_arquivo_stl: "https://exemplo.com/stl/suporte-de-dedo.stl",
    altura_camada_mm: 0.28,
    densidade_preenchimento_pct: 20,
    temperatura_bico_celsius: 205,
    suportes_necessarios: false
  },
  {
    id_solicitacao: 4,
    url_arquivo_stl: "https://exemplo.com/stl/ortese-de-tornozelo.stl",
    altura_camada_mm: 0.2,
    densidade_preenchimento_pct: 25,
    temperatura_bico_celsius: 230,
    suportes_necessarios: true
  }
]);

// Cada solicitação tem no máximo um documento de detalhes
db.detalhes_impressao.createIndex({ id_solicitacao: 1 }, { unique: true });

// ---------------------------------------------------------------------
// Conferência
// ---------------------------------------------------------------------
print("Banco: " + db.getName());
print("impressoras_3d:     " + db.impressoras_3d.countDocuments({}) + " documentos");
print("detalhes_impressao: " + db.detalhes_impressao.countDocuments({}) + " documentos");

// ---------------------------------------------------------------------
// EXEMPLOS DE CONSULTA (copie e cole um por vez no mongosh/Compass)
// ---------------------------------------------------------------------
// Todas as impressoras:
//   db.impressoras_3d.find()
//
// Só as disponíveis:
//   db.impressoras_3d.find({ status_disponibilidade: "Disponível" })
//
// Impressoras de um fornecedor (id do MySQL):
//   db.impressoras_3d.find({ id_usuario_fornecedor: 456 })
//
// Uma impressora pelo _id:
//   db.impressoras_3d.findOne({ _id: ObjectId("665f1c2a8b3e4d0012a00001") })
//
// Detalhes de impressão da solicitação 1:
//   db.detalhes_impressao.findOne({ id_solicitacao: 1 })
//
// Mudar o status de uma impressora:
//   db.impressoras_3d.updateOne(
//     { _id: ObjectId("665f1c2a8b3e4d0012a00002") },
//     { $set: { status_disponibilidade: "Disponível" } }
//   )
