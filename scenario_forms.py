#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scenario_add_form import ScenarioAddForm
from scenario_edit_form import ScenarioEditForm

class ScenarioForms:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.add_form = ScenarioAddForm(db_manager, show_popup_callback)
        self.edit_form = ScenarioEditForm(db_manager, show_popup_callback)
    
    def add_scenario(self, current_profile, refresh_callback):
        """Add new scenario with test step selection from groups"""
        return self.add_form.add_scenario(current_profile, refresh_callback)
    
    def edit_scenario(self, scenario_id, current_profile, refresh_callback):
        """Edit scenario with step management"""
        return self.edit_form.edit_scenario(scenario_id, current_profile, refresh_callback)
