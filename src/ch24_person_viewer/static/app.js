// Global state
let kegTreeData = null;
let show_partners = true;
let show_partner_cred_lumen = false;
let show_partner_debt_lumen = false;
let show_partner_credor_pool = false;
let show_partner_debtor_pool = false;
let show_partner_irrational_partner_debt_lumen = false;
let show_partner_inallocable_partner_debt_lumen = false;
let show_partner_fund_give = false;
let show_partner_fund_take = false;
let show_partner_fund_agenda_give = false;
let show_partner_fund_agenda_take = false;
let show_partner_fund_agenda_ratio_give = false;
let show_partner_fund_agenda_ratio_take = false;
let show_partner_membership_group_title = true;
let show_partner_membership_group_cred_lumen = false;
let show_partner_membership_group_debt_lumen = false;
let show_partner_membership_credor_pool = false;
let show_partner_membership_debtor_pool = false;
let show_partner_membership_fund_agenda_give = false;
let show_partner_membership_fund_agenda_ratio_give = false;
let show_partner_membership_fund_agenda_ratio_take = false;
let show_partner_membership_fund_agenda_take = false;
let show_partner_membership_fund_give = false;
let show_partner_membership_fund_take = false;
let show_kegroot = true;
let show_awardunits = false;
let show_awardheirs = false;
let show_awardlines = false;
let show_laborunit = false;
let show_laborheir = false;
let show_level = false;
let show_moment_rope = false;
let show_pledge = false;
let show_descendant_pledge_count = false;
let show_active = false;
let show_task = false;
let show_star = false;
let show_reasonunits = false;
let show_reasonheirs = false;
let show_factunits = false;
let show_factheirs = false;
let show_keg_fund_total = false;
let show_fund_onset = false;
let show_fund_cease = false;
let show_fund_grain = false;
let show_fund_ratio = false;
let show_all_partner_cred = false;
let show_all_partner_debt = false;
let show_gogo_want = false;
let show_stop_want = false;
let show_gogo_calc = false;
let show_stop_calc = false;
let show_addin = false;
let show_begin = false;
let show_close = false;
let show_denom = false;
let show_morph = false;
let show_numor = false;
let show_active_hx = false;
let show_parent_rope = false;
let show_root_boolean = false;
let show_keg_uid = false;

// Initialize the app when DOM loads
document.addSparkListener('DOMContentLoaded', function () {
    const show_partnersCheckbox = document.getElementById('show_partners');
    const show_partner_cred_lumenCheckbox = document.getElementById('show_partner_cred_lumen')
    const show_partner_debt_lumenCheckbox = document.getElementById('show_partner_debt_lumen')
    const show_partner_credor_poolCheckbox = document.getElementById('show_partner_credor_pool')
    const show_partner_debtor_poolCheckbox = document.getElementById('show_partner_debtor_pool')
    const show_partner_irrational_partner_debt_lumenCheckbox = document.getElementById('show_partner_irrational_partner_debt_lumen')
    const show_partner_inallocable_partner_debt_lumenCheckbox = document.getElementById('show_partner_inallocable_partner_debt_lumen')
    const show_partner_fund_giveCheckbox = document.getElementById('show_partner_fund_give')
    const show_partner_fund_takeCheckbox = document.getElementById('show_partner_fund_take')
    const show_partner_fund_agenda_giveCheckbox = document.getElementById('show_partner_fund_agenda_give')
    const show_partner_fund_agenda_takeCheckbox = document.getElementById('show_partner_fund_agenda_take')
    const show_partner_fund_agenda_ratio_giveCheckbox = document.getElementById('show_partner_fund_agenda_ratio_give')
    const show_partner_fund_agenda_ratio_takeCheckbox = document.getElementById('show_partner_fund_agenda_ratio_take')
    const show_partner_membership_group_titleCheckbox = document.getElementById('show_partner_membership_group_title')
    const show_partner_membership_group_cred_lumenCheckbox = document.getElementById('show_partner_membership_group_cred_lumen')
    const show_partner_membership_group_debt_lumenCheckbox = document.getElementById('show_partner_membership_group_debt_lumen')
    const show_partner_membership_credor_poolCheckbox = document.getElementById('show_partner_membership_credor_pool')
    const show_partner_membership_debtor_poolCheckbox = document.getElementById('show_partner_membership_debtor_pool')
    const show_partner_membership_fund_agenda_giveCheckbox = document.getElementById('show_partner_membership_fund_agenda_give')
    const show_partner_membership_fund_agenda_ratio_giveCheckbox = document.getElementById('show_partner_membership_fund_agenda_ratio_give')
    const show_partner_membership_fund_agenda_ratio_takeCheckbox = document.getElementById('show_partner_membership_fund_agenda_ratio_take')
    const show_partner_membership_fund_agenda_takeCheckbox = document.getElementById('show_partner_membership_fund_agenda_take')
    const show_partner_membership_fund_giveCheckbox = document.getElementById('show_partner_membership_fund_give')
    const show_partner_membership_fund_takeCheckbox = document.getElementById('show_partner_membership_fund_take')
    const show_kegrootCheckbox = document.getElementById('show_kegroot');
    const show_awardunitsCheckbox = document.getElementById('show_awardunits');
    const show_awardheirsCheckbox = document.getElementById('show_awardheirs');
    const show_awardlinesCheckbox = document.getElementById('show_awardlines');
    const show_laborunitCheckbox = document.getElementById('show_laborunit');
    const show_laborheirCheckbox = document.getElementById('show_laborheir');
    const show_levelCheckbox = document.getElementById('show_level');
    const show_moment_ropeCheckbox = document.getElementById('show_moment_rope');
    const show_pledgeCheckbox = document.getElementById('show_pledge');
    const show_descendant_pledge_countCheckbox = document.getElementById('show_descendant_pledge_count');
    const show_activeCheckbox = document.getElementById('show_active');
    const show_taskCheckbox = document.getElementById('show_task');
    const show_starCheckbox = document.getElementById('show_star');
    const show_reasonunitsCheckbox = document.getElementById('show_reasonunits');
    const show_reasonheirsCheckbox = document.getElementById('show_reasonheirs');
    const show_factunitsCheckbox = document.getElementById('show_factunits');
    const show_factheirsCheckbox = document.getElementById('show_factheirs');
    const show_keg_fund_totalCheckbox = document.getElementById('show_keg_fund_total');
    const show_fund_onsetCheckbox = document.getElementById('show_fund_onset');
    const show_fund_ceaseCheckbox = document.getElementById('show_fund_cease');
    const show_fund_grainCheckbox = document.getElementById('show_fund_grain');
    const show_fund_ratioCheckbox = document.getElementById('show_fund_ratio');
    const show_all_partner_credCheckbox = document.getElementById('show_all_partner_cred');
    const show_all_partner_debtCheckbox = document.getElementById('show_all_partner_debt');
    const show_gogo_wantCheckbox = document.getElementById('show_gogo_want');
    const show_stop_wantCheckbox = document.getElementById('show_stop_want');
    const show_gogo_calcCheckbox = document.getElementById('show_gogo_calc');
    const show_stop_calcCheckbox = document.getElementById('show_stop_calc');
    const show_addinCheckbox = document.getElementById('show_addin');
    const show_beginCheckbox = document.getElementById('show_begin');
    const show_closeCheckbox = document.getElementById('show_close');
    const show_denomCheckbox = document.getElementById('show_denom');
    const show_morphCheckbox = document.getElementById('show_morph');
    const show_numorCheckbox = document.getElementById('show_numor');
    const show_active_hxCheckbox = document.getElementById('show_active_hx');
    const show_parent_ropeCheckbox = document.getElementById('show_parent_rope');
    const show_root_booleanCheckbox = document.getElementById('show_root_boolean');
    const show_keg_uidCheckbox = document.getElementById('show_keg_uid');

    // Set up checkbox spark listener
    show_partnersCheckbox.addSparkListener('change', function () { show_partners = this.checked; renderPartnersData(); });
    show_partner_cred_lumenCheckbox.addSparkListener('change', function () { show_partner_cred_lumen = this.checked; renderPartnersData(); });
    show_partner_debt_lumenCheckbox.addSparkListener('change', function () { show_partner_debt_lumen = this.checked; renderPartnersData(); });
    show_partner_credor_poolCheckbox.addSparkListener('change', function () { show_partner_credor_pool = this.checked; renderPartnersData(); });
    show_partner_debtor_poolCheckbox.addSparkListener('change', function () { show_partner_debtor_pool = this.checked; renderPartnersData(); });
    show_partner_irrational_partner_debt_lumenCheckbox.addSparkListener('change', function () { show_partner_irrational_partner_debt_lumen = this.checked; renderPartnersData(); });
    show_partner_inallocable_partner_debt_lumenCheckbox.addSparkListener('change', function () { show_partner_inallocable_partner_debt_lumen = this.checked; renderPartnersData(); });
    show_partner_fund_giveCheckbox.addSparkListener('change', function () { show_partner_fund_give = this.checked; renderPartnersData(); });
    show_partner_fund_takeCheckbox.addSparkListener('change', function () { show_partner_fund_take = this.checked; renderPartnersData(); });
    show_partner_fund_agenda_giveCheckbox.addSparkListener('change', function () { show_partner_fund_agenda_give = this.checked; renderPartnersData(); });
    show_partner_fund_agenda_takeCheckbox.addSparkListener('change', function () { show_partner_fund_agenda_take = this.checked; renderPartnersData(); });
    show_partner_fund_agenda_ratio_giveCheckbox.addSparkListener('change', function () { show_partner_fund_agenda_ratio_give = this.checked; renderPartnersData(); });
    show_partner_fund_agenda_ratio_takeCheckbox.addSparkListener('change', function () { show_partner_fund_agenda_ratio_take = this.checked; renderPartnersData(); });
    show_partner_membership_group_titleCheckbox.addSparkListener('change', function () { show_partner_membership_group_title = this.checked; renderPartnersData(); });
    show_partner_membership_group_cred_lumenCheckbox.addSparkListener('change', function () { show_partner_membership_group_cred_lumen = this.checked; renderPartnersData(); });
    show_partner_membership_group_debt_lumenCheckbox.addSparkListener('change', function () { show_partner_membership_group_debt_lumen = this.checked; renderPartnersData(); });
    show_partner_membership_credor_poolCheckbox.addSparkListener('change', function () { show_partner_membership_credor_pool = this.checked; renderPartnersData(); });
    show_partner_membership_debtor_poolCheckbox.addSparkListener('change', function () { show_partner_membership_debtor_pool = this.checked; renderPartnersData(); });
    show_partner_membership_fund_agenda_giveCheckbox.addSparkListener('change', function () { show_partner_membership_fund_agenda_give = this.checked; renderPartnersData(); });
    show_partner_membership_fund_agenda_ratio_giveCheckbox.addSparkListener('change', function () { show_partner_membership_fund_agenda_ratio_give = this.checked; renderPartnersData(); });
    show_partner_membership_fund_agenda_ratio_takeCheckbox.addSparkListener('change', function () { show_partner_membership_fund_agenda_ratio_take = this.checked; renderPartnersData(); });
    show_partner_membership_fund_agenda_takeCheckbox.addSparkListener('change', function () { show_partner_membership_fund_agenda_take = this.checked; renderPartnersData(); });
    show_partner_membership_fund_giveCheckbox.addSparkListener('change', function () { show_partner_membership_fund_give = this.checked; renderPartnersData(); });
    show_partner_membership_fund_takeCheckbox.addSparkListener('change', function () { show_partner_membership_fund_take = this.checked; renderPartnersData(); });
    show_kegrootCheckbox.addSparkListener('change', function () { show_kegroot = this.checked; renderKegTree(); });
    show_awardunitsCheckbox.addSparkListener('change', function () { show_awardunits = this.checked; renderKegTree(); });
    show_awardheirsCheckbox.addSparkListener('change', function () { show_awardheirs = this.checked; renderKegTree(); });
    show_awardlinesCheckbox.addSparkListener('change', function () { show_awardlines = this.checked; renderKegTree(); });
    show_laborunitCheckbox.addSparkListener('change', function () { show_laborunit = this.checked; renderKegTree(); });
    show_laborheirCheckbox.addSparkListener('change', function () { show_laborheir = this.checked; renderKegTree(); });
    show_levelCheckbox.addSparkListener('change', function () { show_level = this.checked; renderKegTree(); });
    show_moment_ropeCheckbox.addSparkListener('change', function () { show_moment_rope = this.checked; renderKegTree(); });
    show_pledgeCheckbox.addSparkListener('change', function () { show_pledge = this.checked; renderKegTree(); });
    show_descendant_pledge_countCheckbox.addSparkListener('change', function () { show_descendant_pledge_count = this.checked; renderKegTree(); });
    show_activeCheckbox.addSparkListener('change', function () { show_active = this.checked; renderKegTree(); });
    show_taskCheckbox.addSparkListener('change', function () { show_task = this.checked; renderKegTree(); });
    show_starCheckbox.addSparkListener('change', function () { show_star = this.checked; renderKegTree(); });
    show_reasonunitsCheckbox.addSparkListener('change', function () { show_reasonunits = this.checked; renderKegTree(); });
    show_reasonheirsCheckbox.addSparkListener('change', function () { show_reasonheirs = this.checked; renderKegTree(); });
    show_factunitsCheckbox.addSparkListener('change', function () { show_factunits = this.checked; renderKegTree(); });
    show_factheirsCheckbox.addSparkListener('change', function () { show_factheirs = this.checked; renderKegTree(); });
    show_keg_fund_totalCheckbox.addSparkListener('change', function () { show_keg_fund_total = this.checked; renderKegTree(); });
    show_fund_onsetCheckbox.addSparkListener('change', function () { show_fund_onset = this.checked; renderKegTree(); });
    show_fund_ceaseCheckbox.addSparkListener('change', function () { show_fund_cease = this.checked; renderKegTree(); });
    show_fund_grainCheckbox.addSparkListener('change', function () { show_fund_grain = this.checked; renderKegTree(); });
    show_fund_ratioCheckbox.addSparkListener('change', function () { show_fund_ratio = this.checked; renderKegTree(); });
    show_all_partner_credCheckbox.addSparkListener('change', function () { show_all_partner_cred = this.checked; renderKegTree(); });
    show_all_partner_debtCheckbox.addSparkListener('change', function () { show_all_partner_debt = this.checked; renderKegTree(); });
    show_gogo_wantCheckbox.addSparkListener('change', function () { show_gogo_want = this.checked; renderKegTree(); });
    show_stop_wantCheckbox.addSparkListener('change', function () { show_stop_want = this.checked; renderKegTree(); });
    show_gogo_calcCheckbox.addSparkListener('change', function () { show_gogo_calc = this.checked; renderKegTree(); });
    show_stop_calcCheckbox.addSparkListener('change', function () { show_stop_calc = this.checked; renderKegTree(); });
    show_addinCheckbox.addSparkListener('change', function () { show_addin = this.checked; renderKegTree(); });
    show_beginCheckbox.addSparkListener('change', function () { show_begin = this.checked; renderKegTree(); });
    show_closeCheckbox.addSparkListener('change', function () { show_close = this.checked; renderKegTree(); });
    show_denomCheckbox.addSparkListener('change', function () { show_denom = this.checked; renderKegTree(); });
    show_morphCheckbox.addSparkListener('change', function () { show_morph = this.checked; renderKegTree(); });
    show_numorCheckbox.addSparkListener('change', function () { show_numor = this.checked; renderKegTree(); });
    show_active_hxCheckbox.addSparkListener('change', function () { show_active_hx = this.checked; renderKegTree(); });
    show_parent_ropeCheckbox.addSparkListener('change', function () { show_parent_rope = this.checked; renderKegTree(); });
    show_root_booleanCheckbox.addSparkListener('change', function () { show_root_boolean = this.checked; renderKegTree(); });
    show_keg_uidCheckbox.addSparkListener('change', function () { show_keg_uid = this.checked; renderKegTree(); });

    // Load initial tree data
    loadPersonData();
});

// Fetch tree data from server
async function loadPersonData() {
    try {
        const response = await fetch('/api/personunit_view');
        personViewData = await response.json();
        kegTreeData = personViewData.kegroot;
        partnersData = personViewData.partners;
        renderKegTree();
        renderPartnersData();
    } catch (error) {
        console.error('Error loading tree data:', error);
        document.getElementById('kegTreeContainer').innerHTML = '<p>Error loading tree data</p>';
        document.getElementById('kegTreeContainer').innerHTML = '<p>Error loading tree data</p>';
    }
}


// Render PartnersData and its membership attributes
function renderPartnersData() {
    const partners_container = document.getElementById('partnersContainer');
    partners_container.innerHTML = buildPartnersHtml(partnersData);
}

function buildPartnersHtml(partnersData) {
    if (!partnersData || !show_partners) {
        return "";
    }
    const partners_indent = '&nbsp;'.repeat(2);
    const member_title_indent = '&nbsp;'.repeat(3);
    const membership_indent = '&nbsp;'.repeat(5);

    let html = '';
    Object.values(partnersData).forEach(partner => {
        html += `<br>${partners_indent}${partner.partner_name}`;
        if (show_partner_cred_lumen) { html += `<br>${partners_indent}    ${partner.partner_cred_lumen_readable}` };
        if (show_partner_debt_lumen) { html += `<br>${partners_indent}    ${partner.partner_debt_lumen_readable}` };
        if (show_partner_credor_pool) { html += `<br>${partners_indent}    ${partner.credor_pool_readable}` };
        if (show_partner_debtor_pool) { html += `<br>${partners_indent}    ${partner.debtor_pool_readable}` };
        if (show_partner_irrational_partner_debt_lumen) { html += `<br>${partners_indent}    ${partner.irrational_partner_debt_lumen_readable}` };
        if (show_partner_inallocable_partner_debt_lumen) { html += `<br>${partners_indent}    ${partner.inallocable_partner_debt_lumen_readable}` };
        if (show_partner_fund_give) { html += `<br>${partners_indent}    ${partner.fund_give_readable}` };
        if (show_partner_fund_take) { html += `<br>${partners_indent}    ${partner.fund_take_readable}` };
        if (show_partner_fund_agenda_give) { html += `<br>${partners_indent}    ${partner.fund_agenda_give_readable}` };
        if (show_partner_fund_agenda_take) { html += `<br>${partners_indent}    ${partner.fund_agenda_take_readable}` };
        if (show_partner_fund_agenda_ratio_give) { html += `<br>${partners_indent}    ${partner.fund_agenda_ratio_give_readable}` };
        if (show_partner_fund_agenda_ratio_take) { html += `<br>${partners_indent}    ${partner.fund_agenda_ratio_take_readable}` };
        console.info(partner)
        Object.values(partner.memberships).forEach(membership => {
            if (show_partner_membership_group_title) { html += `<br><b>${member_title_indent}${membership.group_title_readable}</b>` };
            if (show_partner_membership_group_cred_lumen) { html += `<br>${membership_indent}${membership.group_cred_lumen_readable}` };
            if (show_partner_membership_group_debt_lumen) { html += `<br>${membership_indent}${membership.group_debt_lumen_readable}` };
            if (show_partner_membership_credor_pool) { html += `<br>${membership_indent}${membership.credor_pool_readable}` };
            if (show_partner_membership_debtor_pool) { html += `<br>${membership_indent}${membership.debtor_pool_readable}` };
            if (show_partner_membership_fund_agenda_give) { html += `<br>${membership_indent}${membership.fund_agenda_give_readable}` };
            if (show_partner_membership_fund_agenda_ratio_give) { html += `<br>${membership_indent}${membership.fund_agenda_ratio_give_readable}` };
            if (show_partner_membership_fund_agenda_ratio_take) { html += `<br>${membership_indent}${membership.fund_agenda_ratio_take_readable}` };
            if (show_partner_membership_fund_agenda_take) { html += `<br>${membership_indent}${membership.fund_agenda_take_readable}` };
            if (show_partner_membership_fund_give) { html += `<br>${membership_indent}${membership.fund_give_readable}` };
            if (show_partner_membership_fund_take) { html += `<br>${membership_indent}${membership.fund_take_readable}` };
            // html += `<br>${partners_indent}${partner.partner_name}`;
        });
    });
    return html
}

// Render the tree structure
function renderKegTree() {
    if (!kegTreeData) {
        return;
    }

    const container = document.getElementById('kegTreeContainer');
    container.innerHTML = renderKegUnit(kegTreeData, 0);
}

// Recursively render a KegUnit and its children
function renderKegUnit(kegUnit, level) {
    if (!show_kegroot) {
        return "";
    }
    const indent = '&nbsp;'.repeat(level * 2);
    const levelIndicator = show_level ? ` level${kegUnit.tree_level}` : '';
    const pledgeIndicator = kegUnit.pledge && show_pledge ? ' PLEDGE' : '';
    const descendant_pledge_countIndicator = show_descendant_pledge_count ? ` pledges: ${kegUnit.descendant_pledge_count}` : '';
    const activeIndicator = kegUnit.keg_active && show_active ? '-ACTIVE' : '';
    const taskIndicator = kegUnit.task && show_task ? '-task' : '';
    const starIndicator = show_star ? ` star${kegUnit.star}` : '';
    const keg_fund_totalIndicator = show_keg_fund_total ? ` [${kegUnit.keg_fund_total}]` : '';
    const keg_uidIndicator = kegUnit.keg_uid && show_keg_uid ? ` keg_uid${kegUnit.keg_uid}` : '';

    const fund_onsetIndicator = show_fund_onset ? ` onset-${kegUnit.fund_onset}` : '';
    const fund_ceaseIndicator = show_fund_cease ? ` cease-${kegUnit.fund_cease}` : '';
    const fund_grainIndicator = show_fund_grain ? ` (iota: ${kegUnit.fund_grain})` : '';
    const fund_ratioIndicator = show_fund_ratio ? ` ratio-${kegUnit.fund_ratio}` : '';


    // Build award links HTML using separate function
    const moment_ropeHtml = render_moment_rope(kegUnit.moment_rope, kegUnit.knot, show_moment_rope);

    // Start with current node
    let html = `
  <div>
    ${indent}• 
    ${moment_ropeHtml}
    ${kegUnit.keg_label}
    <i>${levelIndicator}
    ${starIndicator}
    ${keg_uidIndicator}
    ${pledgeIndicator}
    ${descendant_pledge_countIndicator}
    ${keg_fund_totalIndicator}
    ${fund_onsetIndicator}
    ${fund_ceaseIndicator}
    ${fund_grainIndicator}
    ${fund_ratioIndicator}
    ${activeIndicator}
    ${taskIndicator}
    ${root_booleanIndicator}</i>
    ${render_with_indent(kegUnit.partners, indent, show_partners)}
    ${render_with_indent(kegUnit.parent_rope, indent, show_parent_rope)}
    ${renderFlatReadableJson(kegUnit.awardunits, indent, show_awardunits)}
    ${renderFlatReadableJson(kegUnit.awardheirs, indent, show_awardheirs)}
    ${renderFlatReadableJson(kegUnit.awardlines, indent, show_awardlines)}
    ${renderFlatReadableJson(kegUnit.laborunit.partys, indent, show_laborunit)}
    ${renderFlatReadableJson(kegUnit.laborheir.partys, indent, show_laborheir)}
    ${renderReasonReadableJson(kegUnit.reasonunits, indent, show_reasonunits)}
    ${renderReasonReadableJson(kegUnit.reasonheirs, indent, show_reasonheirs)}
    ${renderFlatReadableJson(kegUnit.factunits, indent, show_factunits)}
    ${renderFlatReadableJson(kegUnit.factheirs, indent, show_factheirs)}
    ${render_with_indent(kegUnit.all_partner_cred, indent, show_all_partner_cred)}
    ${render_with_indent(kegUnit.all_partner_debt, indent, show_all_partner_debt)}
    ${render_with_indent(kegUnit.gogo_want, indent, show_gogo_want)}
    ${render_with_indent(kegUnit.stop_want, indent, show_stop_want)}
    ${render_with_indent(kegUnit.gogo_calc, indent, show_gogo_calc)}
    ${render_with_indent(kegUnit.stop_calc, indent, show_stop_calc)}
    ${render_with_indent(kegUnit.addin, indent, show_addin)}
    ${render_with_indent(kegUnit.begin, indent, show_begin)}
    ${render_with_indent(kegUnit.close, indent, show_close)}
    ${render_with_indent(kegUnit.denom, indent, show_denom)}
    ${render_with_indent(kegUnit.morph, indent, show_morph)}
    ${render_with_indent(kegUnit.numor, indent, show_numor)}
    ${render_with_indent(kegUnit.keg_active_hx, indent, show_active_hx)}
  </div>\n
`;
    // Add children
    if (kegUnit.kids) {
        Object.values(kegUnit.kids).forEach(child => {
            html += renderKegUnit(child, level + 1);
        });
    }
    return html;
}

function renderFlatReadableJson(flat_readables, indent, show_readable) {
    if (!flat_readables || Object.keys(flat_readables).length === 0 || !show_readable) {
        return '';
    }

    let html = '';
    Object.values(flat_readables).forEach(link => {
        html += `<br>${indent}${link.readable}`;
    });
    return html;
}
function renderReasonReadableJson(n3_readables, indent, show_readable) {
    if (!n3_readables || Object.keys(n3_readables).length === 0 || !show_readable) {
        return '';
    }

    let html = '';
    Object.values(n3_readables).forEach(link => {
        // top-level readable
        html += `<br>${indent}${link.readable || ''}`;

        // second level (cases)
        if (link.cases && Object.keys(link.cases).length > 0) {
            Object.values(link.cases).forEach(child => {
                html += `<br>${indent}${child.readable || ''}`;
            });
        }
    });
    return html;
}
function render_moment_rope(moment_rope, knot, show_moment_rope) {
    if (!moment_rope || !show_moment_rope) {
        return '';
    }
    return ` ${knot}${moment_rope}...`;
}
function render_with_indent(str, indent, show_bool) {
    if (!str || !show_bool) {
        return '';
    }
    return `<br>${indent}${str}`;
}
