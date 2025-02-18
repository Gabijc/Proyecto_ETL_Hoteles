CREATE TABLE "Eventos"(
); 

CREATE TABLE "clientes" (
    "id_cliente" VARCHAR(255) PRIMARY KEY,
    "nombre" VARCHAR(255),
    "apellido" VARCHAR(255),
    "mail" VARCHAR(255)
);

CREATE TABLE "hoteles_grupo"(
	"id_hotel" VARCHAR(255) PRIMARY KEY, 
	"Nombre_hotel" VARCHAR(255),
	"Estrellas" VARCHAR(255),
	"id_ciudad" VARCHAR(255),
	"Competencia" BOOL 
);

);

CREATE TABLE "Reservas"(
	"id_reserva" VARCHAR(255) PRIMARY KEY, 
	"Fecha_reserva" DATE ,
	"inicio_estancia" DATE,
	"final_estancia" DATE,
	"Precio_noche" DECIMAL(),
	"id_cliente" VARCHAR(255) REFERENCES "clientes"("id_cliente"),
	"id_hotel_grupo" VARCHAR(255) REFERENCES "hoteles_grupo" ("id_hotel"),
	"id_hotel_competencia" VARCHAR(255) REFERENCES "hoteles_competencia" ("id_hotel"),
	"id_actividad" 
);