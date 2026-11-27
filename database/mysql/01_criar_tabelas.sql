-- =====================================================================
-- Hope Connected - banco relacional (MySQL 8)
-- Script 1 de 2: cria o banco e as 4 tabelas.
--
-- ATENÇÃO: este script APAGA o banco "hope_connected" (se já existir)
-- e cria tudo de novo. Use para começar do zero.
--
-- Os nomes das colunas seguem as entidades do back-end (User e Solicitacao).
-- As impressoras NÃO ficam no MySQL: elas ficam no MongoDB
-- (coleção impressoras_3d). Por isso, em atendimentos_solicitacao,
-- o campo id_impressora guarda o _id do documento do MongoDB (texto).
-- =====================================================================

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS hope_connected;

CREATE DATABASE hope_connected
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE hope_connected;

-- ---------------------------------------------------------------------
-- 1. usuarios  (quem usa o site: funcionário da AACD ou fornecedor)
-- ---------------------------------------------------------------------
CREATE TABLE usuarios (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome          VARCHAR(150) NOT NULL,
  email         VARCHAR(150) NOT NULL,
  senha_hash    VARCHAR(255) NOT NULL,
  phone         VARCHAR(20)  NULL,
  role          ENUM('AACD', 'Fornecedor') NOT NULL,

  -- endereço (só o fornecedor precisa; a AACD pode deixar vazio)
  cep           CHAR(8)      NULL,
  logradouro    VARCHAR(255) NULL,
  numero        VARCHAR(10)  NULL,
  complemento   VARCHAR(100) NULL,
  bairro        VARCHAR(100) NULL,
  cidade        VARCHAR(100) NULL,
  estado        CHAR(2)      NULL,

  data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 2. solicitacoes  (pedido de uma peça criado pela AACD)
-- ---------------------------------------------------------------------
CREATE TABLE solicitacoes (
  id                 INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_usuario_aacd    INT UNSIGNED NOT NULL,
  nome_peca          VARCHAR(150) NOT NULL,
  material_requerido VARCHAR(60)  NOT NULL,
  quantidade         SMALLINT UNSIGNED NOT NULL DEFAULT 1,
  prioridade         ENUM('Baixa', 'Média', 'Alta') NOT NULL DEFAULT 'Média',
  status             ENUM('Aberto', 'Em Produção', 'Concluído', 'Cancelado')
                     NOT NULL DEFAULT 'Aberto',
  data_criacao       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  CONSTRAINT fk_solicitacoes_usuario
    FOREIGN KEY (id_usuario_aacd) REFERENCES usuarios (id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 3. atendimentos_solicitacao  (fornecedor que aceitou uma solicitação)
--    Guarda uma cópia das especificações da impressora usada, porque
--    a impressora em si está no MongoDB.
-- ---------------------------------------------------------------------
CREATE TABLE atendimentos_solicitacao (
  id                    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_solicitacao        INT UNSIGNED NOT NULL,
  id_usuario_fornecedor INT UNSIGNED NOT NULL,
  id_impressora         VARCHAR(24)  NOT NULL,   -- _id do MongoDB (impressoras_3d)

  -- cópia das especificações da impressora no momento do aceite
  marca_modelo          VARCHAR(120) NOT NULL,
  tecnologia            VARCHAR(30)  NOT NULL,
  volume_x_mm           DECIMAL(7,2) NOT NULL,
  volume_y_mm           DECIMAL(7,2) NOT NULL,
  volume_z_mm           DECIMAL(7,2) NOT NULL,

  data_aceite           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status_producao       ENUM('Imprimindo', 'Enviado', 'Entregue')
                        NOT NULL DEFAULT 'Imprimindo',

  PRIMARY KEY (id),
  CONSTRAINT fk_atendimentos_solicitacao
    FOREIGN KEY (id_solicitacao) REFERENCES solicitacoes (id),
  CONSTRAINT fk_atendimentos_fornecedor
    FOREIGN KEY (id_usuario_fornecedor) REFERENCES usuarios (id),
  -- a mesma impressora não aceita a mesma solicitação duas vezes
  UNIQUE KEY uq_atendimento (id_solicitacao, id_impressora)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 4. envios_entregas  (como a peça foi enviada)
-- ---------------------------------------------------------------------
CREATE TABLE envios_entregas (
  id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_atendimento  INT UNSIGNED NOT NULL,
  metodo_envio    VARCHAR(60)  NOT NULL,          -- ex.: Correios, Motoboy
  codigo_rastreio VARCHAR(60)  NULL,
  data_envio      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  CONSTRAINT fk_envios_atendimento
    FOREIGN KEY (id_atendimento) REFERENCES atendimentos_solicitacao (id)
) ENGINE=InnoDB;
