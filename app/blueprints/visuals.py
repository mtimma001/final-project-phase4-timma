from flask import Blueprint, render_template, request
from app.db_connect import get_db
from ..functions import generate_statistics, generate_visualizations, fetch_and_filter_data
import pandas as pd

visuals = Blueprint('visuals', __name__)

@visuals.route('/visuals', methods=['GET', 'POST'])
def show_visuals():
    connection = get_db()
    query = "SELECT trial_id, trial_name FROM trials"
    with connection.cursor() as cursor:
        cursor.execute(query)
        trials = cursor.fetchall()

    plot_html = None
    stats = None
    selected_trial = None
    start_date = None
    end_date = None

    if request.method == 'POST':
        selected_trial = request.form.get('trial_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        df = fetch_and_filter_data(selected_trial, start_date, end_date)

        if not df.empty:
            stats = generate_statistics(df)
            plot_html = generate_visualizations(df, single_outcome=False)
    else:
        df = fetch_and_filter_data(None, None, None)
        if not df.empty:
            stats = generate_statistics(df)
            plot_html = generate_visualizations(df, single_outcome=False)

    return render_template('visuals/visuals.html', trials=trials, plot_html=plot_html, stats=stats, selected_trial=selected_trial, start_date=start_date, end_date=end_date)


@visuals.route('/visuals/<int:outcome_id>', methods=['GET'])
def show_single_outcome_visuals(outcome_id):
    connection = get_db()
    query = """
        SELECT o.outcome_id, o.participant_id, o.trial_id, o.outcome_date, o.outcome_details, o.result,
               p.first_name, p.last_name, t.trial_name
        FROM outcomes o
        JOIN participants p ON o.participant_id = p.participant_id
        JOIN trials t ON o.trial_id = t.trial_id
        WHERE o.outcome_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (outcome_id,))
        result = cursor.fetchall()

    if not result:
        return render_template('visuals/visuals.html', plot_html=None, stats=None, message="No data available for this outcome.")

    df = pd.DataFrame(result, columns=['outcome_id', 'participant_id', 'trial_id', 'outcome_date', 'outcome_details', 'result', 'first_name', 'last_name', 'trial_name'])
    stats = generate_statistics(df)
    plot_html = generate_visualizations(df, single_outcome=True)

    return render_template('visuals/visuals.html', plot_html=plot_html, stats=stats, message=None)
