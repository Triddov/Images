-- Table: public.images

-- DROP TABLE IF EXISTS public.images;

CREATE TABLE IF NOT EXISTS public.images
(
    id integer NOT NULL DEFAULT nextval('images_id_seq'::regclass),
    title character varying(255) COLLATE pg_catalog."default" NOT NULL,
    path character varying(255) COLLATE pg_catalog."default",
    size character varying(30) COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    tags character varying(255) COLLATE pg_catalog."default",
    extension character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT images_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.images
    OWNER to postgres;