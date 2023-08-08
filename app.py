from flask import Flask, render_template, request, redirect, url_for
import requests


app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True

class InteriorApp:
    def __init__(self):
        self.title = "interior destiny"
        self.layouts = ["1K", "2DK", "3LDK"]  # レイアウトの選択肢を追加する
        self.destinies = ['金運', '恋愛運', '仕事運']
        self.selected_layout = None
        self.selected_destiny = None
        self.fortune_percentage = 0

    def start(self):
        return self.show_title()

    def show_title(self):
        return render_template("title.html", title=self.title)

    def select_layout(self):
        return render_template("select_layout.html", layouts=self.layouts)

    def show_layout_details(self, selected_layout):
        self.selected_layout = selected_layout
        return render_template("layout_details.html", selected_layout=selected_layout)
    
    def select_destiny(self):
        return render_template("select_destiny.html", destinies=self.destinies)
    
    def show_confirmation(self, selected_destiny):
        self.selected_destiny = selected_destiny
        return render_template("confirmation.html", selected_destiny=selected_destiny)


    def confirmation(self, selected_destiny):
        return render_template("confirmation.html", selected_destiny=selected_destiny)
    
    def draw_fortune(self):
        fortune_data = self.get_fortune_data()
        if fortune_data:
            rain_mm = fortune_data.get('hourly', {}).get('rain', 0)
            fortune_result = self.get_fortune_result(rain_mm)
            return render_template("draw_fortune.html", fortune_result=fortune_result, fortune_data=fortune_data)
        else:
            return "Error: Failed to fetch data from the API.app.pyコードのエラー"

    def get_fortune_data(self):
        url = 'https://api.open-meteo.com/v1/forecast'
        
        query_params = {
            'latitude': '35.0211',
            'longitude': '135.7538',
            'hourly': 'rain',
            'timezone': 'Asia/Tokyo',
        }

        response = requests.get(url, params=query_params) # APIにリクエストを送信してレスポンスを取得します

        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print('Error: Failed to fetch data from the API. Status code:', response.status_code)
            return None
        
    def get_fortune_result(self, rain_mm):
        import random
        # 降水量が0mmなら晴れ、それ以外なら雨と判定
        if rain_mm == 0.00:
            fortune = random.choice(['金運の雨', '恋愛運の雨', '仕事運の雨'])
        else:
            fortune = random.choice(['金運の晴れ', '恋愛運の晴れ', '仕事運の晴れ'])

        return fortune



    def show_fortune_details(self):
        return render_template("fortune_details.html", selected_layout=self.selected_layout, selected_destiny=self.selected_destiny, fortune_percentage=self.fortune_percentage)

interior_app = InteriorApp()

@app.route('/')
def home():
    return interior_app.start()

@app.route('/select_layout', methods=['POST', 'GET'])
def select_layout():
    if request.method == 'POST':
        selected_layout = request.form.get('layout')
        if selected_layout is not None:
            # レイアウトが選択されたらselect_destiny.htmlにリダイレクト
            return redirect('/select_destiny')
        else:
            return "Error: Layout not selected"
    else:
        return interior_app.select_layout()
    
@app.route('/select_destiny', methods=['POST', 'GET'])
def select_destiny():
    if request.method == 'POST':
        selected_destiny = request.form.get('destiny')
        if selected_destiny is not None:
            return interior_app.show_confirmation(selected_destiny)
        else:
            return render_template("select_destiny.html", destinies=interior_app.destinies, selected_layout=interior_app.selected_layout)
    else:
        selected_layout = request.args.get('layout')
        if selected_layout is not None:
            return interior_app.select_destiny()
        else:
            return redirect(url_for('select_layout'))

@app.route('/confirmation', methods=['POST', 'GET'])
def confirmation():
    if request.method == 'POST':
        # フォームが送信されたら、draw_fortune()メソッドを呼び出す
        return draw_fortune()
    else:
        # フォームが送信されていない場合は、confirmation.htmlを表示する
        app_instance = InteriorApp()
        return app_instance.confirmation()



@app.route('/draw_fortune', methods=['POST'])
def draw_fortune():
    app_instance = InteriorApp()
    return app_instance.draw_fortune()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8000')