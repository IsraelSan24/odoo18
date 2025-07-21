/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ScorecardListRenderer extends Component {
    setup() {
        super.setup();
        this.orm = useService("orm");
        onMounted(() => {
            this.addTooltips();
        });
        onWillUnmount(() => {
            this.removeTooltips();
        });
    }

    async addTooltips() {
        const skillCells = this.el.querySelectorAll('.o_field_cell[name="score_skill_id"]');
        
        for (const cell of skillCells) {
            const skillId = cell.querySelector('.o_field_widget')?.textContent;
            if (skillId) {
                try {
                    const skills = await this.orm.searchRead(
                        'recruitment.score.skill',
                        [['name', '=', skillId.trim()]],
                        ['description']
                    );
                    
                    if (skills.length > 0 && skills[0].description) {
                        this.createTooltip(cell, skills[0].description);
                    }
                } catch (error) {
                    console.error('Error fetching skill description:', error);
                }
            }
        }
    }

    createTooltip(element, description) {
        const wrapper = document.createElement('div');
        wrapper.className = 'skill-tooltip';
        wrapper.innerHTML = element.innerHTML;
        
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-text';
        tooltip.textContent = description;
        
        wrapper.appendChild(tooltip);
        element.innerHTML = '';
        element.appendChild(wrapper);
    }

    removeTooltips() {
        const tooltips = this.el.querySelectorAll('.skill-tooltip');
        tooltips.forEach(tooltip => tooltip.remove());
    }
}

registry.category("views").add("scorecard_list", {
    type: "list",
    display_name: "Scorecard List",
    icon: "fa fa-star",
    multiRecord: true,
    Controller: ScorecardListRenderer,
});