CREATE TABLE IF NOT EXISTS `vive_con` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

-- DROP TABLE nivel_estudio;
CREATE TABLE IF NOT EXISTS `nivel_estudio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `religion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- drop TABLE lengua_indigena;
CREATE TABLE IF NOT EXISTS`lengua_indigena` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

-- drop table sexo;
CREATE TABLE IF NOT EXISTS `sexo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(20) NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

-- drop table ocupacion;
CREATE TABLE IF NOT EXISTS `ocupacion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(128) NOT NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- drop table medio_contacto;
CREATE TABLE IF NOT EXISTS `medio_contacto` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

-- drop table municipio;
CREATE TABLE IF NOT EXISTS`municipio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(128) NOT NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;


-- drop table medios;
CREATE TABLE IF NOT EXISTS `medios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(512) NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `estado_civil` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(128) NOT NULL,
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

-- drop table tipo_caso;
CREATE TABLE IF NOT EXISTS `tipo_caso` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(512),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

-- drop table estatus;
CREATE TABLE IF NOT EXISTS `estatus` (
 `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(512),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

-- drop table modalidad_violencia;
CREATE TABLE IF NOT EXISTS `modalidad_violencia` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(128),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

-- drop table nivel_violencia;
CREATE TABLE IF NOT EXISTS `nivel_violencia` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45),
  `estatus` TINYINT NULL,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

drop table if exists pais;
create table pais (
	id int auto_increment, 
    nombre varchar (45) not null unique, 
    estatus tinyint (4), 
    fecha_alta timestamp default current_timestamp, 
    fecha_baja datetime, 
    primary key (id)
);

drop table if exists estado;
create table estado (
	id int auto_increment, 
    -- id_pais int, 
    nombre varchar (45) not null unique, 
    estatus tinyint (4), 
    fecha_alta timestamp default current_timestamp, 
    fecha_baja datetime, 
    primary key (id) 
    -- foreign key (id_pais) references pais (id)
);

drop table if exists consejero;
create table consejero (
	id int auto_increment, 
    -- id_estado int, 
    nombre varchar (128) not null unique, 
    estatus tinyint (4), 
    fecha_alta timestamp default current_timestamp, 
    fecha_baja datetime, 
    primary key (id) 
    -- foreign key (id_estado) references estado (id)
);

drop table if exists tipo_violencia;
create table tipo_violencia (
	id int auto_increment, 
    -- id_estado int, 
    nombre varchar (128), 
    estatus tinyint (4), 
    fecha_alta timestamp default current_timestamp, 
    fecha_baja datetime, 
    primary key (id) 
    -- foreign key (id_estado) references estado (id)
);

drop table if exists violentometro;
create table violentometro (
	id int auto_increment, 
    -- id_estado int, 
    nombre varchar (518), 
    estatus tinyint (4), 
    fecha_alta timestamp default current_timestamp, 
    fecha_baja datetime, 
    primary key (id) 
    -- foreign key (id_estado) references estado (id)
);

drop table if exists acude_institucion;
create table acude_institucion (
	id int auto_increment, 
    -- id_estado int, 
    nombre varchar (518), 
    estatus tinyint (4), 
    fecha_alta timestamp default current_timestamp, 
    fecha_baja datetime, 
    primary key (id) 
    -- foreign key (id_estado) references estado (id)
);

drop table if exists ayuda_psicologica;
create table ayuda_psicologica (
	id int auto_increment, 
    -- id_estado int, 
    nombre varchar (518), 
    estatus tinyint (4), 
    fecha_alta timestamp default current_timestamp, 
    fecha_baja datetime, 
    primary key (id) 
    -- foreign key (id_estado) references estado (id)
);
DROP TABLE ayuda_legal;
CREATE TABLE IF NOT EXISTS `ayuda_legal` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(512),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ayuda_medica` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(128),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ayuda_otros` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(128),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `canal_legal` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(128),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `canal_otro` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(128),
  `estatus` TINYINT NULL DEFAULT 1,
  `fecha_alta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_baja` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB;

DROP TABLE victima;
CREATE TABLE IF NOT EXISTS `victima` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido_paterno` VARCHAR(45) NULL,
  `apellido_materno` VARCHAR(45) NULL,
  `telefono` VARCHAR(13) NULL,
  `edad` INT NULL,
  `estado_civil` INT ,
  `ocupacion` INT ,
  `religion` INT ,
  `vive_con` INT ,
  `nivel_estudio` INT ,
  `sexo` INT,
  `municipio` INT ,
  `medios` INT ,
  `lengua_indigena` INT ,
  `medio_contacto` INT ,
  `caso_id` int null,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


INSERT INTO estado_civil(nombre) SELECT DISTINCT EstadoCivil FROM casos;
INSERT INTO municipio(nombre) SELECT DISTINCT Municipio FROM casos;
INSERT INTO ocupacion(nombre) SELECT DISTINCT Ocupacion FROM casos;
INSERT INTO religion(nombre) SELECT DISTINCT Religion FROM casos;
INSERT INTO vive_con(nombre) SELECT DISTINCT VivesCon FROM casos;
INSERT INTO medios(nombre) SELECT DISTINCT ComoTeEnteraste FROM casos;
INSERT INTO tipo_caso(nombre) SELECT DISTINCT tipocaso FROM casos;
INSERT INTO estatus(nombre) SELECT DISTINCT Estatus FROM casos;
INSERT INTO sexo(nombre) SELECT DISTINCT Sexo FROM casos;
INSERT INTO nivel_estudio(nombre) SELECT DISTINCT NivelEstudios FROM casos;
INSERT INTO lengua_indigena(nombre) SELECT DISTINCT LenguaIndigena FROM casos;
INSERT INTO medio_contacto(nombre) SELECT DISTINCT MedioContacto FROM casos;
INSERT INTO nivel_violencia(nombre) SELECT DISTINCT NivelViolencia FROM casos;

INSERT INTO pais(nombre) SELECT DISTINCT Pais FROM casos;
INSERT INTO estado(nombre) SELECT DISTINCT Estado FROM casos;

INSERT INTO modalidad_violencia(nombre) SELECT DISTINCT Consejera FROM llamadas;
INSERT INTO tipo_violencia(nombre) SELECT DISTINCT TipoViolencia FROM llamadas;
INSERT INTO modalidad_violencia(nombre) SELECT DISTINCT ModalidadViolencia FROM llamadas;
INSERT INTO violentometro(nombre) SELECT DISTINCT Violentometro FROM llamadas;
INSERT INTO acude_institucion(nombre) SELECT DISTINCT AcudeInstitucion FROM llamadas;
insert into consejero (nombre) select distinct Consejera from llamadas;
insert into violentometro (nombre) select distinct Violentometro from llamadas;

insert into ayuda_psicologica (nombre) select distinct AyudaPsicologico from llamadas;
insert into ayuda_legal (nombre) select distinct AyudaLegal from llamadas;
insert into ayuda_medica (nombre) select distinct AyudaMedica from llamadas;
insert into ayuda_otros (nombre) select distinct AyudaOtros from llamadas;
insert into canal_legal (nombre) select distinct CanaLegal from llamadas;
insert into canal_otro (nombre) select distinct CanaOtro from llamadas;

UPDATE casos_temporal, estado_civil SET casos_temporal.EstadoCivil = estado_civil.id 
WHERE casos_temporal.EstadoCivil = estado_civil.nombre;

UPDATE casos_temporal, municipio SET casos_temporal.Municipio = municipio.id 
WHERE casos_temporal.Municipio = municipio.nombre;

UPDATE casos_temporal, estado SET casos_temporal.Estado = estado.id 
WHERE casos_temporal.Estado = estado.nombre;

UPDATE casos_temporal, ocupacion SET casos_temporal.Ocupacion = ocupacion.id 
WHERE casos_temporal.Ocupacion = ocupacion.nombre;

UPDATE casos_temporal, religion SET casos_temporal.Religion = religion.id 
WHERE casos_temporal.Religion = religion.nombre;

UPDATE casos_temporal, vive_con SET casos_temporal.VivesCon = vive_con.id 
WHERE casos_temporal.VivesCon = vive_con.nombre;

UPDATE casos_temporal, medios SET casos_temporal.ComoTeEnteraste = medios.id 
WHERE casos_temporal.ComoTeEnteraste = medios.nombre;

UPDATE casos_temporal, tipo_caso SET casos_temporal.tipocaso = tipo_caso.id 
WHERE casos_temporal.tipocaso = tipo_caso.nombre;

UPDATE casos_temporal, estatus SET casos_temporal.Estatus = estatus.id 
WHERE casos_temporal.Estatus = estatus.nombre;

UPDATE casos_temporal, sexo SET casos_temporal.Sexo = sexo.id 
WHERE casos_temporal.Sexo = sexo.nombre;

UPDATE casos_temporal, nivel_estudio SET casos_temporal.NivelEstudios = nivel_estudio.id 
WHERE casos_temporal.NivelEstudios = nivel_estudio.nombre;

UPDATE casos_temporal, lengua_indigena SET casos_temporal.LenguaIndigena = lengua_indigena.id 
WHERE casos_temporal.LenguaIndigena = lengua_indigena.nombre;

UPDATE casos_temporal, medio_contacto SET casos_temporal.MedioContacto = medio_contacto.id 
WHERE casos_temporal.MedioContacto = medio_contacto.nombre;

UPDATE casos_temporal, pais SET casos_temporal.Pais = pais.id
WHERE casos_temporal.Pais = pais.nombre;

UPDATE casos_temporal, nivel_violencia SET casos_temporal.NivelViolencia = nivel_violencia.id
WHERE casos_temporal.NivelViolencia = nivel_violencia.nombre;

UPDATE casos_temporal, victima SET casos_temporal.Telefono = victima.id
WHERE casos_temporal.Telefono = victima.telefono;

/* UPDATE llamadas_temporal, ayuda_psicologica  SET llamadas_temporal.AyudaPsicologico = ayuda_psicologica.id WHERE llamadas_temporal.AyudaPsicologico = ayuda_psicologica.nombre;
UPDATE llamadas_temporal, ayuda_legal  SET llamadas_temporal.AyudaLegal = ayuda_legal.id WHERE llamadas_temporal.AyudaLegal = ayuda_legal.nombre;
UPDATE llamadas_temporal, ayuda_medica  SET llamadas_temporal.AyudaMedica = ayuda_medica.id WHERE llamadas_temporal.AyudaMedica = ayuda_medica.nombre;
UPDATE llamadas_temporal, ayuda_otros  SET llamadas_temporal.AyudaOtros = ayuda_otros.id WHERE llamadas_temporal.AyudaOtros = ayuda_otros.nombre;
UPDATE llamadas_temporal, canal_legal  SET llamadas_temporal.CanaLegal = canal_legal.id WHERE llamadas_temporal.CanaLegal = canal_legal.nombre;
UPDATE llamadas_temporal, canal_otro  SET llamadas_temporal.CanaOtro = canal_otro.id WHERE llamadas_temporal.CanaOtro = canal_otro.nombre; */
