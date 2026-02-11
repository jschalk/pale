from sqlite3 import Connection as sqlite3_Connection
from src.ch00_py.db_toolbox import (
    create_table2table_agg_insert_query,
    create_update_inconsistency_error_query,
)
from src.ch17_idea.idea_config import get_idea_config_dict, get_quick_ideas_column_ref
from src.ch17_idea.idea_db_tool import create_idea_sorted_table, get_default_sorted_list
from src.ch18_world_etl._ref.ch18_semantic_types import KnotTerm
from src.ch18_world_etl.etl_config import create_prime_tablename

CREATE_PLNAWAR_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title_ERASE TEXT)"""
CREATE_PLNAWAR_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, awardee_title_ERASE_otx TEXT, awardee_title_ERASE_inx TEXT)"""
CREATE_PLNAWAR_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title_ERASE TEXT)"""
CREATE_PLNAWAR_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"""
CREATE_PLNAWAR_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, awardee_title_otx TEXT, awardee_title_inx TEXT, give_force REAL, take_force REAL)"""
CREATE_PLNAWAR_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"""
CREATE_PLNAWAR_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title_ERASE TEXT, error_message TEXT)"""
CREATE_PLNAWAR_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title_ERASE TEXT)"""
CREATE_PLNAWAR_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title_ERASE TEXT)"""
CREATE_PLNAWAR_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"""
CREATE_PLNAWAR_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"""
CREATE_PLNAWAR_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"""
CREATE_PLNCASE_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"""
CREATE_PLNCASE_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_state_ERASE_otx TEXT, reason_state_ERASE_inx TEXT)"""
CREATE_PLNCASE_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"""
CREATE_PLNCASE_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower_otx REAL, reason_lower_inx REAL, reason_upper_otx REAL, reason_upper_inx REAL, reason_divisor INTEGER, context_keg_close TEXT, context_keg_denom TEXT, context_keg_morph TEXT, inx_epoch_diff INTEGER)"""
CREATE_PLNCASE_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_state_otx TEXT, reason_state_inx TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER)"""
CREATE_PLNCASE_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER)"""
CREATE_PLNCASE_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT, error_message TEXT)"""
CREATE_PLNCASE_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"""
CREATE_PLNCASE_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"""
CREATE_PLNCASE_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, error_message TEXT)"""
CREATE_PLNCASE_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, error_message TEXT)"""
CREATE_PLNCASE_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER)"""
CREATE_PLNFACT_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context_ERASE TEXT)"""
CREATE_PLNFACT_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, fact_context_ERASE_otx TEXT, fact_context_ERASE_inx TEXT)"""
CREATE_PLNFACT_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context_ERASE TEXT)"""
CREATE_PLNFACT_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower_otx REAL, fact_lower_inx REAL, fact_upper_otx REAL, fact_upper_inx REAL, context_keg_close TEXT, context_keg_denom TEXT, context_keg_morph TEXT, inx_epoch_diff INTEGER)"""
CREATE_PLNFACT_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, fact_context_otx TEXT, fact_context_inx TEXT, fact_state_otx TEXT, fact_state_inx TEXT, fact_lower REAL, fact_upper REAL)"""
CREATE_PLNFACT_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"""
CREATE_PLNFACT_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context_ERASE TEXT, error_message TEXT)"""
CREATE_PLNFACT_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context_ERASE TEXT)"""
CREATE_PLNFACT_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context_ERASE TEXT)"""
CREATE_PLNFACT_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, error_message TEXT)"""
CREATE_PLNFACT_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, error_message TEXT)"""
CREATE_PLNFACT_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"""
CREATE_PLNHEAL_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name_ERASE TEXT)"""
CREATE_PLNHEAL_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, healer_name_ERASE_otx TEXT, healer_name_ERASE_inx TEXT)"""
CREATE_PLNHEAL_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name_ERASE TEXT)"""
CREATE_PLNHEAL_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name TEXT)"""
CREATE_PLNHEAL_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, healer_name_otx TEXT, healer_name_inx TEXT)"""
CREATE_PLNHEAL_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name TEXT)"""
CREATE_PLNHEAL_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name_ERASE TEXT, error_message TEXT)"""
CREATE_PLNHEAL_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name_ERASE TEXT)"""
CREATE_PLNHEAL_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name_ERASE TEXT)"""
CREATE_PLNHEAL_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name TEXT, error_message TEXT)"""
CREATE_PLNHEAL_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name TEXT, error_message TEXT)"""
CREATE_PLNHEAL_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name TEXT)"""
CREATE_PLNLABO_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title_ERASE TEXT)"""
CREATE_PLNLABO_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, party_title_ERASE_otx TEXT, party_title_ERASE_inx TEXT)"""
CREATE_PLNLABO_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title_ERASE TEXT)"""
CREATE_PLNLABO_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title TEXT, solo INTEGER)"""
CREATE_PLNLABO_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, party_title_otx TEXT, party_title_inx TEXT, solo INTEGER)"""
CREATE_PLNLABO_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title TEXT, solo INTEGER)"""
CREATE_PLNLABO_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title_ERASE TEXT, error_message TEXT)"""
CREATE_PLNLABO_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title_ERASE TEXT)"""
CREATE_PLNLABO_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title_ERASE TEXT)"""
CREATE_PLNLABO_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title TEXT, solo INTEGER, error_message TEXT)"""
CREATE_PLNLABO_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title TEXT, solo INTEGER, error_message TEXT)"""
CREATE_PLNLABO_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title TEXT, solo INTEGER)"""
CREATE_PLNMEMB_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title_ERASE TEXT)"""
CREATE_PLNMEMB_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, group_title_ERASE_otx TEXT, group_title_ERASE_inx TEXT)"""
CREATE_PLNMEMB_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title_ERASE TEXT)"""
CREATE_PLNMEMB_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL)"""
CREATE_PLNMEMB_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, group_title_otx TEXT, group_title_inx TEXT, group_cred_lumen REAL, group_debt_lumen REAL)"""
CREATE_PLNMEMB_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL)"""
CREATE_PLNMEMB_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title_ERASE TEXT, error_message TEXT)"""
CREATE_PLNMEMB_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title_ERASE TEXT)"""
CREATE_PLNMEMB_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title_ERASE TEXT)"""
CREATE_PLNMEMB_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, error_message TEXT)"""
CREATE_PLNMEMB_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, error_message TEXT)"""
CREATE_PLNMEMB_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL)"""
CREATE_PLNKEGG_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope_ERASE TEXT)"""
CREATE_PLNKEGG_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_ERASE_otx TEXT, keg_rope_ERASE_inx TEXT)"""
CREATE_PLNKEGG_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope_ERASE TEXT)"""
CREATE_PLNKEGG_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER)"""
CREATE_PLNKEGG_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER)"""
CREATE_PLNKEGG_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER)"""
CREATE_PLNKEGG_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope_ERASE TEXT, error_message TEXT)"""
CREATE_PLNKEGG_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope_ERASE TEXT)"""
CREATE_PLNKEGG_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope_ERASE TEXT)"""
CREATE_PLNKEGG_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"""
CREATE_PLNKEGG_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"""
CREATE_PLNKEGG_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER)"""
CREATE_PLNREAS_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context_ERASE TEXT)"""
CREATE_PLNREAS_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, reason_context_ERASE_otx TEXT, reason_context_ERASE_inx TEXT)"""
CREATE_PLNREAS_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context_ERASE TEXT)"""
CREATE_PLNREAS_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, active_requisite INTEGER)"""
CREATE_PLNREAS_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, keg_rope_otx TEXT, keg_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, active_requisite INTEGER)"""
CREATE_PLNREAS_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, active_requisite INTEGER)"""
CREATE_PLNREAS_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context_ERASE TEXT, error_message TEXT)"""
CREATE_PLNREAS_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context_ERASE TEXT)"""
CREATE_PLNREAS_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context_ERASE TEXT)"""
CREATE_PLNREAS_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, active_requisite INTEGER, error_message TEXT)"""
CREATE_PLNREAS_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, active_requisite INTEGER, error_message TEXT)"""
CREATE_PLNREAS_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, active_requisite INTEGER)"""
CREATE_PLNUNIT_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name_ERASE TEXT)"""
CREATE_PLNUNIT_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_ERASE_otx TEXT, plan_name_ERASE_inx TEXT)"""
CREATE_PLNUNIT_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name_ERASE TEXT)"""
CREATE_PLNUNIT_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL)"""
CREATE_PLNUNIT_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL)"""
CREATE_PLNUNIT_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL)"""
CREATE_PLNUNIT_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name_ERASE TEXT, error_message TEXT)"""
CREATE_PLNUNIT_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name_ERASE TEXT)"""
CREATE_PLNUNIT_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name_ERASE TEXT)"""
CREATE_PLNUNIT_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, error_message TEXT)"""
CREATE_PLNUNIT_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, error_message TEXT)"""
CREATE_PLNUNIT_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL)"""
CREATE_PLNPRSN_HEARD_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name_ERASE TEXT)"""
CREATE_PLNPRSN_HEARD_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, person_name_ERASE_otx TEXT, person_name_ERASE_inx TEXT)"""
CREATE_PLNPRSN_HEARD_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_h_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name_ERASE TEXT)"""
CREATE_PLNPRSN_HEARD_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, person_cred_lumen REAL, person_debt_lumen REAL)"""
CREATE_PLNPRSN_HEARD_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, person_cred_lumen REAL, person_debt_lumen REAL)"""
CREATE_PLNPRSN_HEARD_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_h_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, person_cred_lumen REAL, person_debt_lumen REAL)"""
CREATE_PLNPRSN_SOUND_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name_ERASE TEXT, error_message TEXT)"""
CREATE_PLNPRSN_SOUND_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name_ERASE TEXT)"""
CREATE_PLNPRSN_SOUND_DEL_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name_ERASE TEXT)"""
CREATE_PLNPRSN_SOUND_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, person_cred_lumen REAL, person_debt_lumen REAL, error_message TEXT)"""
CREATE_PLNPRSN_SOUND_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, person_cred_lumen REAL, person_debt_lumen REAL, error_message TEXT)"""
CREATE_PLNPRSN_SOUND_PUT_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, person_cred_lumen REAL, person_debt_lumen REAL)"""
CREATE_MMTBUDD_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, bud_time_otx INTEGER, bud_time_inx INTEGER, quota REAL, celldepth INTEGER)"""
CREATE_MMTBUDD_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_MMTBUDD_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_h_vld (moment_rope TEXT, plan_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER)"""
CREATE_MMTBUDD_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_MMTBUDD_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_MMTBUDD_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER)"""
CREATE_MMTHOUR_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT)"""
CREATE_MMTHOUR_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, cumulative_minute INTEGER, hour_label_otx TEXT, hour_label_inx TEXT, error_message TEXT)"""
CREATE_MMTHOUR_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_h_vld (moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT)"""
CREATE_MMTHOUR_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_MMTHOUR_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_MMTHOUR_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT)"""
CREATE_MMTMONT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_day INTEGER, month_label TEXT)"""
CREATE_MMTMONT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, cumulative_day INTEGER, month_label_otx TEXT, month_label_inx TEXT, error_message TEXT)"""
CREATE_MMTMONT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_h_vld (moment_rope TEXT, cumulative_day INTEGER, month_label TEXT)"""
CREATE_MMTMONT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_MMTMONT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_MMTMONT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_day INTEGER, month_label TEXT)"""
CREATE_MMTOFFI_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, offi_time_otx INTEGER, offi_time_inx INTEGER)"""
CREATE_MMTOFFI_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_MMTOFFI_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_h_vld (moment_rope TEXT, offi_time INTEGER)"""
CREATE_MMTOFFI_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_MMTOFFI_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_MMTOFFI_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, offi_time INTEGER)"""
CREATE_MMTPAYY_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, tran_time_otx INTEGER, tran_time_inx INTEGER, amount REAL)"""
CREATE_MMTPAYY_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, plan_name_otx TEXT, plan_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_MMTPAYY_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_h_vld (moment_rope TEXT, plan_name TEXT, person_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_MMTPAYY_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_MMTPAYY_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_MMTPAYY_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, plan_name TEXT, person_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_MMTUNIT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER)"""
CREATE_MMTUNIT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, epoch_label_otx TEXT, epoch_label_inx TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_MMTUNIT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_h_vld (moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER)"""
CREATE_MMTUNIT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_MMTUNIT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_MMTUNIT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER)"""
CREATE_MMTWEEK_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_MMTWEEK_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, weekday_order INTEGER, weekday_label_otx TEXT, weekday_label_inx TEXT, error_message TEXT)"""
CREATE_MMTWEEK_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_h_vld (moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_MMTWEEK_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_MMTWEEK_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_MMTWEEK_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_NABTIME_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, otx_time INTEGER, inx_time INTEGER)"""
CREATE_NABTIME_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, otx_time INTEGER, inx_time INTEGER, error_message TEXT)"""
CREATE_NABTIME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, otx_time INTEGER, inx_time INTEGER, error_message TEXT)"""
CREATE_NABTIME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, otx_time INTEGER, inx_time INTEGER, error_message TEXT)"""
CREATE_NABTIME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, otx_time INTEGER, inx_time INTEGER)"""
CREATE_TRLCORE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_agg (face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT)"""
CREATE_TRLCORE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_raw (source_dimen TEXT, face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLCORE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_vld (face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT)"""
CREATE_TRLLABE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_agg (spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLLABE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLLABE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_vld (spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT)"""
CREATE_TRLNAME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_agg (spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLNAME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLNAME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_vld (spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT)"""
CREATE_TRLROPE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_agg (spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLROPE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLROPE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_vld (spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT)"""
CREATE_TRLTITL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_agg (spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLTITL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLTITL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_vld (spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT)"""


def get_prime_create_table_sqlstrs() -> dict[str, str]:
    return {
        "plan_keg_awardunit_h_del_agg": CREATE_PLNAWAR_HEARD_DEL_AGG_SQLSTR,
        "plan_keg_awardunit_h_del_raw": CREATE_PLNAWAR_HEARD_DEL_RAW_SQLSTR,
        "plan_keg_awardunit_h_del_vld": CREATE_PLNAWAR_HEARD_DEL_VLD_SQLSTR,
        "plan_keg_awardunit_h_put_agg": CREATE_PLNAWAR_HEARD_PUT_AGG_SQLSTR,
        "plan_keg_awardunit_h_put_raw": CREATE_PLNAWAR_HEARD_PUT_RAW_SQLSTR,
        "plan_keg_awardunit_h_put_vld": CREATE_PLNAWAR_HEARD_PUT_VLD_SQLSTR,
        "plan_keg_awardunit_s_del_agg": CREATE_PLNAWAR_SOUND_DEL_AGG_SQLSTR,
        "plan_keg_awardunit_s_del_raw": CREATE_PLNAWAR_SOUND_DEL_RAW_SQLSTR,
        "plan_keg_awardunit_s_del_vld": CREATE_PLNAWAR_SOUND_DEL_VLD_SQLSTR,
        "plan_keg_awardunit_s_put_agg": CREATE_PLNAWAR_SOUND_PUT_AGG_SQLSTR,
        "plan_keg_awardunit_s_put_raw": CREATE_PLNAWAR_SOUND_PUT_RAW_SQLSTR,
        "plan_keg_awardunit_s_put_vld": CREATE_PLNAWAR_SOUND_PUT_VLD_SQLSTR,
        "plan_keg_factunit_h_del_agg": CREATE_PLNFACT_HEARD_DEL_AGG_SQLSTR,
        "plan_keg_factunit_h_del_raw": CREATE_PLNFACT_HEARD_DEL_RAW_SQLSTR,
        "plan_keg_factunit_h_del_vld": CREATE_PLNFACT_HEARD_DEL_VLD_SQLSTR,
        "plan_keg_factunit_h_put_agg": CREATE_PLNFACT_HEARD_PUT_AGG_SQLSTR,
        "plan_keg_factunit_h_put_raw": CREATE_PLNFACT_HEARD_PUT_RAW_SQLSTR,
        "plan_keg_factunit_h_put_vld": CREATE_PLNFACT_HEARD_PUT_VLD_SQLSTR,
        "plan_keg_factunit_s_del_agg": CREATE_PLNFACT_SOUND_DEL_AGG_SQLSTR,
        "plan_keg_factunit_s_del_raw": CREATE_PLNFACT_SOUND_DEL_RAW_SQLSTR,
        "plan_keg_factunit_s_del_vld": CREATE_PLNFACT_SOUND_DEL_VLD_SQLSTR,
        "plan_keg_factunit_s_put_agg": CREATE_PLNFACT_SOUND_PUT_AGG_SQLSTR,
        "plan_keg_factunit_s_put_raw": CREATE_PLNFACT_SOUND_PUT_RAW_SQLSTR,
        "plan_keg_factunit_s_put_vld": CREATE_PLNFACT_SOUND_PUT_VLD_SQLSTR,
        "plan_keg_healerunit_h_del_agg": CREATE_PLNHEAL_HEARD_DEL_AGG_SQLSTR,
        "plan_keg_healerunit_h_del_raw": CREATE_PLNHEAL_HEARD_DEL_RAW_SQLSTR,
        "plan_keg_healerunit_h_del_vld": CREATE_PLNHEAL_HEARD_DEL_VLD_SQLSTR,
        "plan_keg_healerunit_h_put_agg": CREATE_PLNHEAL_HEARD_PUT_AGG_SQLSTR,
        "plan_keg_healerunit_h_put_raw": CREATE_PLNHEAL_HEARD_PUT_RAW_SQLSTR,
        "plan_keg_healerunit_h_put_vld": CREATE_PLNHEAL_HEARD_PUT_VLD_SQLSTR,
        "plan_keg_healerunit_s_del_agg": CREATE_PLNHEAL_SOUND_DEL_AGG_SQLSTR,
        "plan_keg_healerunit_s_del_raw": CREATE_PLNHEAL_SOUND_DEL_RAW_SQLSTR,
        "plan_keg_healerunit_s_del_vld": CREATE_PLNHEAL_SOUND_DEL_VLD_SQLSTR,
        "plan_keg_healerunit_s_put_agg": CREATE_PLNHEAL_SOUND_PUT_AGG_SQLSTR,
        "plan_keg_healerunit_s_put_raw": CREATE_PLNHEAL_SOUND_PUT_RAW_SQLSTR,
        "plan_keg_healerunit_s_put_vld": CREATE_PLNHEAL_SOUND_PUT_VLD_SQLSTR,
        "plan_keg_partyunit_h_del_agg": CREATE_PLNLABO_HEARD_DEL_AGG_SQLSTR,
        "plan_keg_partyunit_h_del_raw": CREATE_PLNLABO_HEARD_DEL_RAW_SQLSTR,
        "plan_keg_partyunit_h_del_vld": CREATE_PLNLABO_HEARD_DEL_VLD_SQLSTR,
        "plan_keg_partyunit_h_put_agg": CREATE_PLNLABO_HEARD_PUT_AGG_SQLSTR,
        "plan_keg_partyunit_h_put_raw": CREATE_PLNLABO_HEARD_PUT_RAW_SQLSTR,
        "plan_keg_partyunit_h_put_vld": CREATE_PLNLABO_HEARD_PUT_VLD_SQLSTR,
        "plan_keg_partyunit_s_del_agg": CREATE_PLNLABO_SOUND_DEL_AGG_SQLSTR,
        "plan_keg_partyunit_s_del_raw": CREATE_PLNLABO_SOUND_DEL_RAW_SQLSTR,
        "plan_keg_partyunit_s_del_vld": CREATE_PLNLABO_SOUND_DEL_VLD_SQLSTR,
        "plan_keg_partyunit_s_put_agg": CREATE_PLNLABO_SOUND_PUT_AGG_SQLSTR,
        "plan_keg_partyunit_s_put_raw": CREATE_PLNLABO_SOUND_PUT_RAW_SQLSTR,
        "plan_keg_partyunit_s_put_vld": CREATE_PLNLABO_SOUND_PUT_VLD_SQLSTR,
        "plan_keg_reason_caseunit_h_del_agg": CREATE_PLNCASE_HEARD_DEL_AGG_SQLSTR,
        "plan_keg_reason_caseunit_h_del_raw": CREATE_PLNCASE_HEARD_DEL_RAW_SQLSTR,
        "plan_keg_reason_caseunit_h_del_vld": CREATE_PLNCASE_HEARD_DEL_VLD_SQLSTR,
        "plan_keg_reason_caseunit_h_put_agg": CREATE_PLNCASE_HEARD_PUT_AGG_SQLSTR,
        "plan_keg_reason_caseunit_h_put_raw": CREATE_PLNCASE_HEARD_PUT_RAW_SQLSTR,
        "plan_keg_reason_caseunit_h_put_vld": CREATE_PLNCASE_HEARD_PUT_VLD_SQLSTR,
        "plan_keg_reason_caseunit_s_del_agg": CREATE_PLNCASE_SOUND_DEL_AGG_SQLSTR,
        "plan_keg_reason_caseunit_s_del_raw": CREATE_PLNCASE_SOUND_DEL_RAW_SQLSTR,
        "plan_keg_reason_caseunit_s_del_vld": CREATE_PLNCASE_SOUND_DEL_VLD_SQLSTR,
        "plan_keg_reason_caseunit_s_put_agg": CREATE_PLNCASE_SOUND_PUT_AGG_SQLSTR,
        "plan_keg_reason_caseunit_s_put_raw": CREATE_PLNCASE_SOUND_PUT_RAW_SQLSTR,
        "plan_keg_reason_caseunit_s_put_vld": CREATE_PLNCASE_SOUND_PUT_VLD_SQLSTR,
        "plan_keg_reasonunit_h_del_agg": CREATE_PLNREAS_HEARD_DEL_AGG_SQLSTR,
        "plan_keg_reasonunit_h_del_raw": CREATE_PLNREAS_HEARD_DEL_RAW_SQLSTR,
        "plan_keg_reasonunit_h_del_vld": CREATE_PLNREAS_HEARD_DEL_VLD_SQLSTR,
        "plan_keg_reasonunit_h_put_agg": CREATE_PLNREAS_HEARD_PUT_AGG_SQLSTR,
        "plan_keg_reasonunit_h_put_raw": CREATE_PLNREAS_HEARD_PUT_RAW_SQLSTR,
        "plan_keg_reasonunit_h_put_vld": CREATE_PLNREAS_HEARD_PUT_VLD_SQLSTR,
        "plan_keg_reasonunit_s_del_agg": CREATE_PLNREAS_SOUND_DEL_AGG_SQLSTR,
        "plan_keg_reasonunit_s_del_raw": CREATE_PLNREAS_SOUND_DEL_RAW_SQLSTR,
        "plan_keg_reasonunit_s_del_vld": CREATE_PLNREAS_SOUND_DEL_VLD_SQLSTR,
        "plan_keg_reasonunit_s_put_agg": CREATE_PLNREAS_SOUND_PUT_AGG_SQLSTR,
        "plan_keg_reasonunit_s_put_raw": CREATE_PLNREAS_SOUND_PUT_RAW_SQLSTR,
        "plan_keg_reasonunit_s_put_vld": CREATE_PLNREAS_SOUND_PUT_VLD_SQLSTR,
        "plan_kegunit_h_del_agg": CREATE_PLNKEGG_HEARD_DEL_AGG_SQLSTR,
        "plan_kegunit_h_del_raw": CREATE_PLNKEGG_HEARD_DEL_RAW_SQLSTR,
        "plan_kegunit_h_del_vld": CREATE_PLNKEGG_HEARD_DEL_VLD_SQLSTR,
        "plan_kegunit_h_put_agg": CREATE_PLNKEGG_HEARD_PUT_AGG_SQLSTR,
        "plan_kegunit_h_put_raw": CREATE_PLNKEGG_HEARD_PUT_RAW_SQLSTR,
        "plan_kegunit_h_put_vld": CREATE_PLNKEGG_HEARD_PUT_VLD_SQLSTR,
        "plan_kegunit_s_del_agg": CREATE_PLNKEGG_SOUND_DEL_AGG_SQLSTR,
        "plan_kegunit_s_del_raw": CREATE_PLNKEGG_SOUND_DEL_RAW_SQLSTR,
        "plan_kegunit_s_del_vld": CREATE_PLNKEGG_SOUND_DEL_VLD_SQLSTR,
        "plan_kegunit_s_put_agg": CREATE_PLNKEGG_SOUND_PUT_AGG_SQLSTR,
        "plan_kegunit_s_put_raw": CREATE_PLNKEGG_SOUND_PUT_RAW_SQLSTR,
        "plan_kegunit_s_put_vld": CREATE_PLNKEGG_SOUND_PUT_VLD_SQLSTR,
        "plan_person_membership_h_del_agg": CREATE_PLNMEMB_HEARD_DEL_AGG_SQLSTR,
        "plan_person_membership_h_del_raw": CREATE_PLNMEMB_HEARD_DEL_RAW_SQLSTR,
        "plan_person_membership_h_del_vld": CREATE_PLNMEMB_HEARD_DEL_VLD_SQLSTR,
        "plan_person_membership_h_put_agg": CREATE_PLNMEMB_HEARD_PUT_AGG_SQLSTR,
        "plan_person_membership_h_put_raw": CREATE_PLNMEMB_HEARD_PUT_RAW_SQLSTR,
        "plan_person_membership_h_put_vld": CREATE_PLNMEMB_HEARD_PUT_VLD_SQLSTR,
        "plan_person_membership_s_del_agg": CREATE_PLNMEMB_SOUND_DEL_AGG_SQLSTR,
        "plan_person_membership_s_del_raw": CREATE_PLNMEMB_SOUND_DEL_RAW_SQLSTR,
        "plan_person_membership_s_del_vld": CREATE_PLNMEMB_SOUND_DEL_VLD_SQLSTR,
        "plan_person_membership_s_put_agg": CREATE_PLNMEMB_SOUND_PUT_AGG_SQLSTR,
        "plan_person_membership_s_put_raw": CREATE_PLNMEMB_SOUND_PUT_RAW_SQLSTR,
        "plan_person_membership_s_put_vld": CREATE_PLNMEMB_SOUND_PUT_VLD_SQLSTR,
        "plan_personunit_h_del_agg": CREATE_PLNPRSN_HEARD_DEL_AGG_SQLSTR,
        "plan_personunit_h_del_raw": CREATE_PLNPRSN_HEARD_DEL_RAW_SQLSTR,
        "plan_personunit_h_del_vld": CREATE_PLNPRSN_HEARD_DEL_VLD_SQLSTR,
        "plan_personunit_h_put_agg": CREATE_PLNPRSN_HEARD_PUT_AGG_SQLSTR,
        "plan_personunit_h_put_raw": CREATE_PLNPRSN_HEARD_PUT_RAW_SQLSTR,
        "plan_personunit_h_put_vld": CREATE_PLNPRSN_HEARD_PUT_VLD_SQLSTR,
        "plan_personunit_s_del_agg": CREATE_PLNPRSN_SOUND_DEL_AGG_SQLSTR,
        "plan_personunit_s_del_raw": CREATE_PLNPRSN_SOUND_DEL_RAW_SQLSTR,
        "plan_personunit_s_del_vld": CREATE_PLNPRSN_SOUND_DEL_VLD_SQLSTR,
        "plan_personunit_s_put_agg": CREATE_PLNPRSN_SOUND_PUT_AGG_SQLSTR,
        "plan_personunit_s_put_raw": CREATE_PLNPRSN_SOUND_PUT_RAW_SQLSTR,
        "plan_personunit_s_put_vld": CREATE_PLNPRSN_SOUND_PUT_VLD_SQLSTR,
        "planunit_h_del_agg": CREATE_PLNUNIT_HEARD_DEL_AGG_SQLSTR,
        "planunit_h_del_raw": CREATE_PLNUNIT_HEARD_DEL_RAW_SQLSTR,
        "planunit_h_del_vld": CREATE_PLNUNIT_HEARD_DEL_VLD_SQLSTR,
        "planunit_h_put_agg": CREATE_PLNUNIT_HEARD_PUT_AGG_SQLSTR,
        "planunit_h_put_raw": CREATE_PLNUNIT_HEARD_PUT_RAW_SQLSTR,
        "planunit_h_put_vld": CREATE_PLNUNIT_HEARD_PUT_VLD_SQLSTR,
        "planunit_s_del_agg": CREATE_PLNUNIT_SOUND_DEL_AGG_SQLSTR,
        "planunit_s_del_raw": CREATE_PLNUNIT_SOUND_DEL_RAW_SQLSTR,
        "planunit_s_del_vld": CREATE_PLNUNIT_SOUND_DEL_VLD_SQLSTR,
        "planunit_s_put_agg": CREATE_PLNUNIT_SOUND_PUT_AGG_SQLSTR,
        "planunit_s_put_raw": CREATE_PLNUNIT_SOUND_PUT_RAW_SQLSTR,
        "planunit_s_put_vld": CREATE_PLNUNIT_SOUND_PUT_VLD_SQLSTR,
        "moment_budunit_h_agg": CREATE_MMTBUDD_HEARD_AGG_SQLSTR,
        "moment_budunit_h_raw": CREATE_MMTBUDD_HEARD_RAW_SQLSTR,
        "moment_budunit_h_vld": CREATE_MMTBUDD_HEARD_VLD_SQLSTR,
        "moment_budunit_s_agg": CREATE_MMTBUDD_SOUND_AGG_SQLSTR,
        "moment_budunit_s_raw": CREATE_MMTBUDD_SOUND_RAW_SQLSTR,
        "moment_budunit_s_vld": CREATE_MMTBUDD_SOUND_VLD_SQLSTR,
        "moment_epoch_hour_h_agg": CREATE_MMTHOUR_HEARD_AGG_SQLSTR,
        "moment_epoch_hour_h_raw": CREATE_MMTHOUR_HEARD_RAW_SQLSTR,
        "moment_epoch_hour_h_vld": CREATE_MMTHOUR_HEARD_VLD_SQLSTR,
        "moment_epoch_hour_s_agg": CREATE_MMTHOUR_SOUND_AGG_SQLSTR,
        "moment_epoch_hour_s_raw": CREATE_MMTHOUR_SOUND_RAW_SQLSTR,
        "moment_epoch_hour_s_vld": CREATE_MMTHOUR_SOUND_VLD_SQLSTR,
        "moment_epoch_month_h_agg": CREATE_MMTMONT_HEARD_AGG_SQLSTR,
        "moment_epoch_month_h_raw": CREATE_MMTMONT_HEARD_RAW_SQLSTR,
        "moment_epoch_month_h_vld": CREATE_MMTMONT_HEARD_VLD_SQLSTR,
        "moment_epoch_month_s_agg": CREATE_MMTMONT_SOUND_AGG_SQLSTR,
        "moment_epoch_month_s_raw": CREATE_MMTMONT_SOUND_RAW_SQLSTR,
        "moment_epoch_month_s_vld": CREATE_MMTMONT_SOUND_VLD_SQLSTR,
        "moment_epoch_weekday_h_agg": CREATE_MMTWEEK_HEARD_AGG_SQLSTR,
        "moment_epoch_weekday_h_raw": CREATE_MMTWEEK_HEARD_RAW_SQLSTR,
        "moment_epoch_weekday_h_vld": CREATE_MMTWEEK_HEARD_VLD_SQLSTR,
        "moment_epoch_weekday_s_agg": CREATE_MMTWEEK_SOUND_AGG_SQLSTR,
        "moment_epoch_weekday_s_raw": CREATE_MMTWEEK_SOUND_RAW_SQLSTR,
        "moment_epoch_weekday_s_vld": CREATE_MMTWEEK_SOUND_VLD_SQLSTR,
        "moment_paybook_h_agg": CREATE_MMTPAYY_HEARD_AGG_SQLSTR,
        "moment_paybook_h_raw": CREATE_MMTPAYY_HEARD_RAW_SQLSTR,
        "moment_paybook_h_vld": CREATE_MMTPAYY_HEARD_VLD_SQLSTR,
        "moment_paybook_s_agg": CREATE_MMTPAYY_SOUND_AGG_SQLSTR,
        "moment_paybook_s_raw": CREATE_MMTPAYY_SOUND_RAW_SQLSTR,
        "moment_paybook_s_vld": CREATE_MMTPAYY_SOUND_VLD_SQLSTR,
        "moment_timeoffi_h_agg": CREATE_MMTOFFI_HEARD_AGG_SQLSTR,
        "moment_timeoffi_h_raw": CREATE_MMTOFFI_HEARD_RAW_SQLSTR,
        "moment_timeoffi_h_vld": CREATE_MMTOFFI_HEARD_VLD_SQLSTR,
        "moment_timeoffi_s_agg": CREATE_MMTOFFI_SOUND_AGG_SQLSTR,
        "moment_timeoffi_s_raw": CREATE_MMTOFFI_SOUND_RAW_SQLSTR,
        "moment_timeoffi_s_vld": CREATE_MMTOFFI_SOUND_VLD_SQLSTR,
        "momentunit_h_agg": CREATE_MMTUNIT_HEARD_AGG_SQLSTR,
        "momentunit_h_raw": CREATE_MMTUNIT_HEARD_RAW_SQLSTR,
        "momentunit_h_vld": CREATE_MMTUNIT_HEARD_VLD_SQLSTR,
        "momentunit_s_agg": CREATE_MMTUNIT_SOUND_AGG_SQLSTR,
        "momentunit_s_raw": CREATE_MMTUNIT_SOUND_RAW_SQLSTR,
        "momentunit_s_vld": CREATE_MMTUNIT_SOUND_VLD_SQLSTR,
        "nabu_timenum_h_agg": CREATE_NABTIME_HEARD_AGG_SQLSTR,
        "nabu_timenum_h_raw": CREATE_NABTIME_HEARD_RAW_SQLSTR,
        "nabu_timenum_s_agg": CREATE_NABTIME_SOUND_AGG_SQLSTR,
        "nabu_timenum_s_raw": CREATE_NABTIME_SOUND_RAW_SQLSTR,
        "nabu_timenum_s_vld": CREATE_NABTIME_SOUND_VLD_SQLSTR,
        "translate_core_s_agg": CREATE_TRLCORE_SOUND_AGG_SQLSTR,
        "translate_core_s_raw": CREATE_TRLCORE_SOUND_RAW_SQLSTR,
        "translate_core_s_vld": CREATE_TRLCORE_SOUND_VLD_SQLSTR,
        "translate_label_s_agg": CREATE_TRLLABE_SOUND_AGG_SQLSTR,
        "translate_label_s_raw": CREATE_TRLLABE_SOUND_RAW_SQLSTR,
        "translate_label_s_vld": CREATE_TRLLABE_SOUND_VLD_SQLSTR,
        "translate_name_s_agg": CREATE_TRLNAME_SOUND_AGG_SQLSTR,
        "translate_name_s_raw": CREATE_TRLNAME_SOUND_RAW_SQLSTR,
        "translate_name_s_vld": CREATE_TRLNAME_SOUND_VLD_SQLSTR,
        "translate_rope_s_agg": CREATE_TRLROPE_SOUND_AGG_SQLSTR,
        "translate_rope_s_raw": CREATE_TRLROPE_SOUND_RAW_SQLSTR,
        "translate_rope_s_vld": CREATE_TRLROPE_SOUND_VLD_SQLSTR,
        "translate_title_s_agg": CREATE_TRLTITL_SOUND_AGG_SQLSTR,
        "translate_title_s_raw": CREATE_TRLTITL_SOUND_RAW_SQLSTR,
        "translate_title_s_vld": CREATE_TRLTITL_SOUND_VLD_SQLSTR,
    }


def get_moment_plan_sound_agg_tablenames():
    return {
        "plan_person_membership_s_del_agg",
        "plan_person_membership_s_put_agg",
        "plan_personunit_s_del_agg",
        "plan_personunit_s_put_agg",
        "plan_keg_awardunit_s_del_agg",
        "plan_keg_awardunit_s_put_agg",
        "plan_keg_factunit_s_del_agg",
        "plan_keg_factunit_s_put_agg",
        "plan_keg_healerunit_s_del_agg",
        "plan_keg_healerunit_s_put_agg",
        "plan_keg_partyunit_s_del_agg",
        "plan_keg_partyunit_s_put_agg",
        "plan_keg_reason_caseunit_s_del_agg",
        "plan_keg_reason_caseunit_s_put_agg",
        "plan_keg_reasonunit_s_del_agg",
        "plan_keg_reasonunit_s_put_agg",
        "plan_kegunit_s_del_agg",
        "plan_kegunit_s_put_agg",
        "planunit_s_del_agg",
        "planunit_s_put_agg",
        "moment_paybook_s_agg",
        "moment_budunit_s_agg",
        "moment_epoch_hour_s_agg",
        "moment_epoch_month_s_agg",
        "moment_epoch_weekday_s_agg",
        "moment_timeoffi_s_agg",
        "momentunit_s_agg",
        "nabu_timenum_s_agg",
    }


def get_plan_heard_vld_tablenames() -> set[str]:
    return {
        "planunit_h_put_vld",
        "plan_keg_healerunit_h_put_vld",
        "plan_personunit_h_put_vld",
        "plan_keg_reason_caseunit_h_put_vld",
        "plan_keg_partyunit_h_put_vld",
        "plan_keg_reasonunit_h_put_vld",
        "plan_keg_factunit_h_put_vld",
        "plan_person_membership_h_put_vld",
        "plan_kegunit_h_put_vld",
        "plan_keg_awardunit_h_put_vld",
    }


def create_sound_and_heard_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_prime_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_all_idea_tables(conn_or_cursor: sqlite3_Connection):
    idea_refs = get_quick_ideas_column_ref()
    for idea_number, idea_columns in idea_refs.items():
        x_tablename = f"{idea_number}_raw"
        create_idea_sorted_table(conn_or_cursor, x_tablename, idea_columns)


def create_sound_raw_update_inconsist_error_message_sqlstr(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    if dimen.lower().startswith("moment") or dimen.lower().startswith("nabu"):
        exclude_cols = {"idea_number", "spark_num", "face_name", "error_message"}
    else:
        exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("plan"):
        x_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        x_tablename = create_prime_tablename(dimen, "s", "raw")
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())
    return create_update_inconsistency_error_query(
        conn_or_cursor=conn_or_cursor,
        x_tablename=x_tablename,
        focus_columns=dimen_focus_columns,
        exclude_columns=exclude_cols,
        error_holder_column="error_message",
        error_str="Inconsistent data",
    )


def create_sound_agg_insert_sqlstrs(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())

    if dimen.lower().startswith("moment"):
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("plan"):
        agg_tablename = create_prime_tablename(dimen, "s", "agg", "put")
        raw_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        raw_tablename = create_prime_tablename(dimen, "s", "raw")
        agg_tablename = create_prime_tablename(dimen, "s", "agg")

    translate_moment_plan_put_sqlstr = create_table2table_agg_insert_query(
        conn_or_cursor,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
        where_block="WHERE error_message IS NULL",
    )
    sqlstrs = [translate_moment_plan_put_sqlstr]
    if dimen.lower().startswith("plan"):
        del_raw_tablename = create_prime_tablename(dimen, "s", "raw", "del")
        del_agg_tablename = create_prime_tablename(dimen, "s", "agg", "del")
        dimen_focus_columns = get_default_sorted_list(set(dimen_focus_columns))
        last_element = dimen_focus_columns.pop(-1)
        dimen_focus_columns.append(f"{last_element}_ERASE")
        plan_del_sqlstr = create_table2table_agg_insert_query(
            conn_or_cursor,
            src_table=del_raw_tablename,
            dst_table=del_agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
            where_block="",
        )
        sqlstrs.append(plan_del_sqlstr)

    return sqlstrs


def create_insert_into_translate_core_raw_sqlstr(dimen: str) -> str:
    translate_core_s_raw_tablename = create_prime_tablename("trlcore", "s", "raw")
    translate_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    return f"""INSERT INTO {translate_core_s_raw_tablename} (source_dimen, face_name, otx_knot, inx_knot, unknown_str)
SELECT '{translate_s_agg_tablename}', face_name, otx_knot, inx_knot, unknown_str
FROM {translate_s_agg_tablename}
GROUP BY face_name, otx_knot, inx_knot, unknown_str
;
"""


def create_insert_translate_core_agg_into_vld_sqlstr(
    default_knot: KnotTerm, default_unknown: str
):
    return f"""INSERT INTO translate_core_s_vld (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  face_name
, IFNULL(otx_knot, '{default_knot}')
, IFNULL(inx_knot, '{default_knot}')
, IFNULL(unknown_str, '{default_unknown}')
FROM translate_core_s_agg
;
"""


def create_insert_missing_face_name_into_translate_core_vld_sqlstr(
    default_knot: KnotTerm, default_unknown: str, moment_plan_sound_agg_tablename: str
):
    return f"""INSERT INTO translate_core_s_vld (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  {moment_plan_sound_agg_tablename}.face_name
, '{default_knot}'
, '{default_knot}'
, '{default_unknown}'
FROM {moment_plan_sound_agg_tablename} 
LEFT JOIN translate_core_s_vld ON translate_core_s_vld.face_name = {moment_plan_sound_agg_tablename}.face_name
WHERE translate_core_s_vld.face_name IS NULL
GROUP BY {moment_plan_sound_agg_tablename}.face_name
;
"""


def create_update_translate_sound_agg_inconsist_sqlstr(dimen: str) -> str:
    translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    translate_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    return f"""UPDATE {translate_s_agg_tablename}
SET error_message = 'Inconsistent translate core data'
WHERE face_name IN (
    SELECT {translate_s_agg_tablename}.face_name
    FROM {translate_s_agg_tablename} 
    LEFT JOIN {translate_core_s_vld_tablename} ON {translate_core_s_vld_tablename}.face_name = {translate_s_agg_tablename}.face_name
    WHERE {translate_core_s_vld_tablename}.face_name IS NULL
)
;
"""


def create_update_trllabe_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    trllabe_s_agg_tablename = create_prime_tablename("trllabe", "s", "agg")
    return f"""UPDATE {trllabe_s_agg_tablename}
SET error_message = 'Knot cannot exist in LabelTerm'
WHERE rowid IN (
    SELECT label_agg.rowid
    FROM {trllabe_s_agg_tablename} label_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = label_agg.face_name
    WHERE label_agg.otx_label LIKE '%' || core_vld.otx_knot || '%'
      OR label_agg.inx_label LIKE '%' || core_vld.inx_knot || '%'
)
;
"""


def create_update_trlrope_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    trlrope_s_agg_tablename = create_prime_tablename("trlrope", "s", "agg")
    return f"""UPDATE {trlrope_s_agg_tablename}
SET error_message = 'Knot must exist in RopeTerm'
WHERE rowid IN (
    SELECT rope_agg.rowid
    FROM {trlrope_s_agg_tablename} rope_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = rope_agg.face_name
    WHERE NOT rope_agg.otx_rope LIKE core_vld.otx_knot || '%'
        OR NOT rope_agg.inx_rope LIKE core_vld.inx_knot || '%'
)
;
"""


def create_update_trlname_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    trlname_s_agg_tablename = create_prime_tablename("trlname", "s", "agg")
    return f"""UPDATE {trlname_s_agg_tablename}
SET error_message = 'Knot cannot exist in NameTerm'
WHERE rowid IN (
    SELECT name_agg.rowid
    FROM {trlname_s_agg_tablename} name_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = name_agg.face_name
    WHERE name_agg.otx_name LIKE '%' || core_vld.otx_knot || '%'
      OR name_agg.inx_name LIKE '%' || core_vld.inx_knot || '%'
)
;
"""


def create_update_trltitl_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    trltitl_s_agg_tablename = create_prime_tablename("trltitl", "s", "agg")
    return f"""UPDATE {trltitl_s_agg_tablename}
SET error_message = 'Otx and inx titles must match knot.'
WHERE rowid IN (
  SELECT title_agg.rowid
  FROM {trltitl_s_agg_tablename} title_agg
  JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = title_agg.face_name
  WHERE NOT ((
            title_agg.otx_title LIKE core_vld.otx_knot || '%' 
        AND title_agg.inx_title LIKE core_vld.inx_knot || '%') 
      OR (
            NOT title_agg.otx_title LIKE core_vld.otx_knot || '%'
        AND NOT title_agg.inx_title LIKE core_vld.inx_knot || '%'
        ))
)
;
"""


def create_insert_translate_sound_vld_table_sqlstr(dimen: str) -> str:
    translate_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    translate_s_vld_tablename = create_prime_tablename(dimen, "s", "vld")
    dimen_otx_inx_obj_names = {
        "translate_name": "name",
        "translate_title": "title",
        "translate_label": "label",
        "translate_rope": "rope",
    }
    otx_str = f"otx_{dimen_otx_inx_obj_names.get(dimen, dimen)}"
    inx_str = f"inx_{dimen_otx_inx_obj_names.get(dimen, dimen)}"
    return f"""
INSERT INTO {translate_s_vld_tablename} (spark_num, face_name, {otx_str}, {inx_str})
SELECT spark_num, face_name, MAX({otx_str}), MAX({inx_str})
FROM {translate_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY spark_num, face_name
;
"""


def create_knot_exists_in_name_error_update_sqlstr(table: str, column: str) -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    return f"""UPDATE {table}
SET error_message = 'Knot cannot exist in NameTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_knot || '%'
)
;
"""


def create_knot_exists_in_label_error_update_sqlstr(table: str, column: str) -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    return f"""UPDATE {table}
SET error_message = 'Knot cannot exist in LabelTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_knot || '%'
)
;
"""


INSERT_PLNMEMB_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_person_membership_s_put_vld (spark_num, face_name, moment_rope, plan_name, person_name, group_title, group_cred_lumen, group_debt_lumen) SELECT spark_num, face_name, moment_rope, plan_name, person_name, group_title, group_cred_lumen, group_debt_lumen FROM plan_person_membership_s_put_agg WHERE error_message IS NULL"
INSERT_PLNMEMB_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_person_membership_s_del_vld (spark_num, face_name, moment_rope, plan_name, person_name, group_title_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, person_name, group_title_ERASE FROM plan_person_membership_s_del_agg WHERE error_message IS NULL"
INSERT_PLNPRSN_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_personunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, person_name, person_cred_lumen, person_debt_lumen) SELECT spark_num, face_name, moment_rope, plan_name, person_name, person_cred_lumen, person_debt_lumen FROM plan_personunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNPRSN_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_personunit_s_del_vld (spark_num, face_name, moment_rope, plan_name, person_name_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, person_name_ERASE FROM plan_personunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNAWAR_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_keg_awardunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title, give_force, take_force) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title, give_force, take_force FROM plan_keg_awardunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNAWAR_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_keg_awardunit_s_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title_ERASE FROM plan_keg_awardunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNFACT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_keg_factunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context, fact_state, fact_lower, fact_upper) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context, fact_state, fact_lower, fact_upper FROM plan_keg_factunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNFACT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_keg_factunit_s_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context_ERASE FROM plan_keg_factunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNHEAL_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_keg_healerunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name FROM plan_keg_healerunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNHEAL_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_keg_healerunit_s_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name_ERASE FROM plan_keg_healerunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNCASE_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_keg_reason_caseunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor FROM plan_keg_reason_caseunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNCASE_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_keg_reason_caseunit_s_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state_ERASE FROM plan_keg_reason_caseunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNREAS_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_keg_reasonunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, active_requisite) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, active_requisite FROM plan_keg_reasonunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNREAS_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_keg_reasonunit_s_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context_ERASE FROM plan_keg_reasonunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNLABO_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_keg_partyunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, party_title, solo) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, party_title, solo FROM plan_keg_partyunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNLABO_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_keg_partyunit_s_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, party_title_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, party_title_ERASE FROM plan_keg_partyunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNKEGG_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_kegunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool FROM plan_kegunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNKEGG_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_kegunit_s_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope_ERASE) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope_ERASE FROM plan_kegunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNUNIT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO planunit_s_put_vld (spark_num, face_name, moment_rope, plan_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain) SELECT spark_num, face_name, moment_rope, plan_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain FROM planunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNUNIT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO planunit_s_del_vld (spark_num, face_name, moment_rope, plan_name_ERASE) SELECT spark_num, face_name, moment_rope, plan_name_ERASE FROM planunit_s_del_agg WHERE error_message IS NULL"

INSERT_MMTPAYY_SOUND_VLD_SQLSTR = "INSERT INTO moment_paybook_s_vld (spark_num, face_name, moment_rope, plan_name, person_name, tran_time, amount) SELECT spark_num, face_name, moment_rope, plan_name, person_name, tran_time, amount FROM moment_paybook_s_agg WHERE error_message IS NULL"
INSERT_MMTBUDD_SOUND_VLD_SQLSTR = "INSERT INTO moment_budunit_s_vld (spark_num, face_name, moment_rope, plan_name, bud_time, quota, celldepth) SELECT spark_num, face_name, moment_rope, plan_name, bud_time, quota, celldepth FROM moment_budunit_s_agg WHERE error_message IS NULL"
INSERT_MMTHOUR_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_hour_s_vld (spark_num, face_name, moment_rope, cumulative_minute, hour_label) SELECT spark_num, face_name, moment_rope, cumulative_minute, hour_label FROM moment_epoch_hour_s_agg WHERE error_message IS NULL"
INSERT_MMTMONT_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_month_s_vld (spark_num, face_name, moment_rope, cumulative_day, month_label) SELECT spark_num, face_name, moment_rope, cumulative_day, month_label FROM moment_epoch_month_s_agg WHERE error_message IS NULL"
INSERT_MMTWEEK_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_weekday_s_vld (spark_num, face_name, moment_rope, weekday_order, weekday_label) SELECT spark_num, face_name, moment_rope, weekday_order, weekday_label FROM moment_epoch_weekday_s_agg WHERE error_message IS NULL"
INSERT_MMTOFFI_SOUND_VLD_SQLSTR = "INSERT INTO moment_timeoffi_s_vld (spark_num, face_name, moment_rope, offi_time) SELECT spark_num, face_name, moment_rope, offi_time FROM moment_timeoffi_s_agg WHERE error_message IS NULL"
INSERT_MMTUNIT_SOUND_VLD_SQLSTR = "INSERT INTO momentunit_s_vld (spark_num, face_name, moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations) SELECT spark_num, face_name, moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations FROM momentunit_s_agg WHERE error_message IS NULL"

INSERT_NABTIME_SOUND_VLD_SQLSTR = "INSERT INTO nabu_timenum_s_vld (spark_num, face_name, moment_rope, otx_time, inx_time) SELECT spark_num, face_name, moment_rope, otx_time, inx_time FROM nabu_timenum_s_agg WHERE error_message IS NULL"


def get_insert_into_sound_vld_sqlstrs() -> dict[str, str]:
    return {
        "plan_person_membership_s_put_vld": INSERT_PLNMEMB_SOUND_VLD_PUT_SQLSTR,
        "plan_person_membership_s_del_vld": INSERT_PLNMEMB_SOUND_VLD_DEL_SQLSTR,
        "plan_personunit_s_put_vld": INSERT_PLNPRSN_SOUND_VLD_PUT_SQLSTR,
        "plan_personunit_s_del_vld": INSERT_PLNPRSN_SOUND_VLD_DEL_SQLSTR,
        "plan_keg_awardunit_s_put_vld": INSERT_PLNAWAR_SOUND_VLD_PUT_SQLSTR,
        "plan_keg_awardunit_s_del_vld": INSERT_PLNAWAR_SOUND_VLD_DEL_SQLSTR,
        "plan_keg_factunit_s_put_vld": INSERT_PLNFACT_SOUND_VLD_PUT_SQLSTR,
        "plan_keg_factunit_s_del_vld": INSERT_PLNFACT_SOUND_VLD_DEL_SQLSTR,
        "plan_keg_healerunit_s_put_vld": INSERT_PLNHEAL_SOUND_VLD_PUT_SQLSTR,
        "plan_keg_healerunit_s_del_vld": INSERT_PLNHEAL_SOUND_VLD_DEL_SQLSTR,
        "plan_keg_reason_caseunit_s_put_vld": INSERT_PLNCASE_SOUND_VLD_PUT_SQLSTR,
        "plan_keg_reason_caseunit_s_del_vld": INSERT_PLNCASE_SOUND_VLD_DEL_SQLSTR,
        "plan_keg_reasonunit_s_put_vld": INSERT_PLNREAS_SOUND_VLD_PUT_SQLSTR,
        "plan_keg_reasonunit_s_del_vld": INSERT_PLNREAS_SOUND_VLD_DEL_SQLSTR,
        "plan_keg_partyunit_s_put_vld": INSERT_PLNLABO_SOUND_VLD_PUT_SQLSTR,
        "plan_keg_partyunit_s_del_vld": INSERT_PLNLABO_SOUND_VLD_DEL_SQLSTR,
        "plan_kegunit_s_put_vld": INSERT_PLNKEGG_SOUND_VLD_PUT_SQLSTR,
        "plan_kegunit_s_del_vld": INSERT_PLNKEGG_SOUND_VLD_DEL_SQLSTR,
        "planunit_s_put_vld": INSERT_PLNUNIT_SOUND_VLD_PUT_SQLSTR,
        "planunit_s_del_vld": INSERT_PLNUNIT_SOUND_VLD_DEL_SQLSTR,
        "moment_paybook_s_vld": INSERT_MMTPAYY_SOUND_VLD_SQLSTR,
        "moment_budunit_s_vld": INSERT_MMTBUDD_SOUND_VLD_SQLSTR,
        "moment_epoch_hour_s_vld": INSERT_MMTHOUR_SOUND_VLD_SQLSTR,
        "moment_epoch_month_s_vld": INSERT_MMTMONT_SOUND_VLD_SQLSTR,
        "moment_epoch_weekday_s_vld": INSERT_MMTWEEK_SOUND_VLD_SQLSTR,
        "moment_timeoffi_s_vld": INSERT_MMTOFFI_SOUND_VLD_SQLSTR,
        "momentunit_s_vld": INSERT_MMTUNIT_SOUND_VLD_SQLSTR,
        "nabu_timenum_s_vld": INSERT_NABTIME_SOUND_VLD_SQLSTR,
    }


INSERT_MMTPAYY_HEARD_RAW_SQLSTR = "INSERT INTO moment_paybook_h_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, person_name_otx, tran_time, amount) SELECT spark_num, face_name, moment_rope, plan_name, person_name, tran_time, amount FROM moment_paybook_s_vld "
INSERT_MMTBUDD_HEARD_RAW_SQLSTR = "INSERT INTO moment_budunit_h_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, bud_time, quota, celldepth) SELECT spark_num, face_name, moment_rope, plan_name, bud_time, quota, celldepth FROM moment_budunit_s_vld "
INSERT_MMTHOUR_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_hour_h_raw (spark_num, face_name_otx, moment_rope_otx, cumulative_minute, hour_label_otx) SELECT spark_num, face_name, moment_rope, cumulative_minute, hour_label FROM moment_epoch_hour_s_vld "
INSERT_MMTMONT_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_month_h_raw (spark_num, face_name_otx, moment_rope_otx, cumulative_day, month_label_otx) SELECT spark_num, face_name, moment_rope, cumulative_day, month_label FROM moment_epoch_month_s_vld "
INSERT_MMTWEEK_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_weekday_h_raw (spark_num, face_name_otx, moment_rope_otx, weekday_order, weekday_label_otx) SELECT spark_num, face_name, moment_rope, weekday_order, weekday_label FROM moment_epoch_weekday_s_vld "
INSERT_MMTOFFI_HEARD_RAW_SQLSTR = "INSERT INTO moment_timeoffi_h_raw (spark_num, face_name_otx, moment_rope_otx, offi_time) SELECT spark_num, face_name, moment_rope, offi_time FROM moment_timeoffi_s_vld "
INSERT_MMTUNIT_HEARD_RAW_SQLSTR = "INSERT INTO momentunit_h_raw (spark_num, face_name_otx, moment_rope_otx, epoch_label_otx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations) SELECT spark_num, face_name, moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations FROM momentunit_s_vld "

INSERT_PLNMEMB_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_person_membership_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, person_name_otx, group_title_otx, group_cred_lumen, group_debt_lumen) SELECT spark_num, face_name, moment_rope, plan_name, person_name, group_title, group_cred_lumen, group_debt_lumen FROM plan_person_membership_s_put_vld "
INSERT_PLNMEMB_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_person_membership_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, person_name_otx, group_title_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, person_name, group_title_ERASE FROM plan_person_membership_s_del_vld "
INSERT_PLNPRSN_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_personunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, person_name_otx, person_cred_lumen, person_debt_lumen) SELECT spark_num, face_name, moment_rope, plan_name, person_name, person_cred_lumen, person_debt_lumen FROM plan_personunit_s_put_vld "
INSERT_PLNPRSN_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_personunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, person_name_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, person_name_ERASE FROM plan_personunit_s_del_vld "
INSERT_PLNAWAR_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_keg_awardunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, awardee_title_otx, give_force, take_force) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title, give_force, take_force FROM plan_keg_awardunit_s_put_vld "
INSERT_PLNAWAR_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_keg_awardunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, awardee_title_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title_ERASE FROM plan_keg_awardunit_s_del_vld "
INSERT_PLNFACT_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_keg_factunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, fact_context_otx, fact_state_otx, fact_lower, fact_upper) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context, fact_state, fact_lower, fact_upper FROM plan_keg_factunit_s_put_vld "
INSERT_PLNFACT_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_keg_factunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, fact_context_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context_ERASE FROM plan_keg_factunit_s_del_vld "
INSERT_PLNHEAL_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_keg_healerunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, healer_name_otx) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name FROM plan_keg_healerunit_s_put_vld "
INSERT_PLNHEAL_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_keg_healerunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, healer_name_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name_ERASE FROM plan_keg_healerunit_s_del_vld "
INSERT_PLNCASE_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_keg_reason_caseunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, reason_context_otx, reason_state_otx, reason_lower, reason_upper, reason_divisor) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor FROM plan_keg_reason_caseunit_s_put_vld "
INSERT_PLNCASE_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_keg_reason_caseunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, reason_context_otx, reason_state_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state_ERASE FROM plan_keg_reason_caseunit_s_del_vld "
INSERT_PLNREAS_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_keg_reasonunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, reason_context_otx, active_requisite) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, active_requisite FROM plan_keg_reasonunit_s_put_vld "
INSERT_PLNREAS_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_keg_reasonunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, reason_context_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context_ERASE FROM plan_keg_reasonunit_s_del_vld "
INSERT_PLNLABO_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_keg_partyunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, party_title_otx, solo) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, party_title, solo FROM plan_keg_partyunit_s_put_vld "
INSERT_PLNLABO_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_keg_partyunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, party_title_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, party_title_ERASE FROM plan_keg_partyunit_s_del_vld "
INSERT_PLNKEGG_HEARD_RAW_PUT_SQLSTR = "INSERT INTO plan_kegunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_otx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool FROM plan_kegunit_s_put_vld "
INSERT_PLNKEGG_HEARD_RAW_DEL_SQLSTR = "INSERT INTO plan_kegunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, keg_rope_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name, keg_rope_ERASE FROM plan_kegunit_s_del_vld "
INSERT_PLNUNIT_HEARD_RAW_PUT_SQLSTR = "INSERT INTO planunit_h_put_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_otx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain) SELECT spark_num, face_name, moment_rope, plan_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain FROM planunit_s_put_vld "
INSERT_PLNUNIT_HEARD_RAW_DEL_SQLSTR = "INSERT INTO planunit_h_del_raw (spark_num, face_name_otx, moment_rope_otx, plan_name_ERASE_otx) SELECT spark_num, face_name, moment_rope, plan_name_ERASE FROM planunit_s_del_vld "

INSERT_NABTIME_HEARD_RAW_SQLSTR = "INSERT INTO nabu_timenum_h_raw (spark_num, face_name_otx, moment_rope_otx, otx_time, inx_time) SELECT spark_num, face_name, moment_rope, otx_time, inx_time FROM nabu_timenum_s_vld "


def get_insert_into_heard_raw_sqlstrs() -> dict[str, str]:
    return {
        "nabu_timenum_h_raw": INSERT_NABTIME_HEARD_RAW_SQLSTR,
        "moment_paybook_h_raw": INSERT_MMTPAYY_HEARD_RAW_SQLSTR,
        "moment_budunit_h_raw": INSERT_MMTBUDD_HEARD_RAW_SQLSTR,
        "moment_epoch_hour_h_raw": INSERT_MMTHOUR_HEARD_RAW_SQLSTR,
        "moment_epoch_month_h_raw": INSERT_MMTMONT_HEARD_RAW_SQLSTR,
        "moment_epoch_weekday_h_raw": INSERT_MMTWEEK_HEARD_RAW_SQLSTR,
        "moment_timeoffi_h_raw": INSERT_MMTOFFI_HEARD_RAW_SQLSTR,
        "momentunit_h_raw": INSERT_MMTUNIT_HEARD_RAW_SQLSTR,
        "plan_person_membership_h_put_raw": INSERT_PLNMEMB_HEARD_RAW_PUT_SQLSTR,
        "plan_person_membership_h_del_raw": INSERT_PLNMEMB_HEARD_RAW_DEL_SQLSTR,
        "plan_personunit_h_put_raw": INSERT_PLNPRSN_HEARD_RAW_PUT_SQLSTR,
        "plan_personunit_h_del_raw": INSERT_PLNPRSN_HEARD_RAW_DEL_SQLSTR,
        "plan_keg_awardunit_h_put_raw": INSERT_PLNAWAR_HEARD_RAW_PUT_SQLSTR,
        "plan_keg_awardunit_h_del_raw": INSERT_PLNAWAR_HEARD_RAW_DEL_SQLSTR,
        "plan_keg_factunit_h_put_raw": INSERT_PLNFACT_HEARD_RAW_PUT_SQLSTR,
        "plan_keg_factunit_h_del_raw": INSERT_PLNFACT_HEARD_RAW_DEL_SQLSTR,
        "plan_keg_healerunit_h_put_raw": INSERT_PLNHEAL_HEARD_RAW_PUT_SQLSTR,
        "plan_keg_healerunit_h_del_raw": INSERT_PLNHEAL_HEARD_RAW_DEL_SQLSTR,
        "plan_keg_reason_caseunit_h_put_raw": INSERT_PLNCASE_HEARD_RAW_PUT_SQLSTR,
        "plan_keg_reason_caseunit_h_del_raw": INSERT_PLNCASE_HEARD_RAW_DEL_SQLSTR,
        "plan_keg_reasonunit_h_put_raw": INSERT_PLNREAS_HEARD_RAW_PUT_SQLSTR,
        "plan_keg_reasonunit_h_del_raw": INSERT_PLNREAS_HEARD_RAW_DEL_SQLSTR,
        "plan_keg_partyunit_h_put_raw": INSERT_PLNLABO_HEARD_RAW_PUT_SQLSTR,
        "plan_keg_partyunit_h_del_raw": INSERT_PLNLABO_HEARD_RAW_DEL_SQLSTR,
        "plan_kegunit_h_put_raw": INSERT_PLNKEGG_HEARD_RAW_PUT_SQLSTR,
        "plan_kegunit_h_del_raw": INSERT_PLNKEGG_HEARD_RAW_DEL_SQLSTR,
        "planunit_h_put_raw": INSERT_PLNUNIT_HEARD_RAW_PUT_SQLSTR,
        "planunit_h_del_raw": INSERT_PLNUNIT_HEARD_RAW_DEL_SQLSTR,
    }


def create_update_heard_raw_existing_inx_col_sqlstr(
    translate_type_abbv: str, table: str, column_prefix: str
) -> str:
    return f"""
WITH trl_face_otx_spark AS (
    SELECT 
      raw_dim.rowid raw_rowid
    , raw_dim.spark_num
    , raw_dim.face_name_otx
    , raw_dim.{column_prefix}_otx
    , MAX(trl.spark_num) translate_spark_num
    FROM {table} raw_dim
    LEFT JOIN translate_{translate_type_abbv}_s_vld trl ON trl.face_name = raw_dim.face_name_otx
        AND trl.otx_{translate_type_abbv} = raw_dim.{column_prefix}_otx
        AND raw_dim.spark_num >= trl.spark_num
    GROUP BY 
      raw_dim.rowid
    , raw_dim.spark_num
    , raw_dim.face_name_otx
    , raw_dim.{column_prefix}_otx
),
trl_inx_strs AS (
    SELECT trl_foe.raw_rowid, trl_vld.inx_{translate_type_abbv}
    FROM trl_face_otx_spark trl_foe
    LEFT JOIN translate_{translate_type_abbv}_s_vld trl_vld
        ON trl_vld.face_name = trl_foe.face_name_otx
        AND trl_vld.otx_{translate_type_abbv} = trl_foe.{column_prefix}_otx
        AND trl_vld.spark_num = trl_foe.translate_spark_num
)
UPDATE {table} as dim_h_raw
SET {column_prefix}_inx = (
    SELECT trl_inx_strs.inx_{translate_type_abbv}
    FROM trl_inx_strs
    WHERE dim_h_raw.rowid = trl_inx_strs.raw_rowid
)
;
"""


def create_update_heard_raw_empty_inx_col_sqlstr(table: str, column_prefix: str) -> str:
    """UPDATE statement that will always set the "inx" column to the "otx" value if "inx" is NULL"""
    return f"""
UPDATE {table} as dim_h_raw
SET {column_prefix}_inx = {column_prefix}_otx
WHERE {column_prefix}_inx IS NULL
;
"""


PLNAWAR_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_keg_awardunit_h_del_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, awardee_title_ERASE_inx
FROM plan_keg_awardunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, awardee_title_ERASE_inx
"""
PLNFACT_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_keg_factunit_h_del_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, fact_context_ERASE_inx
FROM plan_keg_factunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, fact_context_ERASE_inx
"""
PLNHEAL_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_keg_healerunit_h_del_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, healer_name_ERASE_inx
FROM plan_keg_healerunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, healer_name_ERASE_inx
"""
PLNLABO_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_keg_partyunit_h_del_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, party_title_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, party_title_ERASE_inx
FROM plan_keg_partyunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, party_title_ERASE_inx
"""
PLNCASE_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_keg_reason_caseunit_h_del_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, reason_state_ERASE_inx
FROM plan_keg_reason_caseunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, reason_state_ERASE_inx
"""
PLNREAS_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_keg_reasonunit_h_del_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_ERASE_inx
FROM plan_keg_reasonunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_ERASE_inx
"""
PLNKEGG_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_kegunit_h_del_agg (spark_num, face_name, moment_rope, plan_name, keg_rope_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_ERASE_inx
FROM plan_kegunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_ERASE_inx
"""
PLNMEMB_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_person_membership_h_del_agg (spark_num, face_name, moment_rope, plan_name, person_name, group_title_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, group_title_ERASE_inx
FROM plan_person_membership_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, group_title_ERASE_inx
"""
PLNPRSN_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO plan_personunit_h_del_agg (spark_num, face_name, moment_rope, plan_name, person_name_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_ERASE_inx
FROM plan_personunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_ERASE_inx
"""
PLNUNIT_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO planunit_h_del_agg (spark_num, face_name, moment_rope, plan_name_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_ERASE_inx
FROM planunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_ERASE_inx
"""
PLNAWAR_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_keg_awardunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title, give_force, take_force)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, awardee_title_inx, give_force, take_force
FROM plan_keg_awardunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, awardee_title_inx, give_force, take_force
"""
PLNFACT_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_keg_factunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context, fact_state, fact_lower_otx, fact_upper_otx)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper
FROM plan_keg_factunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper
"""
PLNHEAL_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_keg_healerunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, healer_name_inx
FROM plan_keg_healerunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, healer_name_inx
"""
PLNLABO_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_keg_partyunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, party_title, solo)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, party_title_inx, solo
FROM plan_keg_partyunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, party_title_inx, solo
"""
PLNCASE_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_keg_reason_caseunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state, reason_lower_otx, reason_upper_otx, reason_divisor)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, reason_state_inx, reason_lower, reason_upper, reason_divisor
FROM plan_keg_reason_caseunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, reason_state_inx, reason_lower, reason_upper, reason_divisor
"""
PLNREAS_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_keg_reasonunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, active_requisite)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, active_requisite
FROM plan_keg_reasonunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, active_requisite
"""
PLNKEGG_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_kegunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, keg_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool
FROM plan_kegunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool
"""
PLNMEMB_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_person_membership_h_put_agg (spark_num, face_name, moment_rope, plan_name, person_name, group_title, group_cred_lumen, group_debt_lumen)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, group_title_inx, group_cred_lumen, group_debt_lumen
FROM plan_person_membership_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, group_title_inx, group_cred_lumen, group_debt_lumen
"""
PLNPRSN_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO plan_personunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, person_name, person_cred_lumen, person_debt_lumen)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, person_cred_lumen, person_debt_lumen
FROM plan_personunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, person_cred_lumen, person_debt_lumen
"""
PLNUNIT_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO planunit_h_put_agg (spark_num, face_name, moment_rope, plan_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain
FROM planunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain
"""
MMTBUDD_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_budunit_h_agg (spark_num, face_name, moment_rope, plan_name, bud_time_otx, quota, celldepth)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, bud_time, quota, celldepth
FROM moment_budunit_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, bud_time, quota, celldepth
"""
MMTHOUR_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_hour_h_agg (spark_num, face_name, moment_rope, cumulative_minute, hour_label)
SELECT spark_num, face_name_inx, moment_rope_inx, cumulative_minute, hour_label_inx
FROM moment_epoch_hour_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, cumulative_minute, hour_label_inx
"""
MMTMONT_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_month_h_agg (spark_num, face_name, moment_rope, cumulative_day, month_label)
SELECT spark_num, face_name_inx, moment_rope_inx, cumulative_day, month_label_inx
FROM moment_epoch_month_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, cumulative_day, month_label_inx
"""
MMTWEEK_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_weekday_h_agg (spark_num, face_name, moment_rope, weekday_order, weekday_label)
SELECT spark_num, face_name_inx, moment_rope_inx, weekday_order, weekday_label_inx
FROM moment_epoch_weekday_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, weekday_order, weekday_label_inx
"""
MMTPAYY_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_paybook_h_agg (spark_num, face_name, moment_rope, plan_name, person_name, tran_time_otx, amount)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, tran_time, amount
FROM moment_paybook_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, tran_time, amount
"""
MMTOFFI_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_timeoffi_h_agg (spark_num, face_name, moment_rope, offi_time_otx)
SELECT spark_num, face_name_inx, moment_rope_inx, offi_time
FROM moment_timeoffi_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, offi_time
"""
MMTUNIT_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO momentunit_h_agg (spark_num, face_name, moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations)
SELECT spark_num, face_name_inx, moment_rope_inx, epoch_label_inx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations
FROM momentunit_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, epoch_label_inx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations
"""
NABTIME_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO nabu_timenum_h_agg (spark_num, face_name, moment_rope, otx_time, inx_time)
SELECT spark_num, face_name_inx, moment_rope_inx, otx_time, inx_time
FROM nabu_timenum_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, otx_time, inx_time
"""


def get_insert_heard_agg_sqlstrs() -> dict[str, str]:
    return {
        "plan_keg_awardunit_h_del_agg": PLNAWAR_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_keg_factunit_h_del_agg": PLNFACT_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_keg_healerunit_h_del_agg": PLNHEAL_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_keg_partyunit_h_del_agg": PLNLABO_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_keg_reason_caseunit_h_del_agg": PLNCASE_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_keg_reasonunit_h_del_agg": PLNREAS_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_kegunit_h_del_agg": PLNKEGG_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_person_membership_h_del_agg": PLNMEMB_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_personunit_h_del_agg": PLNPRSN_HEARD_AGG_DEL_INSERT_SQLSTR,
        "planunit_h_del_agg": PLNUNIT_HEARD_AGG_DEL_INSERT_SQLSTR,
        "plan_keg_awardunit_h_put_agg": PLNAWAR_HEARD_AGG_PUT_INSERT_SQLSTR,
        "plan_keg_factunit_h_put_agg": PLNFACT_HEARD_AGG_PUT_INSERT_SQLSTR,
        "plan_keg_healerunit_h_put_agg": PLNHEAL_HEARD_AGG_PUT_INSERT_SQLSTR,
        "plan_keg_partyunit_h_put_agg": PLNLABO_HEARD_AGG_PUT_INSERT_SQLSTR,
        "plan_keg_reason_caseunit_h_put_agg": PLNCASE_HEARD_AGG_PUT_INSERT_SQLSTR,
        "plan_keg_reasonunit_h_put_agg": PLNREAS_HEARD_AGG_PUT_INSERT_SQLSTR,
        "plan_kegunit_h_put_agg": PLNKEGG_HEARD_AGG_PUT_INSERT_SQLSTR,
        "plan_person_membership_h_put_agg": PLNMEMB_HEARD_AGG_PUT_INSERT_SQLSTR,
        "plan_personunit_h_put_agg": PLNPRSN_HEARD_AGG_PUT_INSERT_SQLSTR,
        "planunit_h_put_agg": PLNUNIT_HEARD_AGG_PUT_INSERT_SQLSTR,
        "moment_budunit_h_agg": MMTBUDD_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_hour_h_agg": MMTHOUR_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_month_h_agg": MMTMONT_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_weekday_h_agg": MMTWEEK_HEARD_AGG_INSERT_SQLSTR,
        "moment_paybook_h_agg": MMTPAYY_HEARD_AGG_INSERT_SQLSTR,
        "moment_timeoffi_h_agg": MMTOFFI_HEARD_AGG_INSERT_SQLSTR,
        "momentunit_h_agg": MMTUNIT_HEARD_AGG_INSERT_SQLSTR,
        "nabu_timenum_h_agg": NABTIME_HEARD_AGG_INSERT_SQLSTR,
    }


def get_update_heard_agg_timenum_sqlstr(dst_tablename: str, focus_column: str) -> str:
    #   spark_num, mod(otx_time - inx_time, IFNULL(x_moment.c400_number, 1472657760)) AS inx_epoch_diff
    mmtunit_h_agg_tablename = create_prime_tablename("momentunit", "h", "agg")
    nabtime_h_agg_tablename = create_prime_tablename("nabu_timenum", "h", "agg")
    return f"""WITH spark_inx_epoch_diff AS (
SELECT 
  spark_num
, otx_time - inx_time AS inx_epoch_diff
, IFNULL(c400_number * 210379680, 1472657760) as epoch_length
FROM {nabtime_h_agg_tablename}
LEFT JOIN (
    SELECT moment_rope, c400_number 
    FROM {mmtunit_h_agg_tablename} 
    GROUP BY moment_rope, c400_number
    ) x_moment ON x_moment.moment_rope = {nabtime_h_agg_tablename}.moment_rope
)
UPDATE {dst_tablename}
SET {focus_column}_inx = mod({focus_column}_otx + (
    SELECT inx_epoch_diff
    FROM spark_inx_epoch_diff
    WHERE spark_inx_epoch_diff.spark_num = {dst_tablename}.spark_num
), (SELECT epoch_length
    FROM spark_inx_epoch_diff
    WHERE spark_inx_epoch_diff.spark_num = {dst_tablename}.spark_num
))
FROM spark_inx_epoch_diff
WHERE {dst_tablename}.spark_num IN (SELECT spark_num FROM spark_inx_epoch_diff)
;
"""


def get_update_heard_agg_timenum_sqlstrs() -> dict[str]:
    mmtoffi_tbl = create_prime_tablename("moment_timeoffi", "h", "agg")
    mmtoffi_key = ("moment_timeoffi", "offi_time")
    mmtpayy_tbl = create_prime_tablename("moment_paybook", "h", "agg")
    mmtpayy_key = ("moment_paybook", "tran_time")
    mmtbudd_tbl = create_prime_tablename("moment_budunit", "h", "agg")
    mmtbudd_key = ("moment_budunit", "bud_time")
    return {
        mmtpayy_key: get_update_heard_agg_timenum_sqlstr(mmtpayy_tbl, "tran_time"),
        mmtoffi_key: get_update_heard_agg_timenum_sqlstr(mmtoffi_tbl, "offi_time"),
        mmtbudd_key: get_update_heard_agg_timenum_sqlstr(mmtbudd_tbl, "bud_time"),
    }


# TODO add_epoch_frame process should to pipeline
# All _inx rope columns have been set. This is where the check for epoch_rope happens
# Identify the epoch_rope from the moment
# Identify how much should be added/deleted.
# Create "_otx" and "_inx" columns for
# reason_lower, reason_upper, fact_lower, fact_upper, tran_time, bud_time,
def get_update_plncase_inx_epoch_diff_sqlstr() -> str:
    nabtime_tablename = create_prime_tablename("nabu_timenum", "h", "agg")
    plncase_abbv = "plan_keg_reason_caseunit"
    plncase_tablename = create_prime_tablename(plncase_abbv, "h", "agg", "put")
    return f"""
WITH spark_inx_epoch_diff AS (
    SELECT 
      spark_num
    , otx_time - inx_time AS inx_epoch_diff
    FROM {nabtime_tablename}
    GROUP BY spark_num, otx_time, inx_time
)
UPDATE {plncase_tablename}
SET inx_epoch_diff = spark_inx_epoch_diff.inx_epoch_diff
FROM spark_inx_epoch_diff
WHERE {plncase_tablename}.spark_num IN (SELECT spark_num FROM spark_inx_epoch_diff)
;
"""


def get_update_plnfact_inx_epoch_diff_sqlstr() -> str:
    nabtime_tablename = create_prime_tablename("nabu_timenum", "h", "agg")
    plnfact_tablename = create_prime_tablename("plnfact", "h", "agg", "put")
    return f"""
WITH spark_inx_epoch_diff AS (
    SELECT 
      spark_num
    , otx_time - inx_time AS inx_epoch_diff
    FROM {nabtime_tablename}
    GROUP BY spark_num, otx_time, inx_time
)
UPDATE {plnfact_tablename}
SET inx_epoch_diff = spark_inx_epoch_diff.inx_epoch_diff
FROM spark_inx_epoch_diff
WHERE {plnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_inx_epoch_diff)
;
"""


def get_update_plncase_context_keg_sqlstr() -> str:
    plncase_tablename = create_prime_tablename("plncase", "h", "agg", "put")
    plnkegg_tablename = create_prime_tablename("plnkegg", "h", "agg", "put")
    return f"""
WITH spark_plnkegg AS (
    SELECT spark_num, close, denom, morph
    FROM {plnkegg_tablename}
    GROUP BY spark_num, close, denom, morph
)
UPDATE {plncase_tablename}
SET 
  context_keg_close = spark_plnkegg.close
, context_keg_denom = spark_plnkegg.denom
, context_keg_morph = spark_plnkegg.morph
FROM spark_plnkegg
WHERE {plncase_tablename}.spark_num IN (SELECT spark_num FROM spark_plnkegg)
;
"""


def get_update_plnfact_context_keg_sqlstr() -> str:
    plnfact_tablename = create_prime_tablename("plnfact", "h", "agg", "put")
    plnkegg_tablename = create_prime_tablename("plnkegg", "h", "agg", "put")
    return f"""
WITH spark_plnkegg AS (
    SELECT spark_num, close, denom, morph
    FROM {plnkegg_tablename}
    GROUP BY spark_num, close, denom, morph
)
UPDATE {plnfact_tablename}
SET 
  context_keg_close = spark_plnkegg.close
, context_keg_denom = spark_plnkegg.denom
, context_keg_morph = spark_plnkegg.morph
FROM spark_plnkegg
WHERE {plnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_plnkegg)
;
"""


def get_update_plncase_range_sqlstr() -> str:
    plncase_tablename = create_prime_tablename("plncase", "h", "agg", "put")
    return f"""
WITH spark_plncase AS (
    SELECT 
      spark_num
    , IFNULL(reason_divisor, IFNULL(context_keg_close, context_keg_denom)) modulus
    , CASE WHEN morph = 1 THEN inx_epoch_diff / IFNULL(context_keg_denom, 1) ELSE inx_epoch_diff END calc_epoch_diff
    FROM {plncase_tablename}
    GROUP BY spark_num, reason_divisor, context_keg_close, context_keg_denom, context_keg_morph
)
UPDATE {plncase_tablename}
SET 
  reason_lower_inx = (reason_lower_otx + spark_plncase.calc_epoch_diff) % spark_plncase.modulus
, reason_upper_inx = (reason_upper_otx + spark_plncase.calc_epoch_diff) % spark_plncase.modulus
FROM spark_plncase
WHERE {plncase_tablename}.spark_num IN (SELECT spark_num FROM spark_plncase)
;
"""


def get_update_plnfact_range_sqlstr() -> str:
    plnfact_tablename = create_prime_tablename("plnfact", "h", "agg", "put")
    return f"""
WITH spark_plnfact AS (
    SELECT 
      spark_num
    , IFNULL(reason_divisor, IFNULL(context_keg_close, context_keg_denom)) modulus
    , FACT WHEN morph = 1 THEN inx_epoch_diff / IFNULL(context_keg_denom, 1) ELSE inx_epoch_diff END calc_epoch_diff
    FROM {plnfact_tablename}
    GROUP BY spark_num, reason_divisor, context_keg_close, context_keg_denom, context_keg_morph
)
UPDATE {plnfact_tablename}
SET 
  reason_lower_inx = (reason_lower_otx + spark_plnfact.calc_epoch_diff) % spark_plnfact.modulus
, reason_upper_inx = (reason_upper_otx + spark_plnfact.calc_epoch_diff) % spark_plnfact.modulus
FROM spark_plnfact
WHERE {plnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_plnfact)
;
"""


def update_heard_agg_timenum_columns(cursor: sqlite3_Connection):
    for update_sqlstr in get_update_heard_agg_timenum_sqlstrs().values():
        cursor.execute(update_sqlstr)


MMTPAYY_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_paybook_h_vld (moment_rope, plan_name, person_name, tran_time, amount)
SELECT moment_rope_inx, plan_name_inx, person_name_inx, tran_time, amount
FROM moment_paybook_h_raw
GROUP BY moment_rope_inx, plan_name_inx, person_name_inx, tran_time, amount
"""
MMTBUDD_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_budunit_h_vld (moment_rope, plan_name, bud_time, quota, celldepth)
SELECT moment_rope_inx, plan_name_inx, bud_time, quota, celldepth
FROM moment_budunit_h_raw
GROUP BY moment_rope_inx, plan_name_inx, bud_time, quota, celldepth
"""
MMTHOUR_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_epoch_hour_h_vld (moment_rope, cumulative_minute, hour_label)
SELECT moment_rope_inx, cumulative_minute, hour_label_inx
FROM moment_epoch_hour_h_raw
GROUP BY moment_rope_inx, cumulative_minute, hour_label_inx
"""
MMTMONT_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_epoch_month_h_vld (moment_rope, cumulative_day, month_label)
SELECT moment_rope_inx, cumulative_day, month_label_inx
FROM moment_epoch_month_h_raw
GROUP BY moment_rope_inx, cumulative_day, month_label_inx
"""
MMTWEEK_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_epoch_weekday_h_vld (moment_rope, weekday_order, weekday_label)
SELECT moment_rope_inx, weekday_order, weekday_label_inx
FROM moment_epoch_weekday_h_raw
GROUP BY moment_rope_inx, weekday_order, weekday_label_inx
"""
MMTOFFI_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_timeoffi_h_vld (moment_rope, offi_time)
SELECT moment_rope_inx, offi_time
FROM moment_timeoffi_h_raw
GROUP BY moment_rope_inx, offi_time
"""
MMTUNIT_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO momentunit_h_vld (moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations)
SELECT moment_rope_inx, epoch_label_inx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations
FROM momentunit_h_raw
GROUP BY moment_rope_inx, epoch_label_inx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations
"""

INSERT_PLNMEMB_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_person_membership_h_put_vld (spark_num, face_name, moment_rope, plan_name, person_name, group_title, group_cred_lumen, group_debt_lumen)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, group_title_inx, group_cred_lumen, group_debt_lumen
FROM plan_person_membership_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, group_title_inx, group_cred_lumen, group_debt_lumen
"""
INSERT_PLNMEMB_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_person_membership_h_del_vld (spark_num, face_name, moment_rope, plan_name, person_name, group_title_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, group_title_ERASE_inx
FROM plan_person_membership_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, group_title_ERASE_inx
"""
INSERT_PLNPRSN_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_personunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, person_name, person_cred_lumen, person_debt_lumen)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, person_cred_lumen, person_debt_lumen
FROM plan_personunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_inx, person_cred_lumen, person_debt_lumen
"""
INSERT_PLNPRSN_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_personunit_h_del_vld (spark_num, face_name, moment_rope, plan_name, person_name_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_ERASE_inx
FROM plan_personunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, person_name_ERASE_inx
"""
INSERT_PLNAWAR_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_keg_awardunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title, give_force, take_force)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, awardee_title_inx, give_force, take_force
FROM plan_keg_awardunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, awardee_title_inx, give_force, take_force
"""
INSERT_PLNAWAR_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_keg_awardunit_h_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, awardee_title_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, awardee_title_ERASE_inx
FROM plan_keg_awardunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, awardee_title_ERASE_inx
"""
INSERT_PLNFACT_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_keg_factunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context, fact_state, fact_lower, fact_upper)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper
FROM plan_keg_factunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper
"""
INSERT_PLNFACT_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_keg_factunit_h_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, fact_context_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, fact_context_ERASE_inx
FROM plan_keg_factunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, fact_context_ERASE_inx
"""
INSERT_PLNHEAL_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_keg_healerunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, healer_name_inx
FROM plan_keg_healerunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, healer_name_inx
"""
INSERT_PLNHEAL_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_keg_healerunit_h_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, healer_name_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, healer_name_ERASE_inx
FROM plan_keg_healerunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, healer_name_ERASE_inx
"""
INSERT_PLNCASE_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_keg_reason_caseunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, reason_state_inx, reason_lower, reason_upper, reason_divisor
FROM plan_keg_reason_caseunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, reason_state_inx, reason_lower, reason_upper, reason_divisor
"""
INSERT_PLNCASE_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_keg_reason_caseunit_h_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, reason_state_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, reason_state_ERASE_inx
FROM plan_keg_reason_caseunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, reason_state_ERASE_inx
"""
INSERT_PLNREAS_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_keg_reasonunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context, active_requisite)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, active_requisite
FROM plan_keg_reasonunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_inx, active_requisite
"""
INSERT_PLNREAS_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_keg_reasonunit_h_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, reason_context_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_ERASE_inx
FROM plan_keg_reasonunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, reason_context_ERASE_inx
"""
INSERT_PLNLABO_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_keg_partyunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, party_title, solo)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, party_title_inx, solo
FROM plan_keg_partyunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, party_title_inx, solo
"""
INSERT_PLNLABO_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_keg_partyunit_h_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, party_title_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, party_title_ERASE_inx
FROM plan_keg_partyunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, party_title_ERASE_inx
"""
INSERT_PLNKEGG_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO plan_kegunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, keg_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool
FROM plan_kegunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool
"""
INSERT_PLNKEGG_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO plan_kegunit_h_del_vld (spark_num, face_name, moment_rope, plan_name, keg_rope_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_ERASE_inx
FROM plan_kegunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, keg_rope_ERASE_inx
"""
INSERT_PLNUNIT_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO planunit_h_put_vld (spark_num, face_name, moment_rope, plan_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain
FROM planunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain
"""
INSERT_PLNUNIT_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO planunit_h_del_vld (spark_num, face_name, moment_rope, plan_name_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, plan_name_ERASE_inx
FROM planunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, plan_name_ERASE_inx
"""


def get_insert_heard_vld_sqlstrs() -> dict[str, str]:
    return {
        "moment_paybook_h_vld": MMTPAYY_HEARD_VLD_INSERT_SQLSTR,
        "moment_budunit_h_vld": MMTBUDD_HEARD_VLD_INSERT_SQLSTR,
        "moment_epoch_hour_h_vld": MMTHOUR_HEARD_VLD_INSERT_SQLSTR,
        "moment_epoch_month_h_vld": MMTMONT_HEARD_VLD_INSERT_SQLSTR,
        "moment_epoch_weekday_h_vld": MMTWEEK_HEARD_VLD_INSERT_SQLSTR,
        "moment_timeoffi_h_vld": MMTOFFI_HEARD_VLD_INSERT_SQLSTR,
        "momentunit_h_vld": MMTUNIT_HEARD_VLD_INSERT_SQLSTR,
        "plan_person_membership_h_put_vld": INSERT_PLNMEMB_HEARD_VLD_PUT_SQLSTR,
        "plan_person_membership_h_del_vld": INSERT_PLNMEMB_HEARD_VLD_DEL_SQLSTR,
        "plan_personunit_h_put_vld": INSERT_PLNPRSN_HEARD_VLD_PUT_SQLSTR,
        "plan_personunit_h_del_vld": INSERT_PLNPRSN_HEARD_VLD_DEL_SQLSTR,
        "plan_keg_awardunit_h_put_vld": INSERT_PLNAWAR_HEARD_VLD_PUT_SQLSTR,
        "plan_keg_awardunit_h_del_vld": INSERT_PLNAWAR_HEARD_VLD_DEL_SQLSTR,
        "plan_keg_factunit_h_put_vld": INSERT_PLNFACT_HEARD_VLD_PUT_SQLSTR,
        "plan_keg_factunit_h_del_vld": INSERT_PLNFACT_HEARD_VLD_DEL_SQLSTR,
        "plan_keg_healerunit_h_put_vld": INSERT_PLNHEAL_HEARD_VLD_PUT_SQLSTR,
        "plan_keg_healerunit_h_del_vld": INSERT_PLNHEAL_HEARD_VLD_DEL_SQLSTR,
        "plan_keg_reason_caseunit_h_put_vld": INSERT_PLNCASE_HEARD_VLD_PUT_SQLSTR,
        "plan_keg_reason_caseunit_h_del_vld": INSERT_PLNCASE_HEARD_VLD_DEL_SQLSTR,
        "plan_keg_reasonunit_h_put_vld": INSERT_PLNREAS_HEARD_VLD_PUT_SQLSTR,
        "plan_keg_reasonunit_h_del_vld": INSERT_PLNREAS_HEARD_VLD_DEL_SQLSTR,
        "plan_keg_partyunit_h_put_vld": INSERT_PLNLABO_HEARD_VLD_PUT_SQLSTR,
        "plan_keg_partyunit_h_del_vld": INSERT_PLNLABO_HEARD_VLD_DEL_SQLSTR,
        "plan_kegunit_h_put_vld": INSERT_PLNKEGG_HEARD_VLD_PUT_SQLSTR,
        "plan_kegunit_h_del_vld": INSERT_PLNKEGG_HEARD_VLD_DEL_SQLSTR,
        "planunit_h_put_vld": INSERT_PLNUNIT_HEARD_VLD_PUT_SQLSTR,
        "planunit_h_del_vld": INSERT_PLNUNIT_HEARD_VLD_DEL_SQLSTR,
    }


MMTPAYY_FU2_SELECT_SQLSTR = "SELECT moment_rope, plan_name, person_name, tran_time, amount FROM moment_paybook_h_vld WHERE moment_rope = "
MMTBUDD_FU2_SELECT_SQLSTR = "SELECT moment_rope, plan_name, bud_time, quota, celldepth FROM moment_budunit_h_vld WHERE moment_rope = "
MMTHOUR_FU2_SELECT_SQLSTR = "SELECT moment_rope, cumulative_minute, hour_label FROM moment_epoch_hour_h_vld WHERE moment_rope = "
MMTMONT_FU2_SELECT_SQLSTR = "SELECT moment_rope, cumulative_day, month_label FROM moment_epoch_month_h_vld WHERE moment_rope = "
MMTWEEK_FU2_SELECT_SQLSTR = "SELECT moment_rope, weekday_order, weekday_label FROM moment_epoch_weekday_h_vld WHERE moment_rope = "
MMTOFFI_FU2_SELECT_SQLSTR = (
    "SELECT moment_rope, offi_time FROM moment_timeoffi_h_vld WHERE moment_rope = "
)
MMTUNIT_FU2_SELECT_SQLSTR = "SELECT moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations FROM momentunit_h_vld WHERE moment_rope = "


def get_moment_heard_select1_sqlstrs(moment_rope: str) -> dict[str, str]:
    return {
        "momentunit": f"{MMTUNIT_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_budunit": f"{MMTBUDD_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_paybook": f"{MMTPAYY_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_epoch_hour": f"{MMTHOUR_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_epoch_month": f"{MMTMONT_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_epoch_weekday": f"{MMTWEEK_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_timeoffi": f"{MMTOFFI_FU2_SELECT_SQLSTR}'{moment_rope}'",
    }


def get_idea_stageble_put_dimens() -> dict[str, list[str]]:
    return {
        "br00000": ["momentunit"],
        "br00001": ["planunit", "moment_budunit", "momentunit"],
        "br00002": ["plan_personunit", "planunit", "moment_paybook", "momentunit"],
        "br00003": ["moment_epoch_hour", "momentunit"],
        "br00004": ["moment_epoch_month", "momentunit"],
        "br00005": ["moment_epoch_weekday", "momentunit"],
        "br00006": ["moment_timeoffi", "momentunit"],
        "br00011": ["plan_personunit", "planunit", "momentunit"],
        "br00012": [
            "plan_person_membership",
            "plan_personunit",
            "planunit",
            "momentunit",
        ],
        "br00013": ["plan_kegunit", "planunit", "momentunit"],
        "br00019": ["plan_kegunit", "planunit", "momentunit"],
        "br00020": [
            "plan_person_membership",
            "plan_personunit",
            "planunit",
            "momentunit",
        ],
        "br00021": ["plan_personunit", "planunit", "momentunit"],
        "br00022": [
            "plan_keg_awardunit",
            "plan_kegunit",
            "planunit",
            "momentunit",
        ],
        "br00023": [
            "plan_keg_factunit",
            "plan_kegunit",
            "planunit",
            "momentunit",
        ],
        "br00024": [
            "plan_keg_partyunit",
            "plan_kegunit",
            "planunit",
            "momentunit",
        ],
        "br00025": [
            "plan_keg_healerunit",
            "plan_kegunit",
            "planunit",
            "momentunit",
        ],
        "br00026": [
            "plan_keg_reason_caseunit",
            "plan_keg_reasonunit",
            "plan_kegunit",
            "planunit",
            "momentunit",
        ],
        "br00027": [
            "plan_keg_reasonunit",
            "plan_kegunit",
            "planunit",
            "momentunit",
        ],
        "br00028": ["plan_kegunit", "planunit", "momentunit"],
        "br00029": ["planunit", "momentunit"],
        "br00036": [
            "plan_keg_healerunit",
            "plan_kegunit",
            "planunit",
            "momentunit",
        ],
        "br00042": [],
        "br00043": [],
        "br00044": [],
        "br00045": [],
        "br00050": ["plan_personunit", "planunit", "momentunit"],
        "br00051": ["planunit", "momentunit"],
        "br00052": ["plan_kegunit", "planunit", "momentunit"],
        "br00053": ["plan_kegunit", "planunit", "momentunit"],
        "br00054": ["plan_kegunit", "planunit", "momentunit"],
        "br00055": ["plan_kegunit", "planunit", "momentunit"],
        "br00056": [
            "plan_keg_reasonunit",
            "plan_kegunit",
            "planunit",
            "momentunit",
        ],
        "br00057": ["plan_kegunit", "planunit", "momentunit"],
        "br00058": ["planunit", "momentunit"],
        "br00059": ["momentunit"],
        "br00070": ["momentunit", "nabu_timenum"],
        "br00113": ["plan_personunit", "planunit", "momentunit"],
        "br00115": ["plan_personunit", "planunit", "momentunit"],
        "br00116": ["plan_personunit", "planunit", "momentunit"],
        "br00117": ["plan_personunit", "planunit", "momentunit"],
    }


IDEA_STAGEBLE_DEL_DIMENS = {
    "br00050": ["plan_person_membership"],
    "br00051": ["plan_personunit"],
    "br00052": ["plan_keg_awardunit"],
    "br00053": ["plan_keg_factunit"],
    "br00054": ["plan_keg_partyunit"],
    "br00055": ["plan_keg_healerunit"],
    "br00056": ["plan_keg_reason_caseunit"],
    "br00057": ["plan_keg_reasonunit"],
    "br00058": ["plan_kegunit"],
    "br00059": ["planunit"],
}


CREATE_MOMENT_OTE1_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS moment_ote1_agg (
  moment_rope TEXT
, plan_name TEXT
, spark_num INTEGER
, bud_time INTEGER
, error_message TEXT
)
;
"""
INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR = """
INSERT INTO moment_ote1_agg (moment_rope, plan_name, spark_num, bud_time)
SELECT moment_rope, plan_name, spark_num, bud_time
FROM (
    SELECT 
      moment_rope_inx moment_rope
    , plan_name_inx plan_name
    , spark_num
    , bud_time
    FROM moment_budunit_h_raw
    GROUP BY moment_rope_inx, plan_name_inx, spark_num, bud_time
)
ORDER BY moment_rope, plan_name, spark_num, bud_time
;
"""


CREATE_JOB_PLNMEMB_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_person_membership_job (moment_rope TEXT, plan_name TEXT, person_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL, fund_agenda_ratio_give REAL, fund_agenda_ratio_take REAL)"""
CREATE_JOB_PLNPRSN_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_personunit_job (moment_rope TEXT, plan_name TEXT, person_name TEXT, person_cred_lumen REAL, person_debt_lumen REAL, groupmark TEXT, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL, fund_agenda_ratio_give REAL, fund_agenda_ratio_take REAL, inallocable_person_debt_lumen REAL, irrational_person_debt_lumen REAL)"""
CREATE_JOB_PLNGROU_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_groupunit_job (moment_rope TEXT, plan_name TEXT, group_title TEXT, fund_grain REAL, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL)"""
CREATE_JOB_PLNAWAR_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_awardunit_job (moment_rope TEXT, plan_name TEXT, keg_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, fund_give REAL, fund_take REAL)"""
CREATE_JOB_PLNFACT_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_factunit_job (moment_rope TEXT, plan_name TEXT, keg_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"""
CREATE_JOB_PLNHEAL_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_healerunit_job (moment_rope TEXT, plan_name TEXT, keg_rope TEXT, healer_name TEXT)"""
CREATE_JOB_PLNCASE_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reason_caseunit_job (moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, task INTEGER, case_active INTEGER)"""
CREATE_JOB_PLNREAS_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_reasonunit_job (moment_rope TEXT, plan_name TEXT, keg_rope TEXT, reason_context TEXT, active_requisite INTEGER, task INTEGER, reason_active INTEGER, parent_heir_active INTEGER)"""
CREATE_JOB_PLNLABO_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_keg_partyunit_job (moment_rope TEXT, plan_name TEXT, keg_rope TEXT, party_title TEXT, solo INTEGER, plan_name_is_labor INTEGER)"""
CREATE_JOB_PLNKEGG_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_kegunit_job (moment_rope TEXT, plan_name TEXT, keg_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, fund_grain REAL, keg_active INTEGER, task INTEGER, fund_onset REAL, fund_cease REAL, fund_ratio REAL, gogo_calc REAL, stop_calc REAL, tree_level INTEGER, range_evaluated INTEGER, descendant_pledge_count INTEGER, healerunit_ratio REAL, all_person_cred INTEGER, all_person_debt INTEGER)"""
CREATE_JOB_PLNUNIT_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_job (moment_rope TEXT, plan_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, rational INTEGER, keeps_justified INTEGER, offtrack_fund REAL, sum_healerunit_kegs_fund_total REAL, keeps_buildable INTEGER, tree_traverse_count INTEGER)"""


def get_job_create_table_sqlstrs() -> dict[str, str]:
    return {
        "plan_person_membership_job": CREATE_JOB_PLNMEMB_SQLSTR,
        "plan_personunit_job": CREATE_JOB_PLNPRSN_SQLSTR,
        "plan_groupunit_job": CREATE_JOB_PLNGROU_SQLSTR,
        "plan_keg_awardunit_job": CREATE_JOB_PLNAWAR_SQLSTR,
        "plan_keg_factunit_job": CREATE_JOB_PLNFACT_SQLSTR,
        "plan_keg_healerunit_job": CREATE_JOB_PLNHEAL_SQLSTR,
        "plan_keg_reason_caseunit_job": CREATE_JOB_PLNCASE_SQLSTR,
        "plan_keg_reasonunit_job": CREATE_JOB_PLNREAS_SQLSTR,
        "plan_keg_partyunit_job": CREATE_JOB_PLNLABO_SQLSTR,
        "plan_kegunit_job": CREATE_JOB_PLNKEGG_SQLSTR,
        "planunit_job": CREATE_JOB_PLNUNIT_SQLSTR,
    }


def create_job_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_job_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


CREATE_MOMENT_PERSON_NETS_SQLSTR = "CREATE TABLE IF NOT EXISTS moment_person_nets (moment_rope TEXT, plan_name TEXT, plan_net_amount REAL)"
