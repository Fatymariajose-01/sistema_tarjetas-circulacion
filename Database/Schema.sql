

-- 1. Tabla: USUARIO
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL CHECK (rol IN ('Administrador', 'Supervisor', 'Operador'))
);

-- 2. Tabla: PROPIETARIO
CREATE TABLE Propietario (
    id_propietario VARCHAR(15) PRIMARY KEY, -- DPI o NIT
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL
);

-- 3. Tabla: VEHICULO
CREATE TABLE Vehiculo (
    placa VARCHAR(10) PRIMARY KEY,
    vin VARCHAR(17) NOT NULL UNIQUE,
    numero_motor VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    linea VARCHAR(50) NOT NULL,
    color VARCHAR(30) NOT NULL,
    anio INT NOT NULL
);

-- 4. Tabla: TARJETA_CIRCULACION
CREATE TABLE Tarjeta_Circulacion (
    id_tarjeta SERIAL PRIMARY KEY,
    placa VARCHAR(10) NOT NULL,
    id_propietario VARCHAR(15) NOT NULL,
    fecha_emision DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_vencimiento DATE NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Activa',
    
    -- Llaves Foráneas
    CONSTRAINT fk_tarjeta_vehiculo FOREIGN KEY (placa) 
        REFERENCES Vehiculo(placa) ON DELETE CASCADE,
    CONSTRAINT fk_tarjeta_propietario FOREIGN KEY (id_propietario) 
        REFERENCES Propietario(id_propietario) ON DELETE CASCADE,
        
    -- Restricción de estados válidos
    CONSTRAINT chk_estado_tarjeta CHECK (estado IN ('Activa', 'Inactiva', 'Reemplazada'))
);

-- 5. Tabla: TRAMITE (Bitácora de gestión)
CREATE TABLE Tramite (
    id_tramite SERIAL PRIMARY KEY,
    tipo_tramite VARCHAR(50) NOT NULL,
    fecha_tramite DATE NOT NULL DEFAULT CURRENT_DATE,
    descripcion VARCHAR(255) NOT NULL,
    placa VARCHAR(10) NOT NULL,
    id_usuario INT NOT NULL,
    
    -- Llaves Foráneas
    CONSTRAINT fk_tramite_vehiculo FOREIGN KEY (placa) 
        REFERENCES Vehiculo(placa) ON DELETE CASCADE,
    CONSTRAINT fk_tramite_usuario FOREIGN KEY (id_usuario) 
        REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

-- 6. Tabla: CALCOMANIA
CREATE TABLE Calcomania (
    id_calcomania SERIAL PRIMARY KEY,
    placa VARCHAR(10) NOT NULL,
    anio INT NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT FALSE, -- TRUE = Solvente, FALSE = En Mora
    
    -- Llave Foránea
    CONSTRAINT fk_calcomania_vehiculo FOREIGN KEY (placa) 
        REFERENCES Vehiculo(placa) ON DELETE CASCADE,
        
    -- Evitar duplicados de pago para una misma placa en el mismo año
    CONSTRAINT uq_placa_anio_calcomania UNIQUE (placa, anio)
);


-- TRIGGER AUTOMÁTICO PARA REEMPLAZAR TARJETAS VIEJAS


-- Función que se ejecuta antes de insertar una nueva tarjeta
CREATE OR REPLACE FUNCTION fn_reemplazar_tarjeta_activa()
RETURNS TRIGGER AS $$
BEGIN
    -- Busca la tarjeta 'Activa' anterior de esa placa y la cambia a 'Reemplazada'
    UPDATE Tarjeta_Circulacion
    SET estado = 'Reemplazada'
    WHERE placa = NEW.placa AND estado = 'Activa';
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creación del Trigger ligado a la tabla Tarjeta_Circulacion
CREATE TRIGGER tg_reemplazar_tarjeta_vieja
BEFORE INSERT ON Tarjeta_Circulacion
FOR EACH ROW
EXECUTE FUNCTION fn_reemplazar_tarjeta_activa();