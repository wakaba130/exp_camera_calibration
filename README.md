# exp_camera_calibration
カメラキャリブレーションのサンプルコード

WEBカメラから直接キャリブレーションができます。

## install

```bash
$ sudo pip install numpy
$ sudo pip install opencv-python
```

## execution

```bash
$ python3 capture_calibration.py [-o OUTPUT] [-s SQUARE_SIZE] [-v VIDEO_ID]
                                 [--pattern_size PATTERN_SIZE] [--sleep SLEEP]
```

+ output　・・・　出力ディレクトリ名(default:output)
+ square_size　・・・　ボードの正方形のサイズ[mm]
+ video_id　・・・　カメラのID（default:0）
+ pattern_size　・・・　ボードの頂点数(default:9x6)
+ sleep　・・・　次の検出までのスリープ時間[sec]

実行すると描画ウィンドウが表示されて、チェッカーボードが認識されると、
`Count:`が進んで行きます。

キーボードの`Esc`ボタンを押すとウィンドウが消えて、カメラパラメータの推定処理ガ実行されます。


出力は、`output`で指定したディレクトリ内に、キャリブレーションに使用した画像と、
キャリブレーション結果の`caribrate.json`が保存されます。

参考：[チェスボード画像自動生成ツール](https://mementoo.info/archives/598)
