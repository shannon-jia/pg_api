--
-- temp
--
-- DROP FUNCTION IF EXISTS func_name CASCADE;
-- CREATE OR REPLACE FUNCTION func_name(
--        arg1 integer
--        )
--        RETURNS integer
--        LANGUAGE 'plpgsql'
-- AS $BODY$
-- -- define
-- DECLARE
--   x integer := 0;
-- -- body
-- BEGIN


--   RETURN x;
-- END;

-- $BODY$;


DROP FUNCTION IF EXISTS hardware.query_alarm CASCADE;
CREATE OR REPLACE FUNCTION hardware.query_alarm()
       RETURNS TABLE(model_name text, ratio real)
       LANGUAGE 'plpgsql'
AS $BODY$
-- define
-- DECLARE

-- body
BEGIN
  RETURN QUERY SELECT a.model_name, a.ratio
         FROM hardware.alarm a;
END;

$BODY$;

--
--
--

DROP FUNCTION IF EXISTS print_query CASCADE;
CREATE OR REPLACE FUNCTION print_query(
       arg1 integer
       )
       RETURNS integer
       LANGUAGE 'plpgsql'
AS $BODY$
-- define
DECLARE
  x integer := 0;
  a record;
-- body
BEGIN

  FOR a IN select * from hardware.query_alarm()
  LOOP
    raise notice 'a : %', a;
    raise notice 'model_name: %, ratio: %', a.model_name, a.ratio;
  END LOOP;

  RETURN x;
END;

$BODY$;
