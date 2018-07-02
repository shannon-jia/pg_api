/****************************************
 * Schema
 ***************************************/
DROP SCHEMA IF EXISTS map CASCADE;
CREATE SCHEMA map;

/****************************************
 * Type
 ***************************************/

/****************************************
* Table
***************************************/
-- operation table
DROP TABLE IF EXISTS map.stations;
CREATE TABLE map.stations(
       id serial PRIMARY KEY,
       name text,
       value text,
       selected bool default true
);


--  device table
DROP TABLE IF EXISTS map.devices;
CREATE TABLE map.devices(
       id serial PRIMARY KEY,
       hw_id integer REFERENCES hardware.module,
       coords point,
       layer integer default 1,
       station integer REFERENCES map.stations,
       comment text
);

--  segments table
DROP TABLE IF EXISTS map.segments;
CREATE TABLE map.segments(
       id serial PRIMARY KEY,
       hw_id integer REFERENCES hardware.socket,
       path path,
       layer integer default 1,
       station integer REFERENCES map.stations,
       comment text
);

--  fields table
DROP TABLE IF EXISTS map.fields;
CREATE TABLE map.fields(
       id serial PRIMARY KEY,
       hw_id integer REFERENCES hardware.terminal,
       field polygon,
       layer integer default 2,
       station integer REFERENCES map.stations,
       comment text
);

--  lsc table
DROP TABLE IF EXISTS map.lsc;
CREATE TABLE map.lsc(
       id serial PRIMARY KEY,
       hw_id integer REFERENCES hardware.junction,
       coords point,
       layer integer default 3,
       station integer REFERENCES map.stations,
       comment text
);

/****************************************
* insert datas
***************************************/
INSERT INTO map.stations(id, name, value)
 VALUES (1, '甲站', 'first'),
        (2, '乙站', 'second'),
        (3, '丙站', 'third');


/****************************************
 *  insert devices
 ****************************************/
INSERT INTO map.devices(hw_id, coords, station)
       VALUES
       (1, '(10,10)'::point, 1),
       (2, '(20,20)'::point, 1),
       (3, '(30,30)'::point, 1);


/****************************************
*  insert segment
****************************************/
INSERT INTO map.segments(hw_id, path, station)
       VALUES
       (1, '((100,100),(100, 200))', 1),
       (2, '((100,200),(200, 200))', 1),
       (3, '((200,200),(300, 300))', 1);


/****************************************
*  insert fields
****************************************/
INSERT INTO map.fields(hw_id, field, station)
       VALUES
       (1, '((10,10),(10, 20),(30,30),(30,40))'::polygon, 1),
       (2, '((5.0, 5.0), (20, 20), (35, 35), (55, 55))'::polygon, 1)
;

/****************************************
*  insert lsc
****************************************/
INSERT INTO map.lsc(hw_id, coords, station)
       VALUES
       (1, '(210,210)'::point, 1),
       (2, '(220,220)'::point, 1),
       (3, '(230,230)'::point, 1);



/****************************************
 *   Funciton
****************************************/
DROP FUNCTION IF EXISTS map.get_status;
CREATE OR REPLACE FUNCTION map.get_status (config text, status text)
RETURNS text AS $$
BEGIN
  CASE UPPER(status)
       WHEN 'ONLINE', 'NORMAL' THEN
            RETURN status;
       ELSE
            RETURN status;
  END CASE;
END;
$$ LANGUAGE plpgsql;

/****************************************
 *   Map Views
 ****************************************/
DROP VIEW IF EXISTS map.vm_devices;
CREATE OR REPLACE VIEW map.vm_devices AS
SELECT hardware.get_mod_name(m) AS device_name,
       text(m.type) AS type, d.id,
       map.get_status(text(m.config), text(m.status)) AS status,
       d.coords, d.comment, s.name AS station, m.config,
       d.layer, '{}'::json AS actions
FROM hardware.module AS m,
     map.devices AS d,
     map.stations AS s
WHERE d.hw_id = m.id and
      d.station = s.id
 ;

-- segment
DROP VIEW IF EXISTS map.vm_segments;
CREATE OR REPLACE VIEW map.vm_segments AS
SELECT hardware.socket_name(m, k) AS device_name,
       text(k.type) AS type, d.id, m.config,
       map.get_status(text(k.config), text(k.status)) AS status,
       d.path, d.comment, s.name AS station,
       d.layer, '{}'::json AS actions
FROM hardware.module AS m,
     hardware.socket AS k,
     map.segments AS d,
     map.stations AS s
WHERE d.hw_id = k.id and
      k.module_id = m.id and
      d.station = s.id
;

-- field
DROP VIEW IF EXISTS map.vm_fields;
CREATE OR REPLACE VIEW map.vm_fields AS
SELECT hardware.get_mod_name(m)||'_'||k.id AS device_name,
       text(k.type) AS type, d.id,
       map.get_status(text(k.config), text(k.status)) AS status,
       d.field, d.comment, s.name AS station,
       d.layer, '{}'::json AS actions
FROM hardware.module AS m,
     hardware.terminal AS k,
     map.fields AS d,
     map.stations AS s
WHERE d.hw_id = k.id and
      k.module_id = m.id and
      d.station = s.id
;

-- lsc
DROP VIEW IF EXISTS map.vm_lsc;
CREATE OR REPLACE VIEW map.vm_lsc AS
SELECT hardware.get_mod_name(m)||'_'||k.id AS device_name,
       text(k.type) AS type, d.id,
       k.status,
       d.coords, d.comment, s.name AS station,
       d.layer, o.commands AS actions
FROM hardware.module AS m,
     hardware.junction AS k,
     hardware.operation AS o,
     map.lsc AS d,
     map.stations AS s
WHERE d.hw_id = k.id and
      k.module_id = m.id and
      d.station = s.id and
      k.operation_id = o.id
;

-- alarms_point function
DROP FUNCTION IF EXISTS map.calc_segment_point;
CREATE OR REPLACE FUNCTION map.calc_segment_point(
       seg_path path,
       ratio real )
       RETURNS point
       LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
  x0 real;
  y0 real;
  x1 real;
  y1 real;
  x real;
  y real;
  loc point;
  locs point[];

BEGIN
  locs := regexp_replace(regexp_replace(regexp_replace(textin(path_out(seg_path)),
          '^\((.*)\)$', '{\1}'), '\(', '"(', 'g'), '\)', ')"', 'g');

  loc := locs[1];
  x0 := loc[0];
  y0 := loc[1];

  loc := locs[2];
  x1 := loc[0];
  y1 := loc[1];

  x := x0 + (x1 - x0) * ratio;
  y := y0 + (y1 - y0) * ratio;

  loc := (x,y);

  RETURN loc;
END;

$BODY$;

-- alarms
DROP VIEW IF EXISTS map.vm_alarms;
CREATE OR REPLACE VIEW map.vm_alarms AS
       SELECT
       a.id,
       a.name,
       a.type,
       s.device_name,
       map.calc_segment_point(s.path, a.ratio) AS coords,
       a.time_stamp,
       s.station,
       s.layer,
       s.comment
FROM hardware.alarm a,
     map.vm_segments s
WHERE a.model_name = s.device_name
;

--
-- rpc
--
DROP FUNCTION IF EXISTS map.config_device;
CREATE OR REPLACE FUNCTION map.config_device(
       x_name text,
       x_config hardware.mod_conf)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE hardware.module SET config = x_config
  where id = (
  select distinct id from hardware.vm_module where name = x_name);
END;

$BODY$;

--
DROP FUNCTION IF EXISTS map.config_field;
CREATE OR REPLACE FUNCTION map.config_field(
       x_name text,
       x_config hardware.terminal_conf)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE hardware.terminal SET config = x_config
  where id = (
  select distinct id from hardware.vm_terminal where name = x_name);
END;

$BODY$;

--
DROP FUNCTION IF EXISTS map.config_segment;
CREATE OR REPLACE FUNCTION map.config_segment(
       x_name text,
       x_config hardware.socket_conf)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE hardware.socket SET config = x_config
  where id = (
  select distinct id from hardware.vm_socket where name = x_name);
END;

$BODY$;

--
DROP FUNCTION IF EXISTS map.update_device_coords;
CREATE OR REPLACE FUNCTION map.update_device_coords(
       x_name text,
       x_coords point)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE map.devices SET coords = x_coords
  where id = (
  select distinct id from map.vm_devices where device_name = x_name);
END;

$BODY$;

DROP FUNCTION IF EXISTS map.update_field_field;
CREATE OR REPLACE FUNCTION map.update_field_field(
       x_name text,
       x_field polygon)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE map.fields SET field = x_field
  where id = (
  select distinct id from map.vm_fields where device_name = x_name);
END;

$BODY$;

DROP FUNCTION IF EXISTS map.update_lsc_coords;
CREATE OR REPLACE FUNCTION map.update_lsc_coords(
       x_name text,
       x_coords point)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE map.lsc SET coords = x_coords
  where id = (
  select distinct id from map.vm_lsc where device_name = x_name);
END;

$BODY$;

DROP FUNCTION IF EXISTS map.update_segment_path;
CREATE OR REPLACE FUNCTION map.update_segment_path(
       x_name text,
       x_path path)
       RETURNS void
       LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
  UPDATE map.segments SET path = x_path
  where id = (
  select distinct id from map.vm_segments where device_name = x_name);
END;

$BODY$;

-- reset alarm
DROP FUNCTION IF EXISTS map.reset_alarm;
CREATE OR REPLACE FUNCTION map.reset_alarm(x_id integer, x_device_name text, x_tag text)
       RETURNS text AS $$
BEGIN
  RETURN  hardware.reset_alarm(x_id, x_device_name, x_tag);
END;
$$ LANGUAGE plpgsql;

-- hardware reset alarm
DROP FUNCTION IF EXISTS hardware.rest_alarm;
CREATE OR REPLACE FUNCTION hardware.reset_alarm(x_id integer, x_device_name text, x_tag text)
RETURNS text AS $$
BEGIN
RETURN  'ok!';
END;
$$ LANGUAGE plpgsql;

-- logs table
DROP TABLE IF EXISTS map.logs;
CREATE TABLE map.logs(
       id               serial PRIMARY KEY,
       operator         text   NOT NULL,
       create_at        timestamp default now()::timestamp(0),
       event_time       timestamp   NOT NULL,
       event_type       text      NOT NULL,
       event_name       text      NOT NULL,
       tag 			        text      default 'null'
);

-- alarm trigger function
DROP FUNCTION IF EXISTS map.process_alarm;
CREATE OR REPLACE FUNCTION map.process_alarm() RETURNS TRIGGER AS $BODY$
BEGIN
  IF (TG_OP = 'INSERT') THEN
     INSERT INTO map.logs(operator, event_time, event_type, event_name)
         VALUES(user, NEW.time_stamp::timestamp, 'NEW ALARM', NEW.name);
     RETURN NEW;
  ElSIF (TG_OP = 'UPDATE') THEN
     INSERT INTO map.logs(operator, event_time, event_type, event_name, tag)
     VALUES(user, now()::timestamp(0), 'RESET ALARM', NEW.name, NEW.tag);
     RETURN NEW;
  END IF;
  RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

-- create alarm trigger
CREATE TRIGGER process_alarm
AFTER INSERT OR UPDATE ON hardware.alarm
       FOR EACH ROW EXECUTE PROCEDURE map.process_alarm();

-- devices trigger function
DROP FUNCTION IF EXISTS map.process_devices;
CREATE OR REPLACE FUNCTION map.process_devices() RETURNS TRIGGER AS $BODY$
BEGIN
  IF (TG_OP = 'UPDATE') THEN
  	IF (OLD.status != NEW.status) THEN
    	INSERT INTO map.logs(operator, event_time, event_type, event_name)
      VALUES(user, now()::timestamp(0), 'CHANGE STATUS', NEW.type);
    	RETURN NEW;
    END IF;
    IF (OLD.config != NEW.config) THEN
    	INSERT INTO map.logs(operator, event_time, event_type, event_name)
      VALUES(user, now()::timestamp(0), 'CHANGE CONFIG', NEW.type);
    	RETURN NEW;
    END IF;
  END IF;
  RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

-- create module trigger
CREATE TRIGGER process_module
AFTER UPDATE ON hardware.module
       FOR EACH ROW EXECUTE PROCEDURE map.process_devices();

-- create junction trigger
CREATE TRIGGER process_junction
AFTER UPDATE ON hardware.junction
       FOR EACH ROW EXECUTE PROCEDURE map.process_devices();

-- create socket trigger
CREATE TRIGGER process_socket
AFTER UPDATE ON hardware.socket
       FOR EACH ROW EXECUTE PROCEDURE map.process_devices();

-- create terminal trigger
CREATE TRIGGER process_terminal
AFTER UPDATE ON hardware.terminal
       FOR EACH ROW EXECUTE PROCEDURE map.process_devices();
/****************************************
 *   Queries
 ****************************************/
