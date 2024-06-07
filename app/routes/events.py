from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Event, Registration, User

# Define the Blueprint for event routes
events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def events():
    """
    Route to display all events.
    """
    if 'user_id' in session:
        events = Event.query.all()
        return render_template('events.html', events=events, active_page='events')
    return redirect(url_for('auth.login'))

@events_bp.route('/my_events')
def my_events():
    """
    Route to display events the current user is registered for.
    """
    if 'user_id' in session:
        user_id = session['user_id']
        events = db.session.query(Event).join(Registration).filter(Registration.user_id == user_id).all()
        return render_template('my_events.html', events=events, active_page='my_events')
    return redirect(url_for('auth.login'))

@events_bp.route('/register_event/<int:event_id>')
def register_event(event_id):
    """
    Route to register the current user for an event.
    """
    if 'user_id' in session:
        user_id = session['user_id']

        # Check if user is already registered for the event
        registration = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
        if registration:
            flash('You are already registered for this event.', 'warning')
            return redirect(url_for('events.events'))

        # Register the user for the event
        new_registration = Registration(user_id=user_id, event_id=event_id)
        db.session.add(new_registration)
        db.session.commit()

        flash('You have successfully registered for the event.', 'success')
        return redirect(url_for('events.events'))
    return redirect(url_for('auth.login'))

@events_bp.route('/create_event', methods=['GET', 'POST'])
def create_event():
    """
    Route to create a new event. Handles both GET and POST requests.
    """
    if 'user_id' in session:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            date = request.form['date']

            # Create new event
            new_event = Event(name=name, description=description, date=date)
            db.session.add(new_event)
            db.session.commit()

            return redirect(url_for('events.events'))
        return render_template('create_event.html', active_page='events')
    return redirect(url_for('auth.login'))

@events_bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    """
    Route to edit an existing event. Handles both GET and POST requests.
    """
    if 'user_id' in session:
        event = Event.query.get(event_id)

        if request.method == 'POST':
            event.name = request.form['name']
            event.description = request.form['description']
            event.date = request.form['date']
            db.session.commit()

            return redirect(url_for('events.events'))

        return render_template('edit_event.html', event=event, active_page='events')
    return redirect(url_for('auth.login'))

@events_bp.route('/delete_event/<int:event_id>', methods=['GET', 'POST'])
def delete_event(event_id):
    """
    Route to delete an event. Handles both GET and POST requests.
    """
    if 'user_id' in session:
        event = Event.query.get(event_id)

        if request.method == 'POST':
            db.session.delete(event)
            db.session.commit()

            return redirect(url_for('events.events'))

        return render_template('delete_event.html', event_id=event_id, active_page='events')
    return redirect(url_for('auth.login'))

@events_bp.route('/event_participants/<int:event_id>')
def event_participants(event_id):
    """
    Route to display participants of an event.
    """
    if 'user_id' in session:
        participants = db.session.query(User.username, User.email).join(Registration).filter(Registration.event_id == event_id).all()
        return render_template('event_participants.html', participants=participants, active_page='events')
    return redirect(url_for('auth.login'))
