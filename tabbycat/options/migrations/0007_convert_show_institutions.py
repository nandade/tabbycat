# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-19 12:00

# This is a data migration. Its purpose is to convert the old "show
# institutions" preferences to the new "show team institutions" and "show
# adjudicator institutions" preferences. If the old preference doesn't exist,
# the migration silently fails.

from __future__ import unicode_literals

from django.db import migrations


def convert_show_institutions(apps, schema_editor):
    TournamentPreferenceModel = apps.get_model("options", "TournamentPreferenceModel")

    old_prefs = TournamentPreferenceModel.objects.filter(section="ui_options",
            name="show_institutions")

    for pref in old_prefs:

        # Ordinarily, we're not really meant to access the `raw_value` field
        # directly. But with data migrations the model we're dealing with (the
        # historical version) doesn't actually have any of the non-field
        # properties (i.e., `pref.value` would raise an AttributeError), so we
        # don't really have a choice here.
        value = pref.raw_value

        # Copy to each of the two new values
        for name in ["show_team_institutions", "show_adjudicator_institutions"]:
            # If there already exists a preference, leave it alone.
            if not TournamentPreferenceModel.objects.filter(section="ui_options",
                    name=name, instance_id=pref.instance_id).exists():
                TournamentPreferenceModel.objects.create(section="ui_options",
                        name=name, instance_id=pref.instance_id, raw_value=value)

        # The checkpreferences command would do this, but since this preference
        # doesn't exist anymore, we may as well delete it now.
        pref.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0006_convert_panellist_feedback_preference'),
    ]

    operations = [
        migrations.RunPython(convert_show_institutions),
    ]
