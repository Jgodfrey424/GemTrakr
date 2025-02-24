# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from firebase_admin import firestore
from jinja2 import TemplateNotFound

db = firestore.client()


@blueprint.route('/index')
@login_required
def index():
    try:
        # Fetch tasks for the logged-in user
        tasks_ref = db.collection("tasks").where("user_id", "==", current_user.id).stream()
        tasks = [{"id": task.id, **task.to_dict()} for task in tasks_ref]

        # 🔥 Fetch Inventory Data 🔥
        inventory_ref = db.collection("inventory").stream()
        inventory = [{"id": item.id, **item.to_dict()} for item in inventory_ref]

        # 📊 Extract Data for Chart 📊
        chart_data = {
            "titles": [item["title"] for item in inventory],
            "costs": [item["cost"] for item in inventory],
            "prices": [item["price"] for item in inventory]
        }

        return render_template(
            'home/index.html', 
            segment='index', 
            tasks=tasks,
            inventory=inventory,  # ✅ Pass inventory list
            chart_data=chart_data  # ✅ Pass chart data
        )

    except Exception as e:
        print(f"Error fetching data: {e}")
        return render_template('home/page-500.html'), 500

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
