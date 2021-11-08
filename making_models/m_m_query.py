insert_or_update_model = """
UPDATE model_core
SET model_name='{mn}', model_file='{mf}'
WHERE model_core.model_name='{mn}';
INSERT INTO model_core (model_name, model_file)
SELECT '{mn}', '{mf}'
WHERE NOT EXISTS (SELECT 1 
				 FROM model_core as mc 
				 WHERE mc.model_name = '{mn}');
"""


