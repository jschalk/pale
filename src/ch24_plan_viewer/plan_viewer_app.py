from flask import Flask, jsonify, render_template_string
from src.ch13_epoch.epoch_main import add_epoch_kegunit, get_default_epoch_config_dict
from src.ch24_plan_viewer.plan_viewer_example import (
    get_planunit_irrational_example,
    get_sue_plan_with_facts_and_reasons,
    get_sue_planunit,
)
from src.ch24_plan_viewer.plan_viewer_tool import get_plan_view_dict

app = Flask(__name__)


def get_plan_viewer_template() -> str:
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>plan_viewer</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Plan Persons and Keg Tree</h1>
        <h5>Each node has a keg_label</h5>
        
        <div class="persons_controls">
            <input type="checkbox" id="show_persons"><label for="show_persons">persons</label>
            <input type="checkbox" id="show_person_cred_lumen"><label for="show_person_cred_lumen">cred_lumen</label>
            <input type="checkbox" id="show_person_debt_lumen"><label for="show_person_debt_lumen">debt_lumen</label>
            <input type="checkbox" id="show_person_credor_pool"><label for="show_person_credor_pool">credor_pool</label>
            <input type="checkbox" id="show_person_debtor_pool"><label for="show_person_debtor_pool">debtor_pool</label>
            <input type="checkbox" id="show_person_irrational_person_debt_lumen"><label for="show_person_irrational_person_debt_lumen">irrational_person_debt_lumen</label>
            <input type="checkbox" id="show_person_inallocable_person_debt_lumen"><label for="show_person_inallocable_person_debt_lumen">inallocable_person_debt_lumen</label>
            <input type="checkbox" id="show_person_fund_give"><label for="show_person_fund_give">fund_give</label>
            <input type="checkbox" id="show_person_fund_take"><label for="show_person_fund_take">fund_take</label>
            <input type="checkbox" id="show_person_fund_agenda_give"><label for="show_person_fund_agenda_give">fund_agenda_give</label>
            <input type="checkbox" id="show_person_fund_agenda_take"><label for="show_person_fund_agenda_take">fund_agenda_take</label>
            <input type="checkbox" id="show_person_fund_agenda_ratio_give"><label for="show_person_fund_agenda_ratio_give">fund_agenda_ratio_give</label>
            <input type="checkbox" id="show_person_fund_agenda_ratio_take"><label for="show_person_fund_agenda_ratio_take">fund_agenda_ratio_take</label>
            <br>
            <input type="checkbox" id="show_person_membership_group_title"><label for="show_person_membership_group_title">membership_group_title</label>
            <input type="checkbox" id="show_person_membership_group_cred_lumen"><label for="show_person_membership_group_cred_lumen">membership_group_cred_lumen</label>
            <input type="checkbox" id="show_person_membership_group_debt_lumen"><label for="show_person_membership_group_debt_lumen">membership_group_debt_lumen</label>
            <input type="checkbox" id="show_person_membership_credor_pool"><label for="show_person_membership_credor_pool">membership_credor_pool</label>
            <input type="checkbox" id="show_person_membership_debtor_pool"><label for="show_person_membership_debtor_pool">membership_debtor_pool</label>
            <input type="checkbox" id="show_person_membership_fund_agenda_give"><label for="show_person_membership_fund_agenda_give">membership_fund_agenda_give</label>
            <input type="checkbox" id="show_person_membership_fund_agenda_ratio_give"><label for="show_person_membership_fund_agenda_ratio_give">membership_fund_agenda_ratio_give</label>
            <input type="checkbox" id="show_person_membership_fund_agenda_ratio_take"><label for="show_person_membership_fund_agenda_ratio_take">membership_fund_agenda_ratio_take</label>
            <input type="checkbox" id="show_person_membership_fund_agenda_take"><label for="show_person_membership_fund_agenda_take">membership_fund_agenda_take</label>
            <input type="checkbox" id="show_person_membership_fund_give"><label for="show_person_membership_fund_give">membership_fund_give</label>
            <input type="checkbox" id="show_person_membership_fund_take"><label for="show_person_membership_fund_take">membership_fund_take</label>
            
        </div>
        <div id="personsContainer" class="keg_tree_display"></div>
        <div class="keg_controls">
            <input type="checkbox" id="show_kegroot"><label for="show_kegroot">kegroot</label>
            <input type="checkbox" id="show_level"><label for="show_level">level</label>
            <input type="checkbox" id="show_moment_label"><label for="show_moment_label">moment_label</label>
            <input type="checkbox" id="show_pledge"><label for="show_pledge">pledge</label>
            <input type="checkbox" id="show_descendant_pledge_count"><label for="show_descendant_pledge_count">descendant_pledge_count</label>
            <input type="checkbox" id="show_keg_active"><label for="show_keg_active">keg_active</label>
            <input type="checkbox" id="show_task"><label for="show_task">task</label>
            <input type="checkbox" id="show_star"><label for="show_star">star</label>
            <input type="checkbox" id="show_keg_fund_total"><label for="show_keg_fund_total">keg_fund_total</label>
            <input type="checkbox" id="show_fund_onset"><label for="show_fund_onset">fund_onset</label>
            <input type="checkbox" id="show_fund_cease"><label for="show_fund_cease">fund_cease</label>
            <input type="checkbox" id="show_fund_grain"><label for="show_fund_grain">fund_grain</label>
            <input type="checkbox" id="show_fund_ratio"><label for="show_fund_ratio">fund_ratio</label>
            <input type="checkbox" id="show_parent_rope"><label for="show_parent_rope">parent_rope</label>
            <input type="checkbox" id="show_root_boolean"><label for="show_root_boolean">root_boolean</label>
            <input type="checkbox" id="show_uid"><label for="show_uid">uid</label>
            <input type="checkbox" id="show_reasonunits"><label for="show_reasonunits">reasonunits</label>
            <input type="checkbox" id="show_reasonheirs"><label for="show_reasonheirs">reasonheirs</label>
            <input type="checkbox" id="show_factunits"><label for="show_factunits">factunits</label>
            <input type="checkbox" id="show_factheirs"><label for="show_factheirs">factheirs</label>
            <input type="checkbox" id="show_awardunits"><label for="show_awardunits">awardunits</label>
            <input type="checkbox" id="show_awardheirs"><label for="show_awardheirs">awardheirs</label>
            <input type="checkbox" id="show_awardlines"><label for="show_awardlines">awardlines</label>
            <input type="checkbox" id="show_laborunit"><label for="show_laborunit">laborunit</label>
            <input type="checkbox" id="show_laborheir"><label for="show_laborheir">laborheir</label>
            <input type="checkbox" id="show_all_person_cred"><label for="show_all_person_cred">_all_person_cred</label>
            <input type="checkbox" id="show_all_person_debt"><label for="show_all_person_debt">_all_person_debt</label>
            <input type="checkbox" id="show_gogo_want"><label for="show_gogo_want">gogo_want</label>
            <input type="checkbox" id="show_stop_want"><label for="show_stop_want">stop_want</label>
            <input type="checkbox" id="show_gogo_calc"><label for="show_gogo_calc">_gogo_calc</label>
            <input type="checkbox" id="show_stop_calc"><label for="show_stop_calc">_stop_calc</label>
            <input type="checkbox" id="show_addin"><label for="show_addin">addin</label>
            <input type="checkbox" id="show_begin"><label for="show_begin">begin</label>
            <input type="checkbox" id="show_close"><label for="show_close">close</label>
            <input type="checkbox" id="show_denom"><label for="show_denom">denom</label>
            <input type="checkbox" id="show_morph"><label for="show_morph">morph</label>
            <input type="checkbox" id="show_numor"><label for="show_numor">numor</label>
            <input type="checkbox" id="show_keg_active_hx"><label for="show_keg_active_hx">keg_active_hx</label>
        </div>
        
        <div id="kegTreeContainer" class="keg_tree_display"></div>
        
        <script src="/static/app.js"></script>
    </body>
    </html>
    """


@app.route("/")
def index():
    """Serve the main HTML page"""
    return render_template_string(get_plan_viewer_template())


@app.route("/api/planunit_view")
def get_planunit_view():
    """API endpoint to get the PlanUnit data with readable strings as JSON"""
    # return jsonify(root.to_dict())
    sue_plan = get_sue_plan_with_facts_and_reasons()
    add_epoch_kegunit(sue_plan, get_default_epoch_config_dict())
    sue_plan.cashout()
    plan_view_dict = get_plan_view_dict(sue_plan)
    return jsonify(plan_view_dict)


if __name__ == "__main__":
    app.run(debug=True)
