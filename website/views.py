import os
import subprocess

import pygame
from flask import Blueprint, render_template, request, flash, jsonify
# from .models import Note
# from . import db
# from website.sudoku.GUI import game
# from website.flappyBird import flappy
from website.sudoku import app_class

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/contact')
def contact():
    return render_template("contact.html")

@views.route('/sudoku')
def sudoku():
    app_class.run_game()
    return render_template("home.html")


@views.route('/flappyBird')
def flappy_bird():
    os.system('python website/flappyBird/flappy.py')

    return render_template("home.html")
