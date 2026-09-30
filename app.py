from flask import Flask, jsonify, request

app = Flask(__name__)


# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# In-memory database
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# CREATE - Add a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Check that title was provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Create a new ID
    new_id = max(event.id for event in events) + 1

    # Create the event
    new_event = Event(new_id, data["title"])

    # Add it to the list
    events.append(new_event)

    # Return the new event
    return jsonify(new_event.to_dict()), 201


# UPDATE - Change an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    # Check that title was provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Look for the event
    for event in events:
        if event.id == event_id:
            # Update the title
            event.title = data["title"]

            # Return updated event
            return jsonify(event.to_dict()), 200

    # Event was not found
    return jsonify({"error": "Event not found"}), 404


# DELETE - Remove an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    # Look for the event
    for event in events:
        if event.id == event_id:

            # Remove the event
            events.remove(event)

            # 204 means successful deletion with no response body
            return "", 204

    # Event was not found
    return jsonify({"error": "Event not found"}), 404


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
