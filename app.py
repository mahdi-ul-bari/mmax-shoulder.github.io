from flask import Flask, render_template, request, session, redirect, url_for
# CHANGED: Import from the new file name
from Shoulder_MMAx import build_shoulder_diagnosis_tree

app = Flask(__name__)
app.secret_key = 'shoulder_secret_key'

def get_current_node_from_history(history_indices):
    """
    Replays the choices made by the user to find the current node.
    """
    node = build_shoulder_diagnosis_tree()
    for index in history_indices:
        paths = list(node.children.keys())
        if index < len(paths):
            path_key = paths[index]
            node = node.children[path_key]
        else:
            break
    return node

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice is not None:
            session['history'].append(int(choice))
            session.modified = True
            return redirect(url_for('index'))

    current_node = get_current_node_from_history(session['history'])
    paths = list(current_node.children.keys())

    return render_template('index.html', node=current_node, paths=paths)

@app.route('/reset')
def reset():
    session.pop('history', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
