from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class SoilAnalysis(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Sample_id = db.Column(db.String(50), nullable=False)
    Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Farm = db.Column(db.String(500), nullable=False)
    Lot = db.Column(db.String(50), nullable=False)
    Crop = db.Column(db.String(50), nullable=False)
    pH = db.Column(db.Integer)
    B = db.Column(db.Integer)
    Ca = db.Column(db.Integer)
    Cu = db.Column(db.Integer)
    Fe = db.Column(db.Integer)
    K = db.Column(db.Integer)
    Mg = db.Column(db.Integer)
    Mn = db.Column(db.Integer)
    N = db.Column(db.Integer)
    P = db.Column(db.Integer)
    S = db.Column(db.Integer)
    Zn = db.Column(db.Integer)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        return 'Sample %r' % self.Sample_id

#db.create_all()







@app.route('/')
def login():
    return render_template('home.html')


@app.route('/api/data')
def data():
    all_data = SoilAnalysis.query.all()
    return {'data': [x.to_dict() for x in all_data]}


@app.route('/dashboard')
def dashboard():
    pass


@app.route('/records')
def records():
    return render_template('records.html', data=data)


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    """"
    Read csv file to pandas dataframe and commit the data to sql alchemy database
    """
    if request.method == 'POST':
        f = request.files['pdf_file']

        df = pd.read_csv(f, names=['Sample ID', 'Farm', 'Lot', 'Crop', 'pH', 'B', 'Ca', 'Cu', 'Fe', 'K',
                         'Mg', 'Mn', 'N', 'P', 'S', 'Zn'], skiprows=[0]
                         )

        try:
            for _index, row in df.iterrows():  # loop through pandas dataframe and return each index and row
                sample = SoilAnalysis(
                    Sample_id=row['Sample ID'], Farm=row['Farm'],
                    Lot=row['Lot'], Crop=row['Crop'], pH=row['pH'],
                    B=row['B'], Ca=row['Ca'], Cu=row['Cu'], Fe=row['Fe'],
                    K=row['K'], Mg=row['Mg'], Mn=row['Mn'], N=row['N'],
                    P=row['P'], S=row['S'], Zn=row['Zn']
                )
                db.session.add(sample)
            db.session.commit()
        except Exception as e:
            print('An error while trying to add dataframe to the database')
            print(e)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)