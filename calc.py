import flet as ft
import math  # ファクトリアル計算や平方根、対数で使用



class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    # 計算機のルートコントロール (UI 全体を定義)
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)  # 計算結果を表示するテキスト
        self.width = 350
        self.bgcolor = ft.colors.BLACK  # 背景色
        self.border_radius = ft.border_radius.all(20)  # 角を丸く設定
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),  # 計算結果の表示部分
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),  # リセットボタン
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),  # 符号変更ボタン
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),  # パーセント計算ボタン
                        ActionButton(text="/", button_clicked=self.button_clicked),  # 割り算ボタン
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),  # 数字ボタン7
                        DigitButton(text="8", button_clicked=self.button_clicked),  # 数字ボタン8
                        DigitButton(text="9", button_clicked=self.button_clicked),  # 数字ボタン9
                        ActionButton(text="*", button_clicked=self.button_clicked),  # 掛け算ボタン
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),  # 数字ボタン4
                        DigitButton(text="5", button_clicked=self.button_clicked),  # 数字ボタン5
                        DigitButton(text="6", button_clicked=self.button_clicked),  # 数字ボタン6
                        ActionButton(text="-", button_clicked=self.button_clicked),  # 引き算ボタン
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),  # 数字ボタン1
                        DigitButton(text="2", button_clicked=self.button_clicked),  # 数字ボタン2
                        DigitButton(text="3", button_clicked=self.button_clicked),  # 数字ボタン3
                        ActionButton(text="+", button_clicked=self.button_clicked),  # 足し算ボタン
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),  # 数字ボタン0
                        DigitButton(text=".", button_clicked=self.button_clicked),  # 小数点ボタン
                        ActionButton(text="=", button_clicked=self.button_clicked),  # イコールボタン
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="^2", button_clicked=self.button_clicked),  # 平方計算ボタン
                        ActionButton(text="/2", button_clicked=self.button_clicked),  # 2で割るボタン
                        ActionButton(text="√", button_clicked=self.button_clicked),  # 平方根計算ボタン
                        ActionButton(text="ln", button_clicked=self.button_clicked),  # 自然対数ボタン
                    ],
                    alignment="end",
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="!", button_clicked=self.button_clicked),  # 階乗計算ボタン
                        ActionButton(text="Prime check", button_clicked=self.button_clicked),  # 素数判定ボタン
                    ],
                    alignment="end",
                ),
            ]
        )

    def button_clicked(self, e):
        # ボタンがクリックされたときの処理
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            # エラー時またはリセットボタンが押された場合
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            # 数字ボタンまたは小数点が押された場合
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            # 四則演算ボタンが押された場合
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data == "=":
            # イコールボタンが押された場合
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data == "%":
            # パーセント計算
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data == "+/-":
            # 符号変更処理
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        elif data == "^2":
            # 平方計算
            try:
                self.result.value = self.format_number(float(self.result.value) ** 2)
            except Exception:
                self.result.value = "Error"

        elif data == "/2":
            # 2で割る処理
            try:
                self.result.value = self.format_number(float(self.result.value) / 2)
            except Exception:
                self.result.value = "Error"

        elif data == "√":
            # 平方根計算
            try:
                if float(self.result.value) < 0:
                    self.result.value = "Error"  # 負数の平方根は計算不可
                else:
                    self.result.value = self.format_number(math.sqrt(float(self.result.value)))
            except Exception:
                self.result.value = "Error"

        elif data == "ln":
            # 自然対数計算
            try:
                if float(self.result.value) <= 0:
                    self.result.value = "Error"  # 0以下の対数は計算不可
                else:
                    self.result.value = self.format_number(math.log(float(self.result.value)))
            except Exception:
                self.result.value = "Error"

        elif data == "!":
            # 階乗計算
            try:
                value = int(float(self.result.value))  # 小数を整数に変換
                if value < 0:
                    self.result.value = "Error"  # 負数の階乗は計算不可
                else:
                    self.result.value = math.factorial(value)
            except Exception:
                self.result.value = "Error"

        elif data == "Prime check":
            # 素数判定
            try:
                value = int(float(self.result.value))  # 入力を整数に変換
                if value < 2:
                    self.result.value = f"{value} - Not Prime"  # 素数でない場合
                else:
                    is_prime = self.is_prime(value)
                    self.result.value = f"{value} - Prime" if is_prime else f"{value} - Not Prime"
            except Exception:
                self.result.value = "Error"

        self.update()

    def is_prime(self, n):
        """素数判定関数"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def format_number(self, num):
        """数値のフォーマット (整数または浮動小数点)"""
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        """四則演算を実行"""
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        """計算機をリセット"""
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App with ln Feature"
    # 計算機アプリケーションを作成
    calc = CalculatorApp()

    # ページに計算機を追加
    page.add(calc)


ft.app(target=main)
