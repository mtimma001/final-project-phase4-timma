from flask import Blueprint, render_template, request
from app.db_connect import get_db
from ..functions import generate_statistics, generate_visualizations, fetch_and_filter_data
import pandas as pd

visuals = Blueprint('visuals', __name__)

@visuals.route('/visuals', methods=['GET', 'POST'])
def show_visuals():
    connection = get_db()

    # Fetch trials and participants for filters
    with connection.cursor() as cursor:
        cursor.execute("SELECT trial_id, trial_name FROM trials")
        trials = cursor.fetchall()

        cursor.execute("SELECT participant_id, first_name, last_name FROM participants")
        participants = cursor.fetchall()

    # Initialize variables
    plot_html = None
    stats = None
    selected_trial_name = "All Trials"
    selected_participant_name = "All Participants"
    selected_trial = None
    selected_participant = None
    start_date = None
    end_date = None

    if request.method == 'POST':
        # Capture filters
        selected_trial = request.form.get('trial_id')
        selected_participant = request.form.get('participant_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Get display names for selected filters
        if selected_trial:
            selected_trial_name = next((trial['trial_name'] for trial in trials
                                        if str(trial['trial_id']) == selected_trial), "All Trials")
        if selected_participant:
            selected_participant_name = next((f"{participant['first_name']} {participant['last_name']}"
                                              for participant in participants
                                              if str(participant['participant_id']) == selected_participant),
                                             "All Participants")

        # Fetch filtered data
        df = fetch_and_filter_data(selected_trial, selected_participant, start_date, end_date)
        if not df.empty:
            stats = generate_statistics(df)
            plot_html = generate_visualizations(df, single_outcome=False)
    else:
        # Default data display
        df = fetch_and_filter_data(None, None, None, None)
        if not df.empty:
            stats = generate_statistics(df)
            plot_html = generate_visualizations(df, single_outcome=False)

    return render_template('visuals.html',
                           trials=trials, participants=participants,
                           plot_html=plot_html, stats=stats,
                           selected_trial_name=selected_trial_name,
                           selected_participant_name=selected_participant_name,
                           start_date=start_date, end_date=end_date)

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
