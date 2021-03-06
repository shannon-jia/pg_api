/****************************************
* Schema
***************************************/
DROP SCHEMA IF EXISTS hardware CASCADE;
CREATE SCHEMA hardware;

/****************************************
 * Type
 ***************************************/
DROP TABLE IF EXISTS hardware.module;
DROP TYPE IF EXISTS hardware.mod_status;
CREATE TYPE hardware.mod_status AS ENUM (
       'ENCLOSURE TAMPER',
       'COMM FAIL',
       'ONLINE',
       'CABLE FAULT'
);

-- create module type
DROP TYPE IF EXISTS hardware.mod_type;
CREATE TYPE hardware.mod_type AS ENUM (
       'PM',
       'CABA',  -- cable A
       'CABB',  -- cable B
       'ROM08',
       'ROM16',
       'AIM',
       'M330',
       'TU',
       'LU',
       'ILU',
       'RM',
       'RCM',
       'MTP',
       'MTPA',
       'MTPB'
);

-- create module config
DROP TYPE IF EXISTS hardware.mod_conf;
CREATE TYPE hardware.mod_conf AS ENUM (
       'SECURED',
       'ACCESSED',
       'DISABLED'
);

--
DROP TYPE IF EXISTS hardware.socket_status;
CREATE TYPE hardware.socket_status AS ENUM (
       'NORMAL',
       'ALARM'
);

--
DROP TYPE IF EXISTS hardware.socket_type;
CREATE TYPE hardware.socket_type AS ENUM (
       'PM CABLE',
       'MTP CABLE',
       'CABLE'
);

--
DROP TYPE IF EXISTS hardware.socket_conf;
CREATE TYPE hardware.socket_conf AS ENUM (
       'SECURED',
       'ACCESSED',
       'DISABLED'
);

--
--
DROP TYPE IF EXISTS hardware.terminal_status;
CREATE TYPE hardware.terminal_status AS ENUM (
       'NORMAL',
       'ALARM'
);

--
DROP TYPE IF EXISTS hardware.terminal_type;
CREATE TYPE hardware.terminal_type AS ENUM (
       'AUXILIARY INPUT',
       'LAMP',
       'SPEAKER',
       'CAMERA'
);

--
DROP TYPE IF EXISTS hardware.terminal_conf;
CREATE TYPE hardware.terminal_conf AS ENUM (
       'SECURED',
       'ACCESSED',
       'DISABLED'
);

--
--
DROP TYPE IF EXISTS hardware.junction_status;
CREATE TYPE hardware.junction_status AS ENUM (
       'ACTIVATE',
       'RESET'
);

--
DROP TYPE IF EXISTS hardware.junction_type;
CREATE TYPE hardware.junction_type AS ENUM (
       'AUXILIARY OUTPUT',
       'RELAY OUTPUT',
       'LAMP',
       'SPEAKER',
       'CAMERA'
);

--
DROP TYPE IF EXISTS hardware.junction_conf;
CREATE TYPE hardware.junction_conf AS ENUM (
       'CLOSE',
       'OPEN',
       'DISABLED'
);

/****************************************
* Table
***************************************/
-- operation table
DROP TABLE IF EXISTS hardware.operation;
CREATE TABLE hardware.operation(
       id serial PRIMARY KEY,
       commands json default '{}'::json
);


-- system table
DROP TABLE IF EXISTS hardware.system;
CREATE TABLE hardware.system(
       id serial PRIMARY KEY,
       url text,
       comment text
);


--
DROP TABLE IF EXISTS hardware.module;
CREATE TABLE hardware.module(
       id serial PRIMARY KEY,
       type hardware.mod_type,
       status hardware.mod_status default 'COMM FAIL'::hardware.mod_status,
       system_id integer REFERENCES hardware.system default 1,
       unit integer default 1 CHECK (unit > 0),
       config hardware.mod_conf default 'SECURED'::hardware.mod_conf,
       link_group integer
);

--
DROP TABLE IF EXISTS hardware.socket;
CREATE TABLE hardware.socket(
       id serial PRIMARY KEY,
       type hardware.socket_type default 'PM CABLE'::hardware.socket_type,
       status hardware.socket_status default 'NORMAL'::hardware.socket_status,
       module_id integer REFERENCES hardware.module default 1,
       -- pin_scope int4range default '[0, 210)'::int4range,
       start_pin integer default 0,
       end_pin integer default 190,
       config hardware.socket_conf default 'SECURED'::hardware.socket_conf,
       link_group integer,
       CHECK (module_id > 0)
);

--
DROP TABLE IF EXISTS hardware.terminal;
CREATE TABLE hardware.terminal(
       id serial PRIMARY KEY,
       type hardware.terminal_type default 'AUXILIARY INPUT'::hardware.terminal_type,
       status hardware.terminal_status default 'NORMAL'::hardware.terminal_status,
       module_id integer REFERENCES hardware.module default 1,
       pin integer default 1 CHECK (pin > 0),
       config hardware.terminal_conf default 'SECURED'::hardware.terminal_conf,
       link_group integer
);

--
DROP TABLE IF EXISTS hardware.junction;
CREATE TABLE hardware.junction(
       id serial PRIMARY KEY,
       type hardware.junction_type default 'RELAY OUTPUT'::hardware.junction_type,
       status hardware.junction_status default 'RESET'::hardware.junction_status,
       module_id integer REFERENCES hardware.module default 1,
       pin integer default 1 CHECK (pin > 0),
       normal hardware.junction_status default 'RESET'::hardware.junction_status,
       operation_id integer REFERENCES hardware.operation default 1,
       dead_time integer default 0
);

--
DROP TABLE IF EXISTS hardware.linkage;
CREATE TABLE hardware.linkage(
       id serial PRIMARY KEY,
       junction_id integer REFERENCES hardware.junction,
       link_group integer,
       activation text,
       dead_time integer default 0
);

/****************************************
* insert line
***************************************/
INSERT INTO hardware.system(id, url)
 VALUES (1, 'ipp2://192.168.1.222:4001'),
        (2, 'ipp2://192.168.1.222:4002'),
        (3, 'ipp2://192.168.1.222:4003');

/****************************************
 * insert operation
 ***************************************/
INSERT INTO hardware.operation(id, commands)
       VALUES
       (1, '{
              "Secure": "secure",
              "Access": "access",
              "Disable": "disable"
              }'::json),
       (2, '{
              "On": "on",
              "Off": "off",
              "Disable": "disable"
              }'::json),
       (3, '{
              "Open": "open",
              "Close": "close",
              "Disable": "disable"
              }'::json);

/****************************************
 *  insert module
 ****************************************/
INSERT INTO hardware.module(type, unit, config, link_group)
       VALUES
       ('PM', 1, 'SECURED', 1),
       ('PM', 2, 'SECURED', 1),
       ('ROM08', 3, 'SECURED', 1),
       ('AIM', 4, 'ACCESSED', 1),
       ('CABA', 1, 'SECURED', 1),
       ('CABB', 1, 'SECURED', 1),
       ('CABA', 2, 'SECURED', 1),
       ('CABB', 2, 'SECURED', 1);

/****************************************
*  insert segment
****************************************/
INSERT INTO hardware.socket(module_id, link_group, start_pin, end_pin)
       VALUES
       (5, 1, 0, 100),
       (5, 1, 80, 190),
       (6, 1, 100, 0),
       (6, 1, 190, 80)
;

/****************************************
*  insert auxiliary Output
****************************************/
INSERT INTO hardware.terminal(id, module_id, pin, type)
       VALUES
       (1, 1, 1, 'AUXILIARY INPUT'),
       (2, 1, 2, 'AUXILIARY INPUT'),
       (3, 1, 3, 'AUXILIARY INPUT'),
       (4, 1, 4, 'AUXILIARY INPUT')
;

/****************************************
*  insert auxiliary Output
****************************************/
INSERT INTO hardware.junction(id, module_id, pin)
       VALUES
       (1, 3, 1),
       (2, 3, 2),
       (3, 3, 3),
       (4, 3, 4),
       (5, 3, 5),
       (6, 3, 6),
       (7, 3, 7),
       (8, 3, 8)
;

/****************************************
*   Funciton
****************************************/
DROP FUNCTION IF EXISTS hardware.mod_name;
CREATE OR REPLACE FUNCTION hardware.mod_name(hardware.module)
       RETURNS text AS $$
BEGIN
  SELECT  $1.type || '_' || $1.system_id || '_' || $1.unit;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS hardware.get_mod_name;
CREATE OR REPLACE FUNCTION hardware.get_mod_name(m hardware.module)
RETURNS text AS $$
BEGIN
  RETURN  m.type || '_' || m.system_id || '_' || m.unit;
END;
$$ LANGUAGE plpgsql;


/****************************************
*   Views
****************************************/
DROP VIEW IF EXISTS hardware.vm_terminal;
CREATE OR REPLACE VIEW hardware.vm_terminal AS
SELECT DISTINCT (m.type||'I_'||m.system_id||'_'||m.unit || '_' ||  t.pin) AS name,
       text(t.type) AS type, t.id, t.status
FROM hardware.module AS m,
     hardware.terminal AS t
WHERE t.module_id = m.id
;

DROP FUNCTION IF EXISTS hardware.update_auxin_status;
CREATE OR REPLACE FUNCTION hardware.update_auxin_status(x_name text,
       x_status hardware.terminal_status)
       RETURNS void AS $$
BEGIN
  UPDATE hardware.terminal SET status = x_status
  where id = (
        select distinct id from hardware.vm_terminal where name = x_name);
END;
$$ LANGUAGE plpgsql;

--
--  Views
--
DROP VIEW IF EXISTS hardware.vm_junction;
CREATE OR REPLACE VIEW hardware.vm_junction AS
SELECT DISTINCT (m.type||'_'||m.system_id||'_'||m.unit || '_' ||  t.pin) AS name,
       text(t.type) AS type, t.id, t.status
FROM hardware.module AS m,
       hardware.junction AS t
WHERE t.module_id = m.id
;

--
-- rpc
--
DROP FUNCTION IF EXISTS hardware.update_auxout_status;
CREATE OR REPLACE FUNCTION hardware.update_auxout_status(
       x_name text,
       x_status hardware.junction_status)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE hardware.junction SET status = x_status
  where id = (
  select distinct id from hardware.vm_junction where name = x_name);
END;

$BODY$;

--
--  Views
--
DROP VIEW IF EXISTS hardware.vm_module;
CREATE OR REPLACE VIEW hardware.vm_module AS
SELECT DISTINCT hardware.get_mod_name(m) AS name,
       m.id, m.status
FROM hardware.module AS m
;

--
-- rpc
--
DROP FUNCTION IF EXISTS hardware.update_module_status;
CREATE OR REPLACE FUNCTION hardware.update_module_status(
       x_name text,
       x_status hardware.mod_status)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE hardware.module SET status = x_status
  where id = (
  select distinct id from hardware.vm_module where name = x_name);
END;

$BODY$;

--
--
--
DROP FUNCTION IF EXISTS hardware.socket_name;
CREATE OR REPLACE FUNCTION hardware.socket_name(
       m hardware.module,
       s hardware.socket)
       RETURNS text
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  -- RETURN  m.type || '_' || m.system_id || '_' || m.unit;
  RETURN  concat_ws('_', 'SOCKET', m.type, m.system_id, m.unit, s.id);
END;

$BODY$;


--
--  Views
--
DROP VIEW IF EXISTS hardware.vm_socket;
CREATE OR REPLACE VIEW hardware.vm_socket AS
SELECT DISTINCT hardware.socket_name(m, s) AS name,
                s.id, s.status, s.config
FROM hardware.module AS m, hardware.socket AS s
     WHERE m.id = s.module_id
;

DROP VIEW IF EXISTS hardware.hw_socket;
CREATE OR REPLACE VIEW hardware.hw_socket AS
SELECT DISTINCT hardware.socket_name(m, s) AS name,
       hardware.get_mod_name(m) AS mod_name,
       s.id, s.status, s.start_pin, s.end_pin,
       s.link_group, s.config
FROM hardware.module AS m, hardware.socket AS s
     WHERE m.id = s.module_id
;

--
--
--
DROP TABLE IF EXISTS hardware.alarm CASCADE;
CREATE TABLE hardware.alarm(
       id serial PRIMARY KEY,
       name text,
       -- pin integer,
       ratio real,
       type text,
       model_name text,
       link_group integer,
       time_stamp text
);


--
-- rpc
--
DROP FUNCTION IF EXISTS hardware.update_socket_status;
CREATE OR REPLACE FUNCTION hardware.update_socket_status(
       x_name text,
       x_status hardware.socket_status,
       x_pin integer,
       x_time_stamp timestamp,
       x_type text)
RETURNS void
LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
  alm record;
  link record;
  x_offset real;
  r hardware.hw_socket%rowtype;

BEGIN

  -- query vm_socket
  FOR r IN
    SELECT * FROM hardware.hw_socket
           WHERE mod_name = x_name
           AND ((x_pin >= start_pin and x_pin < end_pin) or
               (x_pin <= start_pin and x_pin > end_pin))
  LOOP
      UPDATE hardware.socket SET status = x_status
             WHERE id = r.id;

      CONTINUE WHEN r.config <> 'SECURED';

      x_offset := (r.start_pin::real - x_pin::real)
                 /(r.start_pin::real - r.end_pin::real);
      RAISE NOTICE 'offset: %', x_offset;

      -- insert alarm
      SELECT * INTO alm FROM hardware.alarm
          WHERE model_name = r.name
            AND ratio=x_offset;
      IF NOT FOUND THEN
         INSERT INTO hardware.alarm (name, model_name, link_group, time_stamp, ratio, type)
             VALUES(x_name, r.name, r.link_group, x_time_stamp, x_offset, x_type);
      ELSE
        RAISE NOTICE 'Alarm is exists. %', r;
      END IF;
      RAISE NOTICE 'SUCCESS.';
  END LOOP;

END;

$BODY$;


/**
 *   queries
 **/
SELECT hardware.get_mod_name(m) AS name,
       m.status, m.config, o.commands, l.url
       FROM hardware.module AS m,
            hardware.operation AS o,
            hardware.system AS l
       WHERE m.system_id = l.id;

/**
  *
  *
  */
--
DROP TABLE IF EXISTS hardware.subcell;
CREATE TABLE hardware.subcell(
       id serial PRIMARY KEY,
       name integer,
       pin integer,
       link_group integer
);

