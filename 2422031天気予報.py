import requests
import flet as ft
import time  # リクエスト間の遅延を追加

# API URL を定義
REGION_API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
WEATHER_API_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{region_code}.json"

# 地域データを取得
def fetch_region_data():
    try:
        response = requests.get(REGION_API_URL)
        response.raise_for_status()
        time.sleep(1)  # リクエスト間の遅延を追加
        return {code: region["name"] for code, region in response.json()["offices"].items()}
    except requests.exceptions.RequestException as e:
        print(f"地域データの取得エラー: {e}")
        return {}

# 天気データを取得
def fetch_weather_data(region_code):
    try:
        url = WEATHER_API_URL_TEMPLATE.format(region_code=region_code)
        response = requests.get(url)
        response.raise_for_status()
        time.sleep(1)  # リクエスト間の遅延を追加
        data = response.json()
        print(f"API 応答データ ({region_code}): {data}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"HTTP リクエストエラー ({region_code}): {e}")
        return None

# Flet アプリケーション
def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10

    # 天気予報カードを作成する関数
    def build_forecast_card(date, weather_description, temp_min, temp_max):
        return ft.Card(
            content=ft.Column(
                [
                    ft.Text(date, size=16, weight="bold", text_align="center"),
                    ft.Icon(name=ft.Icons.WB_SUNNY, size=40, color=ft.colors.AMBER),  # アンバー色
                    ft.Text(weather_description, text_align="center"),
                    ft.Text(f"{temp_min}°C / {temp_max}°C", weight="bold", text_align="center"),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            elevation=4,
            width=150,
            height=200,
        )

    # 地域が選択されたときに天気予報を更新
    def update_forecast(e):
        selected_region_code = region_dropdown.value
        print(f"選択された地域コード: {selected_region_code}")
        if not selected_region_code:
            print("地域コードが選択されていません。")
            return

        # 天気データを取得
        weather_data = fetch_weather_data(selected_region_code)
        forecast_container.controls.clear()
        if not weather_data:
            forecast_container.controls.append(
                ft.Text("データがありません", color=ft.colors.RED, size=20)  # 赤色
            )
            page.update()
            return
        try:
            # タイムシリーズデータの解析
            time_series = weather_data[0]["timeSeries"]
            areas = time_series[0]["areas"]

            # 温度データが含まれているシリーズを探す
            temp_series = next(
                (series for series in time_series if "temps" in series["areas"][0]), None
            )
            temps = temp_series["areas"][0]["temps"] if temp_series else []

            # 処理済みの日付を追跡するセットを作成
            processed_dates = set()

            for idx, area in enumerate(areas):
                for date, description in zip(
                    time_series[0]["timeDefines"],
                    area["weathers"],
                ):
                    date_str = date[:10]  # YYYY-MM-DD 形式の日付を抽出

                    # すでに処理された日付の場合はスキップ
                    if date_str in processed_dates:
                        continue

                    # 処理済みの日付としてセットに追加
                    processed_dates.add(date_str)

                    # 温度データを処理
                    min_temp = temps[idx] if idx < len(temps) else "N/A"
                    max_temp = temps[idx] if idx < len(temps) else "N/A"

                    forecast_container.controls.append(
                        build_forecast_card(
                            date_str,  # 日付
                            description,
                            min_temp,
                            max_temp
                        )
                    )
        except (KeyError, IndexError) as ex:
            print(f"データの解析エラー: {ex}")
            forecast_container.controls.append(
                ft.Text("データの解析に失敗しました", color=ft.colors.RED, size=20)  # 赤色
            )
        page.update()

    # 地域データを取得し、ドロップダウンに追加
    region_data = fetch_region_data()
    region_options = [
        ft.dropdown.Option(key=code, text=name) for code, name in region_data.items()
    ]

    # UI コンポーネント
    region_dropdown = ft.Dropdown(
        label="地域選択",
        options=region_options,
        on_change=update_forecast,
        width=300,
    )
    forecast_container = ft.Row(wrap=True, spacing=10, alignment=ft.MainAxisAlignment.START)

    # ページレイアウト
    page.add(
        ft.AppBar(
            title=ft.Text("天気予報アプリ", size=20, color=ft.colors.WHITE),  # 白色
            bgcolor=ft.colors.INDIGO,  # インディゴ色
        ),
        ft.Column(
            [region_dropdown, ft.Container(content=forecast_container, padding=10)],
            alignment="start",
            spacing=20,
            scroll="auto",
        ),
    )

# Flet アプリケーションの実行
ft.app(target=main)
