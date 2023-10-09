from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///decision_trees.db'
db = SQLAlchemy(app)

# Define a basic model for decision trees
class DecisionTree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

@app.route('/')
def index():
    # Fetch all decision trees from the database within the app context
    with app.app_context():
        decision_trees = DecisionTree.query.all()
    return render_template('index.html', decision_trees=decision_trees)

@app.route('/create_tree', methods=['POST'])
def create_tree():
    # Create a new decision tree within the app context
    with app.app_context():
        name = request.form['name']
        description = request.form['description']
        new_tree = DecisionTree(name=name, description=description)
        db.session.add(new_tree)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/tree/<int:id>')
def view_tree(id):
    # Fetch a specific decision tree by its ID within the app context
    with app.app_context():
        tree = DecisionTree.query.get(id)
    return render_template('tree.html', tree=tree)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
