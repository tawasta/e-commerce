from odoo import models
from odoo import _
from odoo.addons.queue_job.job import job


class User(models.Model):

    _inherit = "res.users"

    @job()
    def _delayed_create_user_from_template(self, values):

        job_desc = _("Create portal user '{}'".format({values.get("email")}))

        self.with_delay(description=job_desc)._delayed_create_user_from_template(values)
