# image-capture-class-annotation
領域を指定し、キーを入力することで画像を保存するツールです。<br>
クラス分類用のデータセット作成を想定しています。<br>
![njvnq-h1sa6](https://user-images.githubusercontent.com/37477845/119854349-f8a5cd00-bf4b-11eb-9b55-4a4d59c047f1.gif)

# Requirement 
* OpenCV 3.4.2 or later

# Usage
実行方法は以下です。<br>
起動後はマウスクリック4点で切り出し箇所の指定を行い、<br>
キー(0～9、a～z)を押下することで「capture」ディレクトリに画像を保存します。<br>
0～9は00～09ディレクトリを作成し、a以降は10から連番のディレクトリを作成します。
```bash
python image-capture-class-annotation.py
```
オプションとして以下を指定できます。
* --device<br>
入力デバイス(cv2.VideoCapture)<br>
デフォルト：0
* --width<br>
入力デバイスの幅<br>
デフォルト：640
* --height<br>
入力デバイスの高さ<br>
デフォルト：480
* --crop_width<br>
生成画像の幅<br>
デフォルト：96
* --crop_height<br>
生成画像の高さ<br>
デフォルト：96
* --extension<br>
生成画像の拡張子<br>
デフォルト：jpg
* --start_count<br>
ファイル連番の開始数<br>
デフォルト：0

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
image-capture-class-annotation is under [MITLicense](LICENSE).
