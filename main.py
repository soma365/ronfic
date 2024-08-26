from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLAlchemy 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    session = db.Column(db.String(10), nullable=False)
    registrationDate = db.Column(db.String(10))
    measurementDate = db.Column(db.String(10))
    birthDate = db.Column(db.String(10))
    school = db.Column(db.String(100))
    sport = db.Column(db.String(100))
    balanceStatic = db.Column(db.Integer)
    balanceDynamic = db.Column(db.Integer)
    endurance = db.Column(db.Integer)
    strengthSpeed = db.Column(db.Integer)
    speedJump = db.Column(db.Integer)
    speedShuttle = db.Column(db.Integer)
    legPress = db.Column(db.Integer)
    armPull = db.Column(db.Integer)
    coreDynamic = db.Column(db.Integer)
    rotation = db.Column(db.Integer)
    swing = db.Column(db.Integer)
    agility = db.Column(db.Integer)
    upperBalance = db.Column(db.Integer)
    lowerBalance = db.Column(db.Integer)

# 데이터베이스 초기화 (테이블 생성)
with app.app_context():
    db.create_all()

# 메인 페이지 라우트
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 폼 데이터 처리
        name = request.form['name']
        session = request.form['session']
        registration_date = request.form['registrationDate']
        measurement_date = request.form['measurementDate']
        birth_date = request.form['birthDate']
        school = request.form['school']
        sport = request.form['sport']
        balance_static = request.form['balanceStatic']
        balance_dynamic = request.form['balanceDynamic']
        endurance = request.form['endurance']
        strength_speed = request.form['strengthSpeed']
        speed_jump = request.form['speedJump']
        speed_shuttle = request.form['speedShuttle']
        leg_press = request.form['legPress']
        arm_pull = request.form['armPull']
        core_dynamic = request.form['coreDynamic']
        rotation = request.form['rotation']
        swing = request.form['swing']
        agility = request.form['agility']
        upper_balance = request.form['upperBalance']
        lower_balance = request.form['lowerBalance']

        # 데이터베이스에 저장
        new_data = UserData(
            name=name,
            session=session,
            registrationDate=registration_date,
            measurementDate=measurement_date,
            birthDate=birth_date,
            school=school,
            sport=sport,
            balanceStatic=balance_static,
            balanceDynamic=balance_dynamic,
            endurance=endurance,
            strengthSpeed=strength_speed,
            speedJump=speed_jump,
            speedShuttle=speed_shuttle,
            legPress=leg_press,
            armPull=arm_pull,
            coreDynamic=core_dynamic,
            rotation=rotation,
            swing=swing,
            agility=agility,
            upperBalance=upper_balance,
            lowerBalance=lower_balance
        )

        db.session.add(new_data)
        db.session.commit()

        return redirect(url_for('results', name=name))

    return render_template('index.html')

# 검색 라우트
@app.route('/search', methods=['GET'])
def search():
    search_name = request.args.get('searchName')
    if not search_name:
        return redirect(url_for('index'))

    last_session = UserData.query.filter_by(name=search_name).order_by(UserData.id.desc()).first()

    if not last_session:
        popup_message = "해당 이름이 존재하지 않습니다. 신규 이용자입니다."
        return render_template('index.html', popup_message=popup_message)

    show_results_button = True
    session_number = last_session.session
    if session_number == '1':
        popup_message = "1회차 입력완료 이용자입니다."
    elif session_number == '2':
        popup_message = "2회차 입력완료 이용자입니다."
    elif session_number == '3':
        popup_message = "3회차 입력완료 이용자입니다."
    elif session_number == '4':
        popup_message = "4회차 입력완료 이용자입니다."
    else:
        popup_message = "이전 입력된 회차가 없습니다."
        show_results_button = False

    return render_template('index.html',
                           name=last_session.name,
                           registrationDate=last_session.registrationDate,
                           measurementDate=last_session.measurementDate,
                           birthDate=last_session.birthDate,
                           school=last_session.school,
                           sport=last_session.sport,
                           popup_message=popup_message,
                           show_results_button=show_results_button)

# 결과 페이지 라우트
@app.route('/results/<name>')
def results(name):
    sessions = UserData.query.filter_by(name=name).all()

    sessions_dict = [
        {
            "id": session.id,
            "measurementDate": session.measurementDate,
            "balanceStatic": session.balanceStatic,
            "balanceDynamic": session.balanceDynamic,
            "endurance": session.endurance,
            "strengthSpeed": session.strengthSpeed,
            "speedJump": session.speedJump,
            "speedShuttle": session.speedShuttle,
            "legPress": session.legPress,
            "armPull": session.armPull,
            "coreDynamic": session.coreDynamic,
            "rotation": session.rotation,
            "swing": session.swing,
            "agility": session.agility,
            "upperBalance": session.upperBalance,
            "lowerBalance": session.lowerBalance
        }
        for session in sessions
    ]

    return render_template('results.html', sessions=sessions_dict, name=name)

# 데이터 관리 페이지 라우트
@app.route('/data')
def data():
    sessions = UserData.query.all()
    return render_template('data.html', sessions=sessions)

# 수정 페이지 라우트
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    session = UserData.query.get_or_404(id)
    if request.method == 'POST':
        session.name = request.form['name']
        session.session = request.form['session']
        session.registrationDate = request.form['registrationDate']
        session.measurementDate = request.form['measurementDate']
        session.birthDate = request.form['birthDate']
        session.school = request.form['school']
        session.sport = request.form['sport']
        # 필요한 다른 필드들 업데이트...

        db.session.commit()
        return redirect(url_for('data'))

    return render_template('edit.html', session=session)

# 삭제 라우트
@app.route('/delete/<int:id>')
def delete(id):
    session = UserData.query.get_or_404(id)
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for('data'))

# CSV 다운로드 라우트
@app.route('/download_csv', methods=['POST'])
def download_csv():
    # CSV 파일 생성 및 다운로드 코드
    return "CSV 파일을 생성하고 다운로드할 수 있도록 설정합니다."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
