class Voices():
    
    def __init__(self, voices_api_url, token):
        """
        APIのURLを受け取って、初期化するコンストラクタ
        """
        # TODO: APIのURLとトークンを保存する処理を実装する

        #APIのURL
        self.url = voices_api_url

        #APIのトークン（ここでheaderに設定）
        self.headers = {
            'Authorization': f'Bearer {token}'
        }
        if self.url is None or token is None:
            print("Error: API URL or token is not set.")
            
        return None

    def get_voices(self):
        """
        APIからボイスのリストを取得するメソッド
        """
        # TODO: APIからボイスのリストを取得する処理を実装する]
        #返り値の例
        """
        [
            {
                "id": "001",
                "title": "「テスト記事１」",
                "description": "テスト詳細説明１"
            },r
            {
                "id": "002",
                "title": "「テスト記事２」",
                "description": "テスト詳細説明２"
            }
        ]
        """
        import json
        import requests

        DEBUG = False

        #APIからボイスのリストを取得する処理(エラーハンドリングも含む※引用：https://techplay.jp/column/1617)

        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            #APIからのレスポンスをPythonの辞書型に変換する
            files = response.json()

            #APIからのレスポンスをJSON形式で取得して、整形して表示する
            print_data = json.dumps(files, indent=4, ensure_ascii=False)
            if DEBUG:
                print("data:", print_data)

            #filesはファイルの一覧をもっているので、ここから必要な情報を抜き取る
            voices = []
            for file in files:
                if not file["name"].endswith((".md")):
                    continue
            
                md_file = requests.get(file["download_url"], headers=self.headers)
                md_file.raise_for_status()
                md_content = md_file.text
                if DEBUG:
                    print("md_content:\n", md_content)

                #内容とヘッダが---で区切られてるのでいったん分ける
                md_parts = md_content.split("---")
                header = md_parts[1]
                body = md_parts[2]
                
                #タイトルは内容の先頭。一文字目の#を削除した。
                title = body.strip().splitlines()[0].replace("#", "").strip()
                
                #説明はヘッダの中にある。
                for line in header.splitlines():
                    #Tabがあったりなかったりするので消して処理しやすくする
                    line = line.strip()

                    if DEBUG:
                        print("line:", line)
                    
                    #説明はtext:から始まる行に書いてある
                    if line.startswith("text:"):
                        if DEBUG:
                            print("found text line:", line)
                        description = line.split("text:")[1].strip()

                #idはファイル名から拡張子を削除したもの
                id = file["name"].replace(".md", "")
                
                if DEBUG:
                    print("id:", id)
                    print("title:", title)
                    print("description:", description)
                    print("------------------")

                voices.append({
                    "id": id,
                    "title": title,
                    "description": description
                })
                
                

            return voices

        except requests.exceptions.HTTPError as errh:
            print("HTTPError:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("ConnectionError:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout:", errt)
        except requests.exceptions.RequestException as err:
            print("RequestException:",err)
        return None




    def get_voice_detail(self, voice_id: str):
        """
        APIから特定のボイスの詳細を取得するメソッド
        """
        # TODO: APIから特定のボイスの詳細を取得する処理を実装する
        #返り値の例
        """
        {
        "profile": {
                "faculty": "テスト学部",
                "department": "テスト学科",
                "graduation_year": 1234,
                "company": "テスト株式会社",
                    "industry": "テスト業界",
                "offer_timing": {
                    "grade": 12,
                    "month": 3
                },
                "offer_count": 4
            },
            "title": "「テスト記事１」",
            "voice": "テスト記事本文１"
        }
        """
        import json
        import requests

        DEBUG = False
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            #APIからのレスポンスをPythonの辞書型に変換する
            files = response.json()

            #APIからのレスポンスをJSON形式で取得して、整形して表示する
            print_data = json.dumps(files, indent=4, ensure_ascii=False)
            if DEBUG:
                print("data:", print_data)

            #filesはファイルの一覧をもっているので、ここから必要な情報を抜き取る
            for file in files:
                if file["name"].replace(".md", "") == voice_id:
                    if not file["name"].endswith((".md")):
                        continue

                    md_file = requests.get(file["download_url"], headers=self.headers)
                    md_file.raise_for_status()
                    md_content = md_file.text
                    if DEBUG:
                        print("md_content:\n", md_content)

                    #内容とヘッダが---で区切られてるのでいったん分ける
                    md_parts = md_content.split("---")
                    header = md_parts[1]
                    body = md_parts[2]

                    #profileはヘッダの情報を辞書型に変換して保存する
                    profile = {}
                    #ヘッダを行ごとに配列に格納する
                    header_lines = header.splitlines()
                    header_length = len(header_lines)
                    cnt = 0
                    line_num = 1
                    #最初の行は不要なので、1行目から処理する
                    while True:
                        line_num += 1
                        #Tabがあったりなかったりするので消して処理しやすくする
                        line = header_lines[line_num].strip()
                        if DEBUG:
                            print("line:", line, "line_num:", line_num)

                        #description以降は不要なので、description:から始まる行が出てきたらループを抜ける
                        if line.startswith("description:"):
                            break

                        #profileの情報はkey: valueの形式で書いてあるので、:で分割して保存する
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip()
                            value = value.strip()
                            #valueが数値ならintにする
                            if value.isdecimal():
                                value = int(value)

                            #offer_timingはさらにgradeとmonthに分ける
                            if key == "offer_timing":
                                offer_timing = {}
                                #offer_timingの情報はkey: valueの形式で書いてあるので、:で分割して保存する
                                for offer_line in header_lines[line_num+1:]:
                                    offer_line = offer_line.strip()
                                    if ":" in offer_line:
                                        offer_key, offer_value = offer_line.split(":", 1)
                                        if DEBUG:
                                            print("offer_line:", offer_line)
                                        offer_key = offer_key.strip()
                                        offer_value = int(offer_value.strip())
                                        offer_timing[offer_key] = offer_value
                                        cnt += 1
                                        #offer_timingはgradeとmonthの2つの情報があるので、両方取得したらループを抜ける
                                        if cnt == 2:
                                            #line_numを更新して、次の行から処理するようにする
                                            line_num += cnt
                                            if DEBUG:
                                                print("updated line_num:", line_num)
                                            break
                                    else:
                                        break
                                profile[key] = offer_timing
                            else:
                                profile[key] = value
                        #"descripthion:"以降は不要なので、ループを抜ける


                    
                    #タイトルは内容の先頭。一文字目の#を削除した。
                    title = body.strip().splitlines()[0].replace("#", "").strip()
                
                    #記事本文はタイトルの次の行から最後まで
                    voice = "\n".join(body.strip().splitlines()[1:]).strip()
                    
                    if DEBUG:
                        print("id:", voice_id)
                        print("profile:", profile)
                        print("title:", title)
                        print("voice:", voice)
                        print("------------------")
            return{
                "profile": profile,
                "title": title,
                "voice": voice
            }
        except requests.exceptions.HTTPError as errh:
            print("HTTPError:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("ConnectionError:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout:", errt)
        except requests.exceptions.RequestException as err:
            print("RequestException:",err)
        return None
