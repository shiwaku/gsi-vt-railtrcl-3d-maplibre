# 必要なライブラリをインポート
import json  # GeoJSONデータの読み込みと書き込みに使用

def convert_geojson_with_z(input_geojson, z_value):
    """
    RailTrCL_16_tachikawashi のGeoJSONを指定されたフォーマットに変換し、Z値を追加します。

    Parameters:
        input_geojson (dict): 入力のGeoJSONオブジェクト
        z_value (float): 各座標に追加するZ値

    Returns:
        list: 指定されたフォーマットの変換後データ
    """
    # GeoJSONのfeaturesキーからデータを取得
    features = input_geojson.get('features', [])
    if not features:
        raise ValueError("GeoJSONには有効な'features'キーが含まれている必要があります。")

    converted = []

    for feature in features:
        geometry = feature.get('geometry', {})
        
        # ジオメトリのタイプがMultiLineStringであることを確認
        if geometry.get('type') == 'MultiLineString':
            for line in geometry.get('coordinates', []):
                # 各座標が[経度, 緯度]の形式であることを確認
                if not all(len(coord) >= 2 for coord in line):
                    raise ValueError("各座標は少なくとも[経度, 緯度]を持つ必要があります。")
                
                # 各座標にZ値を追加
                path_with_z = [[coord[0], coord[1], z_value] for coord in line]
                
                # フォーマットに従ったデータを作成
                converted.append({
                    "path": path_with_z
                })
        else:
            # 他のジオメトリタイプをスキップし、通知を表示
            print(f"ジオメトリタイプ '{geometry.get('type')}' のフィーチャーをスキップしました。")

    return converted

def convert_geojson_with_properties(input_geojson, z_value):
    """
    RdCL_16_tachikawashi のGeoJSONを指定されたフォーマットに変換し、Z値を追加します。

    Parameters:
        input_geojson (dict): 入力のGeoJSONオブジェクト
        z_value (float): 各座標に追加するZ値

    Returns:
        list: 指定されたフォーマットの変換後データ
    """
    # GeoJSONのfeaturesキーからデータを取得
    features = input_geojson.get('features', [])
    if not features:
        raise ValueError("GeoJSONには有効な'features'キーが含まれている必要があります。")

    converted = []

    for feature in features:
        geometry = feature.get('geometry', {})
        properties = feature.get('properties', {})
        
        # ジオメトリのタイプがMultiLineStringであることを確認
        if geometry.get('type') == 'MultiLineString':
            for line in geometry.get('coordinates', []):
                # 各座標が[経度, 緯度]の形式であることを確認
                if not all(len(coord) >= 2 for coord in line):
                    raise ValueError("各座標は少なくとも[経度, 緯度]を持つ必要があります。")
                
                # 各座標にZ値を追加
                path_with_z = [[coord[0], coord[1], z_value] for coord in line]
                
                # フォーマットに従ったデータを作成
                converted.append({
                    "path": path_with_z,
                    "properties": {
                        "vt_rdctg": properties.get("vt_rdctg", "不明"),
                        "vt_rnkwidth": properties.get("vt_rnkwidth", "不明")
                    }
                })
        else:
            # 他のジオメトリタイプをスキップし、通知を表示
            print(f"ジオメトリタイプ '{geometry.get('type')}' のフィーチャーをスキップしました。")

    return converted

# 入力および出力ファイルパスの設定
rail_input_path = "RailTrCL_16_tachikawashi.geojson"
rdcl_input_path = "RdCL_16_tachikawashi.geojson"

rail_output_path = "RailTrCL_16_tachikawashi_customized.json"
rdcl_output_path = "RdCL_16_tachikawashi_customized.json"

# 各ファイルに対応するZ値
rail_z_value = 17
rdcl_z_value = 1

# ファイルの処理
try:
    # 入力ファイルを読み込む
    with open(rail_input_path, 'r', encoding='utf-8') as f:
        rail_geojson = json.load(f)
    with open(rdcl_input_path, 'r', encoding='utf-8') as f:
        rdcl_geojson = json.load(f)
    
    # RailTrCLデータを変換
    rail_converted = convert_geojson_with_z(rail_geojson, rail_z_value)
    
    # RdCLデータを変換
    rdcl_converted = convert_geojson_with_properties(rdcl_geojson, rdcl_z_value)
    
    # 変換後のデータを新しいJSONファイルに保存
    with open(rail_output_path, 'w', encoding='utf-8') as f:
        json.dump(rail_converted, f, ensure_ascii=False, indent=2)
    with open(rdcl_output_path, 'w', encoding='utf-8') as f:
        json.dump(rdcl_converted, f, ensure_ascii=False, indent=2)
    
    print(f"ファイルが正常に保存されました:\n- {rail_output_path}\n- {rdcl_output_path}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
