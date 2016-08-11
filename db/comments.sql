CREATE TABLE comments
(
  id serial NOT NULL,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  text text NOT NULL,
  task_id integer NOT NULL,
  user_id integer NOT NULL,
  CONSTRAINT comments_pkey PRIMARY KEY (id),
  CONSTRAINT comments_task_id_fkey FOREIGN KEY (task_id)
      REFERENCES tasks (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE comments
  OWNER TO admin;
