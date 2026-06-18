-- CreateTable
CREATE TABLE `usuarios` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(191) NOT NULL,
    `senha_hash` VARCHAR(191) NOT NULL,
    `papel` ENUM('PASTOR', 'LIDER', 'TESOUREIRO', 'MEMBRO') NOT NULL DEFAULT 'MEMBRO',
    `ativo` BOOLEAN NOT NULL DEFAULT true,
    `criado_em` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `ultimo_acesso` DATETIME(3) NULL,

    UNIQUE INDEX `usuarios_email_key`(`email`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `membros` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(191) NOT NULL,
    `cpf` VARCHAR(191) NULL,
    `telefone` VARCHAR(191) NULL,
    `email` VARCHAR(191) NULL,
    `data_nascimento` DATETIME(3) NULL,
    `estado_civil` ENUM('SOLTEIRO', 'CASADO', 'DIVORCIADO', 'VIUVO') NULL,
    `endereco` VARCHAR(191) NULL,
    `foto_url` VARCHAR(191) NULL,
    `data_ingresso` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `status` ENUM('ATIVO', 'INATIVO') NOT NULL DEFAULT 'ATIVO',
    `criado_em` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `usuario_id` INTEGER NULL,

    UNIQUE INDEX `membros_cpf_key`(`cpf`),
    UNIQUE INDEX `membros_email_key`(`email`),
    UNIQUE INDEX `membros_usuario_id_key`(`usuario_id`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `grupos` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(191) NOT NULL,
    `descricao` VARCHAR(191) NULL,
    `criado_em` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `lider_id` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `grupo_membros` (
    `grupo_id` INTEGER NOT NULL,
    `membro_id` INTEGER NOT NULL,

    PRIMARY KEY (`grupo_id`, `membro_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `frequencias` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `presente` BOOLEAN NOT NULL DEFAULT true,
    `registrado_em` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `membro_id` INTEGER NOT NULL,
    `evento_id` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `categorias_financeiras` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(191) NOT NULL,
    `tipo` ENUM('DIZIMO', 'DOACAO', 'DESPESA') NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `campanhas` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(191) NOT NULL,
    `descricao` VARCHAR(191) NULL,
    `meta_valor` DECIMAL(10, 2) NULL,
    `data_inicio` DATETIME(3) NOT NULL,
    `data_fim` DATETIME(3) NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `lancamentos_financeiros` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `tipo` ENUM('DIZIMO', 'DOACAO', 'DESPESA') NOT NULL,
    `valor` DECIMAL(10, 2) NOT NULL,
    `data` DATETIME(3) NOT NULL,
    `descricao` VARCHAR(191) NULL,
    `comprovante_url` VARCHAR(191) NULL,
    `criado_em` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `membro_id` INTEGER NULL,
    `campanha_id` INTEGER NULL,
    `categoria_id` INTEGER NOT NULL,
    `registrado_por` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `avisos` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `titulo` VARCHAR(191) NOT NULL,
    `conteudo` TEXT NOT NULL,
    `publicado_em` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `ativo` BOOLEAN NOT NULL DEFAULT true,
    `autor_id` INTEGER NOT NULL,
    `grupo_id` INTEGER NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `eventos` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `titulo` VARCHAR(191) NOT NULL,
    `descricao` TEXT NULL,
    `local` VARCHAR(191) NULL,
    `data_inicio` DATETIME(3) NOT NULL,
    `data_fim` DATETIME(3) NULL,
    `cancelado` BOOLEAN NOT NULL DEFAULT false,
    `criado_em` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `criado_por` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `evento_confirmacoes` (
    `evento_id` INTEGER NOT NULL,
    `membro_id` INTEGER NOT NULL,

    PRIMARY KEY (`evento_id`, `membro_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `pedidos_oracao` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `conteudo` TEXT NOT NULL,
    `privado` BOOLEAN NOT NULL DEFAULT false,
    `respondido` BOOLEAN NOT NULL DEFAULT false,
    `criado_em` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `membro_id` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `oracoes` (
    `pedido_id` INTEGER NOT NULL,
    `membro_id` INTEGER NOT NULL,

    PRIMARY KEY (`pedido_id`, `membro_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `membros` ADD CONSTRAINT `membros_usuario_id_fkey` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `grupos` ADD CONSTRAINT `grupos_lider_id_fkey` FOREIGN KEY (`lider_id`) REFERENCES `membros`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `grupo_membros` ADD CONSTRAINT `grupo_membros_grupo_id_fkey` FOREIGN KEY (`grupo_id`) REFERENCES `grupos`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `grupo_membros` ADD CONSTRAINT `grupo_membros_membro_id_fkey` FOREIGN KEY (`membro_id`) REFERENCES `membros`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `frequencias` ADD CONSTRAINT `frequencias_membro_id_fkey` FOREIGN KEY (`membro_id`) REFERENCES `membros`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `frequencias` ADD CONSTRAINT `frequencias_evento_id_fkey` FOREIGN KEY (`evento_id`) REFERENCES `eventos`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `lancamentos_financeiros` ADD CONSTRAINT `lancamentos_financeiros_membro_id_fkey` FOREIGN KEY (`membro_id`) REFERENCES `membros`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `lancamentos_financeiros` ADD CONSTRAINT `lancamentos_financeiros_campanha_id_fkey` FOREIGN KEY (`campanha_id`) REFERENCES `campanhas`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `lancamentos_financeiros` ADD CONSTRAINT `lancamentos_financeiros_categoria_id_fkey` FOREIGN KEY (`categoria_id`) REFERENCES `categorias_financeiras`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `lancamentos_financeiros` ADD CONSTRAINT `lancamentos_financeiros_registrado_por_fkey` FOREIGN KEY (`registrado_por`) REFERENCES `usuarios`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `avisos` ADD CONSTRAINT `avisos_autor_id_fkey` FOREIGN KEY (`autor_id`) REFERENCES `usuarios`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `avisos` ADD CONSTRAINT `avisos_grupo_id_fkey` FOREIGN KEY (`grupo_id`) REFERENCES `grupos`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `eventos` ADD CONSTRAINT `eventos_criado_por_fkey` FOREIGN KEY (`criado_por`) REFERENCES `usuarios`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `evento_confirmacoes` ADD CONSTRAINT `evento_confirmacoes_evento_id_fkey` FOREIGN KEY (`evento_id`) REFERENCES `eventos`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `evento_confirmacoes` ADD CONSTRAINT `evento_confirmacoes_membro_id_fkey` FOREIGN KEY (`membro_id`) REFERENCES `membros`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `pedidos_oracao` ADD CONSTRAINT `pedidos_oracao_membro_id_fkey` FOREIGN KEY (`membro_id`) REFERENCES `membros`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `oracoes` ADD CONSTRAINT `oracoes_pedido_id_fkey` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos_oracao`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `oracoes` ADD CONSTRAINT `oracoes_membro_id_fkey` FOREIGN KEY (`membro_id`) REFERENCES `membros`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
