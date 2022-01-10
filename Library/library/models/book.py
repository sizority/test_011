# -*- coding: utf-8 -*-
from random import randint

from odoo import models, fields, api, _


class Author(models.Model):
    _name = 'library.author'

    name = fields.Char()
    country_id = fields.Many2one('res.country')
    city = fields.Char()
    birthday_date = fields.Date()


class Language(models.Model):
    _name = 'library.language'

    name = fields.Char()


class Tag(models.Model):
    _name = 'library.tag'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char()
    color = fields.Integer('Color', default=_get_default_color)


class History(models.Model):
    _name = 'library.history'

    book_id = fields.Many2one('library.book')
    partner_id = fields.Many2one('res.partner')
    date_on_hand = fields.Date()
    date_on_shelf = fields.Date()
    due_date = fields.Date()


class BookInfo(models.Model):
    _name = 'library.book.info'
    _inherit = 'mail.thread'
    _description = 'Book Info'

    name = fields.Char(tracking=True)
    author_id = fields.Many2one('library.author', tracking=True)
    lang_id = fields.Many2one('library.language', tracking=True)
    tag_ids = fields.Many2many('library.tag', tracking=True)
    description = fields.Text(tracking=True)


class Book(models.Model):
    _name = 'library.book'
    _inherit = 'mail.thread'
    _description = 'Book'

    book_id = fields.Many2one('library.book.info')
    name = fields.Char(related='book_id.name', readonly=False)
    number = fields.Char()
    author_id = fields.Many2one(related='book_id.author_id')
    year = fields.Integer()
    lang_id = fields.Many2one(related='book_id.lang_id')
    status = fields.Selection([
        ('on_shelf', 'On shelf'),
        ('on_hand', 'On hand'),
        ('unavailable', 'Unavailable'),
    ], default='on_shelf')
    partner_id = fields.Many2one('res.partner')
    history_id = fields.One2many('library.history', 'book_id')
    tag_ids = fields.Many2many(related='book_id.tag_ids')
    publishing_house = fields.Many2one('res.partner')
    image = fields.Image(string="Image", max_width=256, max_height=256)
    description = fields.Text(related='book_id.description')
    due_date = fields.Date()

    _sql_constraints = [
        ('number_uniq', 'unique (number)', """Only one number can be defined for each book!"""),
    ]

    def action_on_hand(self):
        return {
            'name': _('On Hand %s') % self.name,
            'view_mode': 'form',
            'res_model': 'library.wizard.on_hand',
            'type': 'ir.actions.act_window',
            'target': 'new'
        }
