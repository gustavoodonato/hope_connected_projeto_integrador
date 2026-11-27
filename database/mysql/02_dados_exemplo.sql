-- =====================================================================
-- Hope Connected - dados de exemplo (MySQL)
-- Script 2 de 2: rode DEPOIS do 01_criar_tabelas.sql.
--
-- Todos os usuários de exemplo têm a senha:  senha123
-- (só para desenvolvimento; nunca use isso em produção)
--
-- Os valores de id_impressora (665f1c2a8b3e4d0012a0000X) são os _id das
-- impressoras criadas no script do MongoDB (hope_connected_nosql.js).
-- =====================================================================

SET NAMES utf8mb4;
USE hope_connected;

-- Usuários -------------------------------------------------------------
INSERT INTO usuarios
  (id, nome, email, senha_hash, phone, role,
   cep, logradouro, numero, complemento, bairro, cidade, estado)
VALUES
  (123, 'Murilo', 'muriloso123@gmail.com', 'scrypt:32768:8:1$LJh52Cmfad5wDopf$a44c7a7ebf3e5dbf78be4879fdd0df53373a8affb2c1b47d85c32fdbf76ecc1c6bccb0882ea1ea4203c3c062694dcb84f23eaed973e9eddcd6c878808f91177c',
   NULL, 'AACD',
   NULL, NULL, NULL, NULL, NULL, NULL, NULL),
  (456, 'Lucas', 'luquinhas24@gmail.com', 'scrypt:32768:8:1$LJh52Cmfad5wDopf$a44c7a7ebf3e5dbf78be4879fdd0df53373a8affb2c1b47d85c32fdbf76ecc1c6bccb0882ea1ea4203c3c062694dcb84f23eaed973e9eddcd6c878808f91177c',
   '55444446666', 'Fornecedor',
   '00111222', 'Rua catapimbas da silva', '323', NULL, 'Vila Assunção', 'São Caetano do Sul', 'SP'),
  (789, 'Julio', 'juliao323@gmail.com', 'scrypt:32768:8:1$LJh52Cmfad5wDopf$a44c7a7ebf3e5dbf78be4879fdd0df53373a8affb2c1b47d85c32fdbf76ecc1c6bccb0882ea1ea4203c3c062694dcb84f23eaed973e9eddcd6c878808f91177c',
   '22333334444', 'Fornecedor',
   '00111222', 'Rua belterra', '291', NULL, 'Santo amaro', 'São Paulo', 'SP');

-- Solicitações (todas criadas pelo usuário AACD 123) --------------------
INSERT INTO solicitacoes
  (id, id_usuario_aacd, nome_peca, material_requerido, quantidade, prioridade, status, data_criacao)
VALUES
  (1, 123, 'Prótese de mão',       'PLA',  2, 'Alta',  'Aberto',      '2026-11-10 09:00:00'),
  (2, 123, 'Órtese de punho',      'PETG', 1, 'Média', 'Em Produção', '2026-11-11 14:30:00'),
  (3, 123, 'Suporte de dedo',      'PLA',  5, 'Baixa', 'Aberto',      '2026-11-12 10:15:00'),
  (4, 123, 'Órtese de tornozelo',  'TPU',  1, 'Alta',  'Concluído',   '2026-11-05 08:00:00');

-- Atendimentos (fornecedor que aceitou + cópia da impressora) -----------
INSERT INTO atendimentos_solicitacao
  (id, id_solicitacao, id_usuario_fornecedor, id_impressora,
   marca_modelo, tecnologia, volume_x_mm, volume_y_mm, volume_z_mm,
   data_aceite, status_producao)
VALUES
  (1, 2, 456, '665f1c2a8b3e4d0012a00002',
   'Anycubic Photon Mono X', 'SLA', 192, 120, 245,
   '2026-11-11 16:00:00', 'Imprimindo'),
  (2, 4, 789, '665f1c2a8b3e4d0012a00003',
   'Bambu Lab P1S', 'FDM', 256, 256, 256,
   '2026-11-06 09:30:00', 'Entregue');

-- Envios ---------------------------------------------------------------
INSERT INTO envios_entregas
  (id, id_atendimento, metodo_envio, codigo_rastreio, data_envio)
VALUES
  (1, 2, 'Correios', 'BR123456789BR', '2026-11-08 11:00:00');

-- Confere quantos registros entraram ---------------------------------
SELECT 'usuarios' AS tabela, COUNT(*) AS total FROM usuarios
UNION ALL SELECT 'solicitacoes', COUNT(*) FROM solicitacoes
UNION ALL SELECT 'atendimentos_solicitacao', COUNT(*) FROM atendimentos_solicitacao
UNION ALL SELECT 'envios_entregas', COUNT(*) FROM envios_entregas;
