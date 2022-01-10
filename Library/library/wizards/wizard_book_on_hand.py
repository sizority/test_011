from odoo import models, fields


class WizardOnHand(models.TransientModel):
    _name = 'library.wizard.on_hand'

    partner_id = fields.Many2one('res.partner')
    due_date = fields.Date()

    def action_on_hand(self):
        ctx = self._context
        book = self.env[ctx['active_model']].browse(ctx['active_ids'])
        today = fields.Date()

